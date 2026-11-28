"""Giao diện web cho buổi người dùng thử — chạy: python codebase/web.py  → mở http://127.0.0.1:8765

Chỉ thư viện chuẩn. Gọi đúng answer() trong agent.py (cùng input "attempt=…; ly_do=…; cau=…; tra_loi=…"
như bộ câu thử), nên hành vi giống hệt `python run.py` / `run.py eval`. Không sửa khung.

- Chạy trên máy: nghe 127.0.0.1:8765. Chạy trên Render (có biến PORT): nghe 0.0.0.0:$PORT và BẮT BUỘC có
  APP_PASSCODE (thiếu thì không khởi động) — mọi /api/* phải gửi đúng mã ở header X-Passcode.
- Giới hạn MAX_AGENT_CALLS_PER_MIN lượt gọi agent / phút cho cả máy chủ (mặc định 20) để khỏi bị xài hết key.
- Ổ đĩa Render bị xoá khi khởi động lại → mỗi phiên còn được giữ trong bộ nhớ, in ra log ("[phien] …"),
  và tải được cả bộ ở GET /api/sessions (có mã). Tải về rồi commit vào validation/phien-thu/ sau buổi thử.
- Đáp án câu gốc KHÔNG gửi xuống trình duyệt: máy chủ tự chấm câu gốc và tra mã lượt sai trong
  data/learner_states.json.
- Mỗi phiên lưu một file JSON ở validation/phien-thu/ (mã người thử U1…, không tên): câu gốc sai, mã lượt,
  lý do nguyên văn + nhóm lý do (đúng quy tắc tach_doan_voi_hieu), câu tương tự, đúng/sai, số giây,
  nhận xét, và tóm tắt trace (số lần gọi model, token) của từng bước.
"""
import hmac
import json
import os
import sys
import time
from collections import deque
from datetime import datetime
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tracing  # noqa: E402
from agent import answer, _weak, WEAK  # noqa: E402
from ai import MODEL_PROVIDER, MODEL_NAME  # noqa: E402

ON_HOST = bool(os.environ.get("PORT"))          # Render (và đa số nền tảng) đặt PORT
PORT = int(os.environ.get("PORT") or 8765)
HOST = "0.0.0.0" if ON_HOST else "127.0.0.1"
PASSCODE = (os.environ.get("APP_PASSCODE") or "").strip()
MAX_CALLS = int(os.environ.get("MAX_AGENT_CALLS_PER_MIN") or 20)
_calls = deque()     # thời điểm các lượt gọi agent trong 60 giây gần nhất
SESSIONS = []        # mọi phiên đã lưu từ lúc máy chủ khởi động
_lock = threading.Lock()  # máy chủ nhiều luồng: khoá khi đụng _calls / SESSIONS
# Thứ tự câu gốc (đủ 6 ý trong ngân hàng, theo validation/quy-trinh.md). Muốn đổi thì sửa danh sách này.
ROOT_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6"]
SAVE_DIR = os.path.join(ROOT, "validation", "phien-thu")


def _load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def _roots():
    bank = _load("question_bank.json")
    found = {}
    for c in bank["concepts"]:
        for q in c["questions"]:
            if q.get("role") == "goc":
                found[q["id"]] = {"q": q, "kc": c["kc_code"]}
    return [found[i] for i in ROOT_ORDER if i in found]


def reason_group(reason):
    r = (reason or "").strip()
    if not r:
        return "bỏ qua"
    if _weak(r):  # cùng quy tắc với agent.py (tach_doan_voi_hieu)
        return "yếu"
    return "có lý do"


MIN_EXPLAIN_WORDS = 5  # lời giải thích cho An: không thuộc metric nên chặt hơn luật lý do (_weak)


def explain_group(text):
    t = str(text or "").strip()
    if not t:
        return "bỏ qua"
    return "yếu" if _weak(t) or len(t.split()) < MIN_EXPLAIN_WORDS else "có giải thích"


def rate_ok():
    now = time.time()
    with _lock:
        while _calls and now - _calls[0] > 60:
            _calls.popleft()
        if len(_calls) >= MAX_CALLS:
            return False
        _calls.append(now)
        return True


def passage_text(code):
    """Đoạn bài theo mã (chỉ đoạn bài — không có đáp án hay lời giải)."""
    for c in _load("question_bank.json")["concepts"]:
        for p in c.get("passages", []):
            if p["code"] == code:
                return p["text"]
    return None


def all_sessions():
    """Phiên trong bộ nhớ + phiên còn trên đĩa (khi chạy trên máy), không trùng file."""
    with _lock:
        out = {s["_file"]: s for s in SESSIONS}
    if os.path.isdir(SAVE_DIR):
        for name in sorted(os.listdir(SAVE_DIR)):
            if name.endswith(".json") and "validation/phien-thu/" + name not in out:
                try:
                    with open(os.path.join(SAVE_DIR, name), encoding="utf-8") as f:
                        out["validation/phien-thu/" + name] = dict(json.load(f), _file="validation/phien-thu/" + name)
                except (OSError, json.JSONDecodeError):
                    pass
    return list(out.values())


def run_agent(text):
    tracing.begin("web")
    t0 = time.perf_counter()
    try:
        out = answer(text)
        error = ""
    except Exception as e:  # lỗi gọi model: báo lên giao diện, không sập máy chủ
        out, error = {"output": "{}"}, "%s: %s" % (type(e).__name__, e)
    summary, _events = tracing.end()
    try:
        data = json.loads(out.get("output", "{}"))
    except json.JSONDecodeError:
        data = {}
    return {"input": text, "result": data, "error": error,
            "seconds": round(time.perf_counter() - t0, 2), "trace": summary}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("[web] " + (fmt % args) + "\n")

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        raw = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _json(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n).decode("utf-8") or "{}")

    def _authed(self):
        if not PASSCODE:
            return True
        return hmac.compare_digest((self.headers.get("X-Passcode") or "").encode("utf-8"), PASSCODE.encode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        if self.path == "/api/config":
            return self._send(200, {"need_code": bool(PASSCODE), "model": MODEL_NAME or MODEL_PROVIDER, "weak": sorted(WEAK), "min_explain_words": MIN_EXPLAIN_WORDS})
        if not self._authed():
            return self._send(401, {"error": "Sai mã vào trang"})
        if self.path == "/api/roots":
            roots = [{"id": r["q"]["id"], "stem": r["q"]["stem"], "options": r["q"]["options"]} for r in _roots()]
            return self._send(200, {"roots": roots, "model": MODEL_NAME or MODEL_PROVIDER})
        url = urlsplit(self.path)
        if url.path == "/api/passage":
            code = (parse_qs(url.query).get("code") or [""])[0]
            text = passage_text(code)
            return self._send(200 if text else 404, {"code": code, "text": text} if text else {"error": "không có đoạn %s" % code})
        if self.path == "/api/sessions":
            return self._send(200, {"model": MODEL_NAME or MODEL_PROVIDER, "sessions": all_sessions()})
        self._send(404, {"error": "không có"})

    def do_POST(self):
        if not self._authed():
            return self._send(401, {"error": "Sai mã vào trang"})
        try:
            body = self._json()
        except Exception:
            return self._send(400, {"error": "JSON không hợp lệ"})
        if self.path == "/api/root_answer":
            return self._send(200, self.root_answer(body))
        if self.path == "/api/agent":
            if not rate_ok():
                return self._send(429, {"error": "Quá %d lượt gọi / phút — chờ một chút rồi thử lại" % MAX_CALLS,
                                        "result": {}, "trace": {"model_calls": 0, "tokens_in": 0, "tokens_out": 0},
                                        "input": ""})
            text = str(body.get("text", ""))[:2000]
            return self._send(200, run_agent(text))
        if self.path == "/api/save":
            return self._send(200, self.save(body))
        self._send(404, {"error": "không có"})

    @staticmethod
    def root_answer(body):
        qid, chosen = str(body.get("qid", "")), str(body.get("chosen", "")).upper()
        root = next((r for r in _roots() if r["q"]["id"] == qid), None)
        if not root or chosen not in root["q"]["options"]:
            return {"error": "Không có câu %s hoặc lựa chọn %s" % (qid, chosen)}
        if chosen == root["q"]["answer"]:
            return {"correct": True}
        states = [s for s in _load("learner_states.json") if s["question_id"] == qid and s["chosen"] == chosen]
        states.sort(key=lambda s: s.get("times_wrong", 1))
        if not states:
            return {"correct": False, "error": "Thiếu mã lượt sai cho %s chọn %s trong data/learner_states.json" % (qid, chosen)}
        return {"correct": False, "attempt": states[0]["attempt_id"]}

    @staticmethod
    def save(body):
        tester = "".join(ch for ch in str(body.get("tester", "")) if ch.isalnum())[:8] or "U"
        body["tester"] = tester
        body["reason_group"] = reason_group(body.get("reason")) if body.get("entered_loop") else ""
        # lời giải thích cho An: chỉ phân loại theo luật _weak (không chấm bằng AI)
        for lp in body.get("loops") or []:
            if isinstance(lp, dict) and lp.get("anFix") is not None:
                lp["anFixGroup"] = explain_group(lp["anFix"])
        if body.get("an_fix") is not None:
            body["an_fix_group"] = explain_group(body["an_fix"])
        body["model"] = MODEL_NAME or MODEL_PROVIDER
        body["saved_at"] = datetime.now().isoformat(timespec="seconds")
        rel = "validation/phien-thu/%s-%s.json" % (tester, datetime.now().strftime("%Y%m%d-%H%M%S"))
        with _lock:
            SESSIONS.append(dict(body, _file=rel))
        print("[phien] " + json.dumps(dict(body, _file=rel), ensure_ascii=False), flush=True)  # bản dự phòng trong log
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print("[phien] không ghi được file: %s" % e, flush=True)
        return {"ok": True, "file": rel, "reason_group": body["reason_group"],
                "on_host": ON_HOST}


PAGE = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Học từ lỗi — phiên thử</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono&display=swap">
<style>
:root{--bg:#F3F6F8;--card:#fff;--ink:#0E2A3B;--navy:#0B3D5C;--teal:#0F6A80;--muted:#5E7180;--line:#E1E7EC;
  --red:#B8321F;--red-soft:#FDF1EE;--warn:#FFF7E3;--warn-line:#F3E2B3;--ok:#1E7A4C;--ok-soft:#EAF6EF;--an:#E07A2E;--an-soft:#FFF1E6;
  --r:14px;--shadow:0 1px 2px rgba(14,42,59,.06),0 6px 20px rgba(14,42,59,.06)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 'Be Vietnam Pro',system-ui,Arial,sans-serif}
button{font:inherit;cursor:pointer}
.top{display:flex;justify-content:space-between;align-items:center;padding:14px 32px;background:#fff;border-bottom:1px solid var(--line)}
.brand{font-family:'Montserrat',sans-serif;font-weight:800;font-size:20px;display:flex;gap:10px;align-items:center}
.logo{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,var(--navy),var(--teal));color:#fff;display:grid;place-items:center;font-size:15px}
.pills{display:flex;gap:8px}
.pill{font-size:13px;padding:5px 12px;border:1px solid var(--line);border-radius:999px;color:var(--muted);background:#fff}
.band{background:linear-gradient(90deg,#0A2F47,var(--navy) 60%,var(--teal));color:#fff;border-bottom:3px solid var(--red)}
.band-in{max-width:1240px;margin:0 auto;padding:14px 32px;display:flex;gap:24px;align-items:center;flex-wrap:wrap}
.kicker{font-size:11px;letter-spacing:1.2px;opacity:.75;font-weight:600}
.btitle{font-weight:700;font-size:16px}
.steps{display:flex;gap:6px;list-style:none;margin:0 0 0 auto;padding:0;flex-wrap:wrap}
.steps li{font-size:12.5px;padding:5px 11px;border-radius:999px;background:rgba(255,255,255,.10);color:rgba(255,255,255,.7);border:1px solid rgba(255,255,255,.15)}
.steps li.on{background:#fff;color:var(--navy);font-weight:700}
.steps li.done{color:#fff;background:rgba(255,255,255,.22)}
.steps li.skip{opacity:.4;text-decoration:line-through}
.timer{font-family:'JetBrains Mono',monospace;font-size:13px;opacity:.85;min-width:64px;text-align:right}
.wrap{max-width:1240px;margin:22px auto 60px;padding:0 32px;display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:22px;align-items:start}
.wrap.solo{grid-template-columns:minmax(0,760px);justify-content:center}
.wrap.solo .chat{display:none}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow);padding:30px 34px}
.label{font-size:12px;font-weight:700;letter-spacing:1px;color:var(--red);margin:0 0 10px;display:flex;justify-content:space-between}
.label span{color:var(--muted);letter-spacing:0;font-weight:600}
h1{font-family:'Montserrat',sans-serif;font-weight:800;font-size:34px;line-height:1.2;margin:0 0 12px}
h2{font-family:'Montserrat',sans-serif;font-weight:700;font-size:23px;line-height:1.35;margin:0 0 20px}
.accent{color:var(--red)}
.muted{color:var(--muted)}
.opts{display:flex;flex-direction:column;gap:10px}
.opt{display:flex;gap:14px;align-items:center;text-align:left;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:13px 16px;color:var(--ink);transition:border-color .15s,background .15s}
.opt:hover:not([disabled]){border-color:var(--teal);background:#F6FAFC}
.opt .k{flex:none;width:28px;height:28px;border-radius:8px;background:#EEF2F5;display:grid;place-items:center;font-weight:700;font-size:14px}
.opt.sel{border-color:var(--navy);background:#EEF4F8}
.opt.sel .k{background:var(--navy);color:#fff}
.opt[disabled]{cursor:default}
.opt[disabled]:not(.sel){opacity:.55}
.primary{background:var(--red);color:#fff;border:0;border-radius:11px;padding:12px 22px;font-weight:700;box-shadow:0 4px 14px rgba(184,50,31,.25)}
.primary.navy{background:var(--navy);box-shadow:0 4px 14px rgba(11,61,92,.25)}
.primary[disabled]{opacity:.4;cursor:default;box-shadow:none}
.ghost{background:#fff;border:1.5px solid var(--line);border-radius:11px;padding:10px 18px;color:var(--ink);font-weight:600}
.row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:20px}
.panel{border-radius:12px;padding:16px 18px;margin-top:20px;border:1px solid}
.panel.warn{background:var(--warn);border-color:var(--warn-line)}
.panel.ok{background:var(--ok-soft);border-color:#C6E6D3}
.panel.no{background:var(--red-soft);border-color:#F2CFC7}
.panel h3{margin:0 0 6px;font-size:18px}
.ok-t{color:var(--ok)}.no-t{color:var(--red)}
.recap{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin-top:10px;font-size:15px}
.recap b{color:var(--muted);font-weight:600}
input[type=text],input[type=password],textarea{width:100%;font:inherit;padding:11px 13px;border:1.5px solid var(--line);border-radius:11px;background:#fff;color:var(--ink)}
input:focus,textarea:focus{outline:none;border-color:var(--teal)}
textarea{min-height:80px;resize:vertical}
label{display:block;font-weight:600;margin:18px 0 6px}
.radio{display:flex;gap:10px;flex-wrap:wrap}
.radio label{font-weight:500;margin:0;display:flex;gap:6px;align-items:center;border:1.5px solid var(--line);border-radius:999px;padding:6px 14px}
.err{color:var(--red);font-weight:600}
/* chat */
.chat{background:#fff;border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow);display:flex;flex-direction:column;height:calc(100vh - 170px);min-height:480px;position:sticky;top:16px}
.chat-h{padding:16px 18px 12px;border-bottom:1px solid var(--line)}
.chat-h b{display:block}.chat-h small{color:var(--muted)}
.chat-h.tabs{display:flex;gap:6px;padding:10px}
.ctab{flex:1;display:flex;gap:10px;align-items:center;text-align:left;background:none;border:1.5px solid transparent;border-radius:12px;padding:8px 10px;color:var(--ink)}
.ctab .av{flex:none;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:700;color:#fff;background:linear-gradient(135deg,var(--navy),var(--teal))}
.ctab.an .av{background:var(--an)}
.ctab .tt b{font-size:14.5px}.ctab .tt small{font-size:12px}
.ctab.on{background:#EEF6F3;border-color:#CFE5DD}
.ctab.an.on{background:var(--an-soft);border-color:#F6D3B6}
.ctab[disabled]{opacity:.4;cursor:not-allowed}
.ctab.unread{border-color:var(--an);animation:pulse 1.6s ease-in-out infinite}
.ctab.unread .tt b::after{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--red);margin-left:6px;vertical-align:2px}
.ctab.unread .tt small{color:var(--red);font-weight:700}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(224,122,46,.0)}50%{box-shadow:0 0 0 5px rgba(224,122,46,.25)}}
.who{display:none}
.chat.dm .an .who{display:none}
.optview{display:flex;gap:14px;align-items:center;border:1.5px solid var(--line);border-radius:12px;padding:13px 16px;opacity:.6}
.optview.both{opacity:1;border-color:var(--an);background:var(--an-soft)}
.optview .k{flex:none;width:28px;height:28px;border-radius:8px;background:#EEF2F5;display:grid;place-items:center;font-weight:700;font-size:14px}
.optview .tag{margin-left:auto;font-size:12px;font-weight:700;color:var(--an);white-space:nowrap}
.log{flex:1;overflow-y:auto;padding:16px 16px 8px;display:flex;flex-direction:column;gap:14px}
.mrow{display:flex;gap:10px;align-items:flex-end}
.mrow.me{flex-direction:row-reverse}
.av{flex:none;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:700;color:#fff}
.ai .av{background:linear-gradient(135deg,var(--navy),var(--teal))}
.an .av{background:var(--an)}
.me .av{display:none}
.who{font-size:12px;font-weight:700;color:var(--muted);margin:0 0 3px}
.an .who{color:var(--an)}
.bub{max-width:300px;padding:10px 14px;border-radius:16px;font-size:15px}
.ai .bub{background:#EEF6F3;border-bottom-left-radius:4px}
.an .bub{background:var(--an-soft);border:1px solid #F6D3B6;border-bottom-left-radius:4px}
.me .bub{background:var(--navy);color:#fff;border-bottom-right-radius:4px;max-width:260px}
.me .bub.empty{background:#EEF2F5;color:var(--muted);font-style:italic}
.quick{display:flex;flex-direction:column;align-items:flex-end;gap:8px;padding:10px 12px 0}
.quick:empty{display:none}
.divider{align-self:center;font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:2px 12px;background:var(--bg)}
.chat-in textarea{overflow:hidden}
.chip{border:1.5px solid var(--teal);color:var(--teal);background:#fff;border-radius:999px;padding:6px 13px;font-size:14px;font-weight:600;text-align:left}
.chip:hover:not([disabled]){background:var(--teal);color:#fff}
.chip.quiet{border-color:var(--line);color:var(--muted)}
.chip[disabled]{opacity:.45;cursor:default}
.typing .bub{color:var(--muted)}
.typing .bub::after{content:'';display:inline-block;width:1.4em;animation:dots 1.2s steps(4,end) infinite}
@keyframes dots{0%{content:''}25%{content:'.'}50%{content:'..'}75%{content:'...'}}
.chat-in{border-top:1px solid var(--line);padding:12px;display:flex;gap:8px;align-items:flex-end}
.chat-in textarea{min-height:44px;height:44px;border-radius:12px;font-size:15px}
.send{flex:none;width:44px;height:44px;border-radius:12px;border:0;background:var(--navy);color:#fff;font-size:18px}
.send[disabled]{opacity:.35;cursor:default}
.cite{font:inherit;font-size:12.5px;font-weight:700;background:#fff;border:1.5px solid var(--red);color:var(--red);padding:0 8px;border-radius:999px;margin:0 2px;vertical-align:1px}
.cite[disabled]{opacity:.6}
.bub.src{background:#fff;border:1.5px dashed #CFE0DA;display:flex;flex-direction:column;align-items:flex-start;gap:6px}
.src-h{font-size:12px;font-weight:700;color:var(--muted);letter-spacing:.3px}
.bub.src .cite{font-size:13.5px;padding:3px 10px;margin:0}
.bub.src blockquote.passage{margin:2px 0 0}
.mrow.cont .av{visibility:hidden}
.mrow.next{margin-top:-8px}
blockquote.passage{margin:10px 0 2px;padding:9px 12px;border-left:3px solid var(--red);background:#fff;border-radius:0 8px 8px 0;font-size:14px}
details{margin-top:26px;color:var(--muted);font-size:13px}
details pre{white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:12px;background:var(--bg);padding:12px;border-radius:10px}
.summary{background:var(--bg);border-radius:10px;padding:14px;font-family:'JetBrains Mono',monospace;font-size:13px;white-space:pre-wrap}
@media (max-width:960px){.wrap{grid-template-columns:1fr}.chat{position:static;height:520px}.steps{margin-left:0}}
</style></head>
<body>
<header class="top"><div class="brand"><span class="logo">✦</span>Học từ lỗi</div>
  <div class="pills"><span class="pill" id="who">Phiên thử · nhóm Zebra</span><span class="pill" id="model">model …</span></div></header>
<div class="band"><div class="band-in">
  <div><div class="kicker">ÔN LẠI CHỖ SAI · KHÔNG TÍNH ĐIỂM</div><div class="btitle" id="btitle">Bắt đầu phiên</div></div>
  <ol class="steps" id="steps"></ol><span class="timer" id="timer"></span></div></div>
<div class="wrap solo" id="wrap">
  <section class="card" id="app"></section>
  <aside class="chat" id="chat"><div class="chat-h" id="chatH"></div>
    <div class="log" id="log"></div><div class="log" id="dm" style="display:none"></div><div class="quick" id="quick"></div><div class="chat-in" id="chatIn"></div></aside>
</div>
<script>
const $app=document.getElementById('app'), $group=document.getElementById('log'), $dm=document.getElementById('dm'), $chat=document.getElementById('chat'), $chatH=document.getElementById('chatH');
let $log=$group;  // khung đang hiện: nhóm chung hoặc tin nhắn riêng với An
// khung chat bị thu lại (hiện lựa chọn trả lời nhanh, ô nhập) → giữ tin mới nhất trong tầm nhìn
const pinBottom=new ResizeObserver(es=>es.forEach(e=>{ e.target.scrollTop=e.target.scrollHeight; })); pinBottom.observe($group); pinBottom.observe($dm);
const $in=document.getElementById('chatIn'), $quick=document.getElementById('quick');
const S = {tester:'', roots:[], idx:0, rootLog:[], loops:[], attempt:null, rootWrong:null, rootQid:null, rootChosen:null, reason:null, anFix:null,
           similar:null, answer:null, correct:null, t0:null, seconds:null, calls:[], model:'', needCode:false,
           code: sessionStorage.getItem('passcode')||''};
const el = (tag, attrs={}, ...kids) => { const e=document.createElement(tag);
  for (const [k,v] of Object.entries(attrs)) { if (k==='class') e.className=v; else if (k.startsWith('on')) e.addEventListener(k.slice(2),v); else e.setAttribute(k,v); }
  for (const k of kids) if (k!=null) e.append(k instanceof Node ? k : document.createTextNode(k)); return e; };
const hdr = () => ({'Content-Type':'application/json','X-Passcode':S.code});
const post = (url, body) => fetch(url,{method:'POST',headers:hdr(),body:JSON.stringify(body)}).then(r=>r.json());
const get = url => fetch(url,{headers:hdr()}).then(async r=>({status:r.status, data:await r.json()}));

/* ---- khung: bước, đồng hồ, bố cục ---- */
const STEPS=['Câu gốc','Lý do','Kiểm lại','Giải thích cho An','Kết quả'];
function setStep(i, skip=[]){ document.getElementById('steps').replaceChildren(...STEPS.map((s,j)=>el('li',{class:j===i?'on':(skip.includes(j)?'skip':(j<i?'done':''))},s))); }
function layout(chat){ document.getElementById('wrap').className='wrap'+(chat?'':' solo'); }
const title = t => document.getElementById('btitle').textContent=t;
/* Hai cuộc trò chuyện riêng: Zebra (trợ lý, mở sẵn) và bạn học An (hiện khi An nhắn lần đầu, giữ lịch sử qua các vòng) */
let anOpened=false, dmLocked=false, anUnread=false, onOpenAn=null;
function renderTabs(active){
  $chatH.className='chat-h tabs';
  const tab=(id,av,name,sub)=>{ const b=el('button',{class:'ctab '+id+(active===id?' on':'')+(id==='an'&&anUnread?' unread':''),onclick:()=>switchTo(id)},
      el('span',{class:'av'},av), el('span',{class:'tt'},el('b',{},name),el('small',{},sub)));
    if (dmLocked && id!=='an') { b.disabled=true; b.title='Trả lời An trước đã'; } return b; };
  $chatH.replaceChildren(tab('zebra','Z','Zebra','Trợ lý ôn lỗi'), ...(anOpened?[tab('an','An','Bạn học An',anUnread?'Tin nhắn mới':'Tin nhắn riêng')]:[])); }
function switchTo(id){
  if (id==='zebra' && dmLocked) return;
  if (id==='an' && onOpenAn) { const f=onOpenAn; onOpenAn=null; anUnread=false; dmLocked=true; setTimeout(f,0); }  // mở tab An lần này → An bắt đầu nhắn, khoá tab Zebra tới khi trả lời
  const z=id==='zebra'; $group.style.display=z?'':'none'; $dm.style.display=z?'none':'';
  $log=z?$group:$dm; $chat.classList.toggle('dm',!z); if (z) clearChips(); renderTabs(id); $log.scrollTop=$log.scrollHeight; }
function groupHeader(){ renderTabs($log===$dm?'an':'zebra'); }
/* An nhắn riêng: khoá tab Zebra (có gợi ý, đoạn bài) cho tới khi trả lời An */
/* An nhắn: chỉ hiện chấm "tin nhắn mới" ở tab An; học viên đọc xong Zebra rồi TỰ bấm sang (không tự chuyển) */
function enterDM(){
  anOpened=true; anUnread=true; renderTabs('zebra');
  const hadDm=$dm.children.length>0;
  return new Promise(r=>{ onOpenAn=()=>{ if (hadDm) divider('Câu '+S.rootQid); r(); }; }); }
function leaveDM(){ dmLocked=false; if ($log===$dm) switchTo('zebra'); else renderTabs('zebra'); }
let tick=null;
function startTimer(){ S.t0=performance.now(); clearInterval(tick); tick=setInterval(()=>{document.getElementById('timer').textContent='⏱ '+((performance.now()-S.t0)/1000).toFixed(0)+' giây';},500); }
function stopTimer(){ if(S.t0==null) return; S.seconds=Math.round((performance.now()-S.t0)/100)/10; clearInterval(tick); document.getElementById('timer').textContent='⏱ '+S.seconds+' giây'; }

/* ---- chat ---- */
const WHO={ai:['Z','Zebra'], an:['An','Bạn học An'], me:['','Bạn']};
/* Nhịp tin nhắn kiểu visual novel: mọi tin đi qua hàng đợi Q — "đang gõ…" theo số chữ, rồi dừng để đọc. Bấm vào khung chat để tua nhanh. */
let Q=Promise.resolve(), skipper=null;
const idle = () => Q;
const nWords = t => (t||'').trim().split(/\s+/).filter(Boolean).length;
function sleep(ms){ return new Promise(r=>{ const t=setTimeout(()=>{ skipper=null; r(); },ms); skipper=()=>{ clearTimeout(t); skipper=null; r(); }; }); }
[$group,$dm].forEach(x=>x.addEventListener('click',()=>{ if (skipper) skipper(); }));
const enqueue = fn => (Q=Q.then(fn).catch(e=>console.error(e)));
function appendRow(who, b, target){
  const prev=target.lastElementChild; const cont=prev && prev.classList.contains('mrow') && prev.classList.contains(who) && !prev.classList.contains('typing');
  if (cont) prev.classList.add('cont');
  target.append(el('div',{class:'mrow '+who+(cont?' next':'')}, el('div',{class:'av'},WHO[who][0]), el('div',{}, (who==='me'||cont)?null:el('p',{class:'who'},WHO[who][1]), b)));
  target.scrollTop=target.scrollHeight; }
function typingRow(who, target){
  const r=el('div',{class:'mrow '+who+' typing'},el('div',{class:'av'},WHO[who][0]),el('div',{},el('div',{class:'bub'},(who==='an'?'An':'Zebra')+' đang gõ')));
  target.append(r); target.scrollTop=target.scrollHeight; return r; }
function bubble(who, ...kids){
  const b=el('div',{class:'bub'},...kids); const target=$log;
  enqueue(async ()=>{
    const n=nWords(b.textContent);
    if (who!=='me') { const t=typingRow(who,target); await sleep(Math.min(350+40*n, 2400)); t.remove(); }
    appendRow(who,b,target);
    if (who!=='me') await sleep(Math.min(250+25*n, 1500));   // thời gian đọc trước tin kế
  });
  return b; }
function divider(text){ const target=$log; enqueue(()=>{ target.append(el('div',{class:'divider'},text)); target.scrollTop=target.scrollHeight; }); }
function anSays(text, then){ chatOff(); bubble('an',text); if (then) enqueue(then); }
function typing(){ const r=el('div',{class:'mrow ai typing'},el('div',{class:'av'},'Z'),el('div',{},el('div',{class:'bub'},'Zebra đang nghĩ'))); $log.append(r); $log.scrollTop=$log.scrollHeight; return r; }
/* trả lời nhanh: xếp từ ô nhập lên trên, căn phải; chọn xong thì xoá */
function chips(list){ enqueue(()=>{ $quick.replaceChildren(...list.slice().reverse()); requestAnimationFrame(()=>{ $log.scrollTop=$log.scrollHeight; }); }); return $quick; }
const clearChips = () => $quick.replaceChildren();
function chatInput(placeholder, onSend){ enqueue(()=>chatInputNow(placeholder, onSend)); }
function chatInputNow(placeholder, onSend){
  const t=el('textarea',{placeholder}); const s=el('button',{class:'send',title:'Gửi'},'➤');
  const go=()=>{ const v=t.value.trim(); if(!v) return; $in.replaceChildren(); onSend(v); };
  s.addEventListener('click',go); t.addEventListener('keydown',e=>{ if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();go();} });
  $in.replaceChildren(t,s); t.focus(); return t; }
function chatOff(){ $in.replaceChildren(el('textarea',{placeholder:'…',disabled:''}), el('button',{class:'send',disabled:''},'➤')); }

/* lời nhắn "ý … [mã] … hướng dẫn" → tách 3 tin: ý chính · nguồn (bấm xem đoạn bài) · hướng dẫn */
function sourceBubble(code){
  S.shownCodes=S.shownCodes||new Set(); if (S.shownCodes.has(code)) return null; S.shownCodes.add(code);  // mỗi nguồn chỉ hiện 1 lần / vòng
  let b; const btn=el('button',{class:'cite',title:'Xem đoạn bài',onclick:async ev=>{ ev.currentTarget.disabled=true;
    const r=await get('/api/passage?code='+encodeURIComponent(code));
    b.append(el('blockquote',{class:'passage'}, r.data.text||r.data.error||'')); $log.scrollTop=$log.scrollHeight; }},'📄 Xem đoạn bài '+code);
  b=bubble('ai', el('span',{class:'src-h'},'Nguồn trong bài học'), btn); b.classList.add('src'); return b; }
function sayParts(text, prefix){
  const m=/\[([A-Za-z0-9]+-P\d+)\]/.exec(text||'');
  if (!m) return bubble('ai', prefix||null, text||'');
  const before=text.slice(0,m.index).trim(), after=text.slice(m.index+m[0].length).trim();
  if (before||prefix) bubble('ai', prefix||null, before);
  sourceBubble(m[1]);
  if (after) bubble('ai', after); }
function aiSay(c, prefix){
  if (c.error) return bubble('ai', el('span',{class:'err'},'Lỗi: '+c.error));
  return sayParts(c.result.loi_nhan||'', prefix); }

async function callAgent(text){
  await idle(); const t=typing();
  let c; try { c=await post('/api/agent',{text}); } catch(e) { c={error:String(e)}; } finally { t.remove(); }
  c.result=c.result||{}; c.trace=c.trace||{model_calls:0,tokens_in:0,tokens_out:0}; c.input=c.input||text;
  S.calls.push(c); return c; }

async function downloadAll(){
  const r=await get('/api/sessions');
  if (r.status!==200) { alert(r.data.error||'Không tải được'); return; }
  const blob=new Blob([JSON.stringify(r.data,null,2)],{type:'application/json'});
  const a=el('a',{href:URL.createObjectURL(blob),download:'phien-thu-'+new Date().toISOString().slice(0,16).replace(/[:T]/g,'')+'.json'});
  document.body.append(a); a.click(); a.remove(); }
const dlButton = () => el('button',{class:'ghost',onclick:downloadAll},'Tải toàn bộ phiên (JSON)');
function techBox(){ const d=el('details',{},el('summary',{},'Chi tiết kỹ thuật (cho người cầm máy)'));
  d.append(el('pre',{},S.calls.map(c=>'> '+c.input+'\n  buoc='+(c.result.buoc||'')+' ma_doan='+JSON.stringify(c.result.ma_doan||[])+' · gọi model '+c.trace.model_calls+' · token '+c.trace.tokens_in+'/'+c.trace.tokens_out+(c.error?'\n  LỖI: '+c.error:'')).join('\n'))); return d; }

/* câu hỏi nhiều lựa chọn: chọn rồi bấm gửi */
function mcq(options, btnText, onSubmit){
  let pick=null; const send=el('button',{class:'primary',disabled:''},btnText);
  const box=el('div',{class:'opts'});
  for (const [k,v] of Object.entries(options)) box.append(el('button',{class:'opt',onclick:ev=>{
    [...box.children].forEach(b=>b.classList.remove('sel')); ev.currentTarget.classList.add('sel'); pick=k; send.disabled=false; }},
    el('span',{class:'k'},k), el('span',{},v)));
  send.addEventListener('click',()=>{ if(!pick) return; [...box.children].forEach(b=>b.disabled=true); send.disabled=true; onSubmit(pick); });
  return [box, el('div',{class:'row'},send)]; }

/* ---- màn hình ---- */
function screenStart(){
  layout(false); setStep(-1); title('Bắt đầu phiên');
  $app.replaceChildren(
    el('p',{class:'label'},'PHIÊN THỬ'),
    el('h1',{},'Thử công cụ, ', el('span',{class:'accent'},'không chấm bạn')),
    el('p',{class:'muted'},'Bạn trả lời vài câu ngắn. Sai là bình thường — thậm chí giúp nhóm hơn. Không ghi tên, không quay. Cứ nói to lựa chọn và nghĩ gì thì nói nấy.'),
    ...(S.needCode ? [el('label',{for:'code'},'Mã vào trang (nhóm giữ, không đưa người thử)'), el('input',{type:'password',id:'code',value:S.code})] : []),
    el('label',{for:'tester'},'Mã người thử (người cầm máy điền, vd U1)'),
    el('input',{type:'text',id:'tester',placeholder:'U1'}),
    el('p',{class:'err',id:'starterr'}),
    el('div',{class:'row'}, el('button',{class:'primary navy',onclick:async ()=>{
      if (S.needCode) { S.code=(document.getElementById('code').value||'').trim(); sessionStorage.setItem('passcode',S.code); }
      S.tester=(document.getElementById('tester').value||'').trim(); if(!S.tester){alert('Điền mã người thử, vd U1');return;}
      const r=await get('/api/roots');
      if (r.status!==200) { document.getElementById('starterr').textContent=r.data.error||'Lỗi'; return; }
      S.roots=r.data.roots; document.getElementById('who').textContent='Người thử '+S.tester; screenRoot(); }},'Bắt đầu'), dlButton()));
}

function screenRoot(){
  leaveDM(); clearChips();
  layout(true); setStep(0); title('Câu gốc '+(S.idx+1)+' / '+S.roots.length);
  if (S.idx===0) { $log.replaceChildren(); bubble('ai','Chào bạn, mình là Zebra! Làm câu bên trái nhé. Nếu sai, mình sẽ hỏi lại ngay ở đây — không tính điểm.'); chatOff(); }
  const r=S.roots[S.idx];
  if (S.idx>0) divider('Câu '+(S.idx+1)+' · '+r.id);
  const [box,row]=mcq(r.options,'Gửi câu trả lời', async k=>{
    const res=await post('/api/root_answer',{qid:r.id,chosen:k});
    if (res.error && !res.attempt) { $app.append(el('p',{class:'err'},res.error)); return; }
    S.rootLog.push({qid:r.id, chosen:k, correct:res.correct});
    if (res.correct) {
      const last=S.idx+1>=S.roots.length;
      $app.append(el('div',{class:'panel ok'},el('h3',{class:'ok-t'},'Đúng rồi!'),el('p',{class:'muted',style:'margin:0'},'Câu này bạn nắm rồi — sang câu tiếp.'),
        el('div',{class:'row'},el('button',{class:'primary navy',onclick:()=>{ S.idx++; last?screenFeedback(S.loops.length>0):screenRoot(); }}, last?'Hết câu — sang nhận xét':'Câu tiếp theo'))));
    } else {
      resetLoop(); S.attempt=res.attempt; S.rootQid=r.id; S.rootChosen=k; S.rootWrong=r.id+' (chọn '+k+')';
      $app.append(el('div',{class:'panel warn'},el('h3',{},'Chưa đúng — khoan xem đáp án.'),
        el('p',{class:'muted',style:'margin:0'},'Cùng Zebra thảo luận về câu này nhé 👉')));
      await askReason();
    }
  });
  $app.replaceChildren(el('p',{class:'label'},'CÂU GỐC',el('span',{},'Câu '+(S.idx+1)+'/'+S.roots.length+' · '+r.id)), el('h2',{},r.stem), box, row);
}

async function askReason(){
  setStep(1); title('Vì sao bạn chọn vậy?');
  const c=await callAgent('attempt='+S.attempt);
  startTimer(); aiSay(c);
  const list=[];
  for (const o of (c.result.lua_chon_ly_do||[])) {
    if (o.startsWith('Lý do khác')) continue;
    const kind = o==='Mình đoán' ? 'chip_doan' : 'chip_ly_do';
    list.push(el('button',{class:'chip',onclick:()=>chooseReason(o, kind)},o)); }
  list.push(el('button',{class:'chip quiet',onclick:()=>chooseReason('', 'bo_qua')},'Bỏ qua'));
  chips(list);
  chatInput('Hoặc tự gõ lý do của bạn…', v=>chooseReason(v, 'tu_go'));
}

const AN_RE=/^Bạn An nói: "([\s\S]*?)" An đang nhầm ở đâu\? Gợi ý: ([\s\S]*)$/;
const since = t => Math.round((performance.now()-t)/100)/10;
// cùng luật _weak của agent.py (danh sách từ /api/config) — chỉ luật, không gọi AI
const weakExplain = v => isWeak(v) || (v||'').trim().split(/\s+/).filter(Boolean).length < S.minWords;  // lời giải thích cho An: thêm điều kiện ≥ 5 chữ
const isWeak = v => { const r=(v||'').trim().toLowerCase(); return S.weak.includes(r) || r.includes('đoán') || r.includes('doan') || [...r].length<=3; };
async function chooseReason(text, kind){
  // đo cách học viên đưa lý do (chỉ ghi lại, không đổi luồng): bấm lựa chọn / bấm 'Mình đoán' / tự gõ / bỏ qua + số giây suy nghĩ
  S.reasonMeta={kind, seconds:since(S.t0), chars:(text||'').trim().length};
  text=(text||'').replace(/[;\n\r]+/g,', ').trim();  // ';' là dấu ngăn khoá trong input của agent
  S.reason=text; clearChips(); chatOff();
  if (text) bubble('me',text); else { const b=bubble('me','(bỏ qua)'); b.classList.add('empty'); }
  const c=await callAgent('attempt='+S.attempt+'; ly_do='+text);
  // sua_loi_ban: bỏ phần "Bạn An nói…" (đó là lời chính học viên) — An xuất hiện SAU khi học viên kiểm lại đúng
  const m=(c.result.buoc==='sua_loi_ban' && !c.error) ? AN_RE.exec(c.result.loi_nhan||'') : null;
  if (m) { bubble('ai','Cảm ơn bạn đã nói rõ suy nghĩ — nhiều bạn cũng nghĩ vậy đấy.'); sayParts(m[2], el('b',{},'Gợi ý: ')); }
  else aiSay(c);
  await idle(); showSimilar(c);
}

/* Giải thích cho An: chỉ khi đã kiểm lại ĐÚNG — lúc đó học viên mới có cái để giải thích (sau khi dừng đồng hồ, không cộng vào thời gian một vòng) */
function explainToAn(){
  return new Promise(async done0=>{
    // xong: Ở LẠI tin nhắn riêng; quay lại nhóm khi bấm chip hoặc "Câu tiếp theo" / sang nhận xét
    const done=()=>{ chatOff(); dmLocked=false; renderTabs('an'); chips([el('button',{class:'chip',onclick:()=>{ clearChips(); leaveDM(); }},'↩ Quay lại chat với Zebra')]); done0(); };
    setStep(3); title('Bạn học An nhắn riêng cho bạn');
    const root=S.roots.find(r=>r.id===S.rootQid)||{options:{}}; const opt=root.options[S.rootChosen]||'';
    // bên trái: câu GỐC (không phải câu kiểm lại vừa làm), đánh dấu lựa chọn sai chung — không đánh dấu đáp án đúng
    $app.replaceChildren(el('p',{class:'label'},'AN HỎI VỀ CÂU NÀY',el('span',{},'câu gốc '+S.rootQid)), el('h2',{},root.stem||''),
      el('div',{class:'opts'},...Object.entries(root.options).map(([k,v])=>el('div',{class:'optview'+(k===S.rootChosen?' both':'')},
        el('span',{class:'k'},k), el('span',{},v), k===S.rootChosen?el('span',{class:'tag'},'Bạn và An đã chọn'):null))));
    const hint=el('div',{class:'panel warn'},el('p',{style:'margin:0'},'💬 Bạn học An vừa nhắn riêng hỏi về câu này. Đọc xong tin của Zebra thì bấm tab ',el('b',{},'Bạn học An'),' ở khung bên phải nhé.'));
    $app.append(hint);
    await enterDM();  // chờ học viên tự bấm tab An
    hint.remove();
    bubble('an','Ê bạn ơi 👋 Câu '+S.rootQid+' lúc nãy mình cũng chọn '+S.rootChosen+': “'+opt.replace(/[.。]+$/,'')+'” giống bạn đó 😅');
    bubble('an','Vì sao '+S.rootChosen+' chưa đúng vậy? Bạn giải thích giúp mình với!');
    const tAn=performance.now(); let tries=0;
    const ask=()=>{
      chips([el('button',{class:'chip quiet',onclick:()=>{ clearChips(); chatOff(); after(''); }},'Để sau')]);
      chatInput('Giải thích cho An…', v=>{ clearChips(); chatOff(); after(v); }); };
    const after=v=>{
      tries++;
      S.anFix=v; S.anFixMeta={kind:v?'tu_go':'bo_qua', weak:!!v&&weakExplain(v), tries, seconds:since(tAn), chars:v.length};
      if (!v) { const b=bubble('me','(bỏ qua)'); b.classList.add('empty'); return anSays('Không sao, để mình xem lại đoạn bài nhé!', done); }
      bubble('me',v);
      if (weakExplain(v) && tries<2) return anSays('Hmm, mình chưa hiểu lắm 😅 Bạn nói rõ hơn một chút được không?', ask);
      anSays(weakExplain(v) ? 'Ừm, để mình đọc lại đoạn bài vậy. Cảm ơn bạn nhé!' : 'À, hiểu rồi, cảm ơn bạn! 🙌', done); };
    ask();
  }); }

/* nhiều vòng trong một phiên: metric dùng vòng ĐẦU (trường gốc của phiên), mọi vòng lưu ở loops */
const LOOP_KEYS=['attempt','rootWrong','rootQid','rootChosen','reason','reasonMeta','anFix','anFixMeta','similar','answer','correct','seconds'];
function resetLoop(){ for (const k of LOOP_KEYS) S[k]=null; S.t0=null; S.shownCodes=new Set(); }
function endLoop(){ const o={}; for (const k of LOOP_KEYS) o[k]=S[k]??null; S.loops.push(o); }
function nextButtons(){
  const more=S.idx+1<S.roots.length;
  return el('div',{class:'row'},
    ...(more?[el('button',{class:'primary navy',onclick:()=>{ S.idx++; screenRoot(); }},'Câu tiếp theo')]:[]),
    el('button',{class:more?'ghost':'primary navy',onclick:()=>screenFeedback(true)}, more?'Kết thúc — sang nhận xét':'Hết câu — sang nhận xét')); }
function showSimilar(c){
  const q=c.result.cau_tuong_tu;
  if (!q) { stopTimer(); $app.replaceChildren(el('p',{class:'label'},'KIỂM LẠI'), el('h2',{},'Chưa có câu kiểm lại cho lượt này'),
      nextButtons()); endLoop(); return; }
  setStep(2); title('Câu kiểm lại — cùng ý, không tính điểm'); S.similar=q.id;
  const [box,row]=mcq(q.options,'Kiểm lại', k=>grade(k));
  $app.replaceChildren(el('p',{class:'label'},'CÂU KIỂM LẠI',el('span',{},'cùng ý với '+S.rootQid+' · '+q.id)), el('h2',{},q.stem), box, row);
}

async function grade(k){
  S.answer=k;
  const c=await callAgent('attempt='+S.attempt+'; ly_do='+S.reason+'; cau='+S.similar+'; tra_loi='+k);
  stopTimer(); S.correct=c.result.dung;
  const lead=/^\s*(Chưa đúng|Đúng)/i.test(c.result.loi_nhan||'');  // agent đã mở đầu bằng Đúng / Chưa đúng → không thêm lần nữa
  aiSay(c, lead?null:(S.correct?el('b',{class:'ok-t'},'Đúng. '):el('b',{class:'no-t'},'Chưa đúng. ')));
  await idle();
  if (S.correct) {
    $app.append(el('div',{class:'panel ok'},el('h3',{class:'ok-t'},'Đúng rồi!'),el('p',{class:'muted',style:'margin:0'},'Bạn học An vừa nhắn riêng — bấm vào tab "Bạn học An" ở khung bên phải khi bạn sẵn sàng 👉')));
    await explainToAn();
    $app.replaceChildren(el('p',{class:'label'},'KẾT QUẢ',el('span',{},S.rootQid+' → '+S.similar)), el('h2',{},'Vòng hỏi lại của bạn'));
  }
  setStep(4, S.correct?[]:[3]); title('Kết quả vòng hỏi lại');
  $app.querySelectorAll('.panel').forEach(p=>p.remove());
  $app.append(el('div',{class:'panel '+(S.correct?'ok':'no')},
    el('h3',{class:S.correct?'ok-t':'no-t'}, S.correct?'Bạn đã sửa được chỗ sai 🎉':'Chưa đúng, bạn nên hỏi lab coach hoặc mentor câu này nhé!'),
    el('div',{class:'recap'},
      el('b',{},'Lần đầu'), el('span',{},S.rootQid+' · chọn '+S.rootChosen+' ✗'),
      el('b',{},'Kiểm lại'), el('span',{},S.similar+' · chọn '+k+' '+(S.correct?'✓':'✗')),
      el('b',{},'Lý do'), el('span',{},S.reason||'(bỏ qua)'),
      ...(S.anFix!=null?[el('b',{},'Giải thích cho An'), el('span',{},S.anFix||'(chưa biết)')]:[]),
      el('b',{},'Thời gian'), el('span',{},S.seconds+' giây')),
    nextButtons()));
  endLoop();
}

function radio(name, values){ return el('div',{class:'radio'},...values.map(v=>el('label',{},el('input',{type:'radio',name,value:v}),v))); }
const val = id => (document.getElementById(id)?.value||'').trim();

function screenFeedback(entered){
  leaveDM(); clearChips();
  layout(false); setStep(-1); title('Nhận xét sau phiên');
  $app.replaceChildren(
    el('p',{class:'label'},'NHẬN XÉT SAU PHIÊN'),
    el('h2',{},entered?'Cảm ơn bạn — vài câu cuối':'Bạn đúng hết câu gốc — không vào vòng hỏi lại'),
    el('label',{},'Nếu mai không được dùng nữa, bạn thấy:'), radio('tiec',['rất tiếc','hơi tiếc','không sao']),
    el('label',{for:'khohieu'},'Chỗ nào làm bạn khó hiểu nhất?'), el('textarea',{id:'khohieu'}),
    el('label',{for:'goiy'},'Gợi ý vừa rồi có giúp bạn chọn câu tương tự không — vì sao?'), el('textarea',{id:'goiy'}),
    el('label',{for:'nhanxet'},'Nhận xét khác của người thử (nguyên văn)'), el('textarea',{id:'nhanxet'}),
    el('label',{for:'quansat'},'Quan sát của người ghi (chỗ do dự, chỗ hiểu sai)'), el('textarea',{id:'quansat'}),
    el('div',{class:'row'},el('button',{class:'primary navy',onclick:()=>save(entered)},'Lưu phiên')), techBox());
}

async function save(entered){
  const tiec=document.querySelector('input[name=tiec]:checked')?.value||'';
  const F=S.loops[0]||{};  // vòng đầu → trường gốc (metric hieu_lai_tren_nguoi_thu); mọi vòng ở loops
  const body={tester:S.tester, entered_loop:entered, roots_tried:S.rootLog, root_wrong:F.rootWrong??null, attempt:F.attempt??null,
    reason:F.reason??null, reason_meta:F.reasonMeta??null, an_fix:F.anFix??null, an_fix_meta:F.anFixMeta??null, similar:F.similar??null, answer:F.answer??null, correct:F.correct??null, seconds:F.seconds??null,
    loops:S.loops,
    feedback:{tiec, kho_hieu:val('khohieu'), goi_y:val('goiy'), nhan_xet:val('nhanxet')}, observation:val('quansat'), calls:S.calls};
  const res=await post('/api/save',body);
  const row = entered ? ['| '+S.tester, F.rootWrong, F.attempt, F.reason||'(bỏ qua)', res.reason_group, F.similar||'—', F.answer||'—', F.correct===true?'đúng':(F.correct===false?'sai':'—'), F.seconds!=null?(F.seconds/60).toFixed(1):'—', ' |'].join(' | ')
                      : '| '+S.tester+' | không vào vòng |  |  |  |  |  |  |  |  |';
  if (!res.ok) { $app.append(el('p',{class:'err'},'Chưa lưu được: '+(res.error||'lỗi'))); return; }
  $app.replaceChildren(el('p',{class:'label'},'ĐÃ LƯU'), el('h2',{},'Phiên đã lưu: '+res.file),
    ...(res.on_host ? [el('p',{class:'err'},'Đang chạy trên Render: ổ đĩa bị xoá khi máy chủ khởi động lại. Bấm "Tải toàn bộ phiên" sau mỗi người thử và cuối buổi.')] : []),
    el('p',{class:'muted'},'Dòng để dán vào bảng "Kết quả vòng hỏi lại" trong validation/log.md:'), el('div',{class:'summary'},row),
    el('div',{class:'row'},el('button',{class:'primary navy',onclick:()=>location.reload()},'Phiên mới'), dlButton()), techBox());
}

groupHeader();
fetch('/api/config').then(r=>r.json()).then(d=>{ S.weak=d.weak||[]; S.minWords=d.min_explain_words||5; S.needCode=d.need_code; S.model=d.model; document.getElementById('model').textContent='model '+d.model; screenStart(); });
</script>
</body></html>
"""


def main():
    if ON_HOST and not PASSCODE:
        print("Đang chạy trên máy chủ công khai (có PORT) mà thiếu APP_PASSCODE — dừng để khỏi lộ key. "
              "Đặt biến môi trường APP_PASSCODE rồi chạy lại.", flush=True)
        return 1
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("Giao diện phiên thử: http://%s:%d  (model: %s · mã vào trang: %s · tối đa %d lượt/phút) — Ctrl+C để dừng"
          % (HOST, PORT, MODEL_NAME or MODEL_PROVIDER, "có" if PASSCODE else "không", MAX_CALLS), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
