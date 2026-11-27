"""Giao diện web cho buổi người dùng thử — chạy: python codebase/web.py  → mở http://127.0.0.1:8765

Chỉ thư viện chuẩn. Gọi đúng answer() trong agent.py (cùng input "attempt=…; ly_do=…; cau=…; tra_loi=…"
như bộ câu thử), nên hành vi giống hệt `python run.py` / `run.py eval`. Không sửa khung.

- Chỉ nghe trên 127.0.0.1 (máy người cầm máy). Người thử xem qua chia sẻ màn hình, đọc to lựa chọn.
- Đáp án câu gốc KHÔNG gửi xuống trình duyệt: máy chủ tự chấm câu gốc và tra mã lượt sai trong
  data/learner_states.json.
- Mỗi phiên lưu một file JSON ở validation/phien-thu/ (mã người thử U1…, không tên): câu gốc sai, mã lượt,
  lý do nguyên văn + nhóm lý do (đúng quy tắc tach_doan_voi_hieu), câu tương tự, đúng/sai, số giây,
  nhận xét, và tóm tắt trace (số lần gọi model, token) của từng bước.
"""
import json
import os
import sys
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tracing  # noqa: E402
from agent import answer  # noqa: E402
from ai import MODEL_PROVIDER, MODEL_NAME  # noqa: E402

PORT = 8765
# Thứ tự câu gốc theo validation/quy-trinh.md (Q1 → Q4 → Q5 → Q6). Muốn đổi thì sửa danh sách này.
ROOT_ORDER = ["Q1", "Q4", "Q5", "Q6"]
SAVE_DIR = os.path.join(ROOT, "validation", "phien-thu")
# Quy tắc "lý do yếu" chép từ eval/metric_spec.yaml (tach_doan_voi_hieu)
WEAK = {"ok", "oke", "k", "ko", "không", "k biết", "ko biết", "không biết", "?", "."}


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
    low = r.lower()
    if "đoán" in low or low in WEAK or len(r) <= 3:
        return "yếu"
    return "có lý do"


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

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        if self.path == "/api/roots":
            roots = [{"id": r["q"]["id"], "stem": r["q"]["stem"], "options": r["q"]["options"]} for r in _roots()]
            return self._send(200, {"roots": roots, "model": MODEL_NAME or MODEL_PROVIDER})
        self._send(404, {"error": "không có"})

    def do_POST(self):
        try:
            body = self._json()
        except Exception:
            return self._send(400, {"error": "JSON không hợp lệ"})
        if self.path == "/api/root_answer":
            return self._send(200, self.root_answer(body))
        if self.path == "/api/agent":
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
        body["model"] = MODEL_NAME or MODEL_PROVIDER
        body["saved_at"] = datetime.now().isoformat(timespec="seconds")
        os.makedirs(SAVE_DIR, exist_ok=True)
        path = os.path.join(SAVE_DIR, "%s-%s.json" % (tester, datetime.now().strftime("%Y%m%d-%H%M%S")))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(body, f, ensure_ascii=False, indent=2)
        return {"ok": True, "file": os.path.relpath(path, ROOT).replace(os.sep, "/"),
                "reason_group": body["reason_group"]}


PAGE = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Học từ lỗi — phiên thử</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;1,600&family=Be+Vietnam+Pro:wght@400;600;700&family=JetBrains+Mono&display=swap">
<style>
:root{--paper:#F3EFE6;--ink:#1C1B19;--red:#B3311E;--graphite:#645F56;--rule:#CBC3B3;--card:#FBF9F4;--ok:#1F6B45}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.55 'Be Vietnam Pro',Arial,sans-serif}
header{display:flex;justify-content:space-between;align-items:baseline;padding:18px 40px;border-bottom:1px solid var(--rule)}
header b{font-family:'Fraunces',Georgia,serif;font-size:22px}
header span{color:var(--graphite);font-size:15px}
main{max-width:920px;margin:0 auto;padding:36px 32px 80px}
h1{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:40px;line-height:1.15;margin:0 0 12px}
h2{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:28px;line-height:1.25;margin:0 0 16px}
.pen{color:var(--red);font-style:italic}
.muted{color:var(--graphite)}
.step{font-size:14px;letter-spacing:1px;color:var(--graphite);margin:0 0 8px}
.stem{font-size:22px;line-height:1.5;margin:0 0 20px}
.opts{display:flex;flex-direction:column;gap:10px}
button{font:inherit;cursor:pointer}
.opt{display:flex;gap:14px;align-items:flex-start;text-align:left;background:var(--card);border:1px solid var(--rule);padding:14px 18px;color:var(--ink)}
.opt:hover{border-color:var(--ink)}
.opt .k{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:20px;min-width:22px}
.opt[disabled]{cursor:default;opacity:.55}
.opt.picked{border-color:var(--ink);opacity:1;background:#fff}
.primary{background:var(--ink);color:var(--paper);border:0;padding:12px 22px;font-weight:600}
.ghost{background:none;border:1px solid var(--rule);padding:10px 18px;color:var(--ink)}
.row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:18px}
.msg{border-top:2px solid var(--ink);padding:16px 0 0;margin:28px 0 8px;font-size:20px}
.msg.ai{border-top:4px solid var(--red)}
.result-ok{color:var(--ok);font-weight:700}
.result-no{color:var(--red);font-weight:700}
textarea,input[type=text]{width:100%;font:inherit;padding:10px 12px;border:1px solid var(--rule);background:#fff}
textarea{min-height:84px}
label{display:block;font-weight:600;margin:18px 0 6px}
.radio{display:flex;gap:18px;flex-wrap:wrap}
.radio label{font-weight:400;margin:0;display:flex;gap:6px;align-items:center}
.timer{font-family:'JetBrains Mono',monospace;color:var(--graphite)}
details{margin-top:28px;color:var(--graphite);font-size:14px}
details pre{white-space:pre-wrap;font-family:'JetBrains Mono',monospace;font-size:13px;background:var(--card);padding:12px;border:1px solid var(--rule)}
.err{color:var(--red);font-weight:600}
.summary{background:var(--card);border:1px solid var(--rule);padding:18px;font-family:'JetBrains Mono',monospace;font-size:14px;white-space:pre-wrap}
</style></head>
<body>
<header><b>Học từ lỗi</b><span id="meta">Phiên thử · nhóm Zebra</span></header>
<main id="app"></main>
<script>
const $app = document.getElementById('app');
const S = {tester:'', roots:[], idx:0, rootLog:[], attempt:null, rootWrong:null, reason:null,
           similar:null, answer:null, correct:null, t0:null, seconds:null, calls:[], model:''};
const el = (tag, attrs={}, ...kids) => { const e=document.createElement(tag);
  for (const [k,v] of Object.entries(attrs)) { if (k==='class') e.className=v; else if (k.startsWith('on')) e.addEventListener(k.slice(2),v); else e.setAttribute(k,v); }
  for (const k of kids) e.append(k instanceof Node ? k : document.createTextNode(k)); return e; };
const post = (url, body) => fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(r=>r.json());
let tick=null;
function startTimer(){ S.t0=performance.now(); tick=setInterval(()=>{const t=document.getElementById('timer'); if(t) t.textContent=((performance.now()-S.t0)/1000).toFixed(0)+' giây';},500); }
function stopTimer(){ S.seconds=Math.round((performance.now()-S.t0)/100)/10; clearInterval(tick); }
function techBox(){ const d=el('details',{},el('summary',{},'Chi tiết kỹ thuật (cho người cầm máy)'));
  d.append(el('pre',{},S.calls.map(c=>'> '+c.input+'\n  buoc='+(c.result.buoc||'')+' ma_doan='+JSON.stringify(c.result.ma_doan||[])+' · gọi model '+c.trace.model_calls+' · token '+c.trace.tokens_in+'/'+c.trace.tokens_out+(c.error?'\n  LỖI: '+c.error:'')).join('\n'))); return d; }

function screenStart(){
  $app.replaceChildren(
    el('p',{class:'step'},'BẮT ĐẦU PHIÊN'),
    el('h1',{},'Thử công cụ, ', el('span',{class:'pen'},'không chấm bạn')),
    el('p',{class:'muted'},'Bạn trả lời vài câu ngắn. Sai là bình thường — thậm chí giúp nhóm hơn. Không ghi tên, không quay. Cứ nói to lựa chọn và nghĩ gì thì nói nấy.'),
    el('label',{for:'tester'},'Mã người thử (người cầm máy điền, vd U1)'),
    el('input',{type:'text',id:'tester',placeholder:'U1'}),
    el('div',{class:'row'}, el('button',{class:'primary',onclick:()=>{
      S.tester=(document.getElementById('tester').value||'').trim(); if(!S.tester){alert('Điền mã người thử, vd U1');return;}
      screenRoot(); }},'Bắt đầu')));
}

function screenRoot(){
  const r=S.roots[S.idx];
  const opts=el('div',{class:'opts'});
  for (const [k,v] of Object.entries(r.options)) {
    opts.append(el('button',{class:'opt',onclick:async (ev)=>{
      [...opts.children].forEach(b=>b.disabled=true); ev.currentTarget.classList.add('picked');
      const res=await post('/api/root_answer',{qid:r.id,chosen:k});
      if (res.error && !res.attempt) { $app.append(el('p',{class:'err'},res.error)); return; }
      S.rootLog.push({qid:r.id, chosen:k, correct:res.correct});
      if (res.correct) {
        $app.append(el('p',{class:'msg'},el('span',{class:'result-ok'},'Đúng. '),'Sang câu tiếp theo.'),
          el('div',{class:'row'},el('button',{class:'primary',onclick:()=>{ S.idx++; S.idx<S.roots.length?screenRoot():screenFeedback(false); }}, S.idx+1<S.roots.length?'Câu tiếp':'Hết câu — sang nhận xét')));
      } else { S.attempt=res.attempt; S.rootWrong=r.id+' (chọn '+k+')'; await askReason(); }
    }}, el('span',{class:'k'},k), el('span',{},v)));
  }
  $app.replaceChildren(el('p',{class:'step'},'CÂU GỐC '+(S.idx+1)+' / '+S.roots.length+' · '+r.id),
    el('p',{class:'stem'},r.stem), opts);
}

async function callAgent(text){ const c=await post('/api/agent',{text}); S.calls.push(c); return c; }

async function askReason(){
  const c=await callAgent('attempt='+S.attempt);
  startTimer();
  const box=el('div',{});
  const write=el('div',{style:'display:none'}, el('textarea',{id:'own',placeholder:'Gõ nguyên văn lời người thử'}),
    el('div',{class:'row'},el('button',{class:'primary',onclick:()=>chooseReason(document.getElementById('own').value)},'Gửi lý do')));
  const opts=el('div',{class:'opts'});
  for (const o of (c.result.lua_chon_ly_do||[])) {
    if (o.startsWith('Lý do khác')) opts.append(el('button',{class:'opt',onclick:()=>{write.style.display='block';}},el('span',{},o)));
    else opts.append(el('button',{class:'opt',onclick:()=>chooseReason(o)},el('span',{},o)));
  }
  box.append(el('p',{class:'msg ai'},c.error?el('span',{class:'err'},'Lỗi: '+c.error):(c.result.loi_nhan||'')), opts, write,
    el('div',{class:'row'},el('button',{class:'ghost',onclick:()=>chooseReason('')},'Bỏ qua bước này'),el('span',{class:'timer',id:'timer'},'0 giây')));
  $app.replaceChildren(el('p',{class:'step'},'VÌ SAO BẠN CHỌN VẬY?'), el('h2',{},'Câu vừa rồi chưa đúng — mình hỏi lại một chút'), box);
}

async function chooseReason(text){
  text=(text||'').replace(/[;\n\r]+/g,', ').trim();  // ';' là dấu ngăn khoá trong input của agent
  S.reason=text;
  $app.querySelectorAll('button').forEach(b=>b.disabled=true);
  const c=await callAgent('attempt='+S.attempt+'; ly_do='+text);
  const q=c.result.cau_tuong_tu;
  const parts=[el('p',{class:'step'},'GỢI Ý VÀ CÂU KIỂM LẠI'), el('p',{class:'msg ai'},c.error?el('span',{class:'err'},'Lỗi: '+c.error):(c.result.loi_nhan||''))];
  if (!q) { stopTimer(); parts.push(el('div',{class:'row'},el('button',{class:'primary',onclick:()=>screenFeedback(true)},'Sang nhận xét'))); $app.replaceChildren(...parts); return; }
  S.similar=q.id;
  const opts=el('div',{class:'opts'});
  for (const [k,v] of Object.entries(q.options)) opts.append(el('button',{class:'opt',onclick:(ev)=>{ [...opts.children].forEach(b=>b.disabled=true); ev.currentTarget.classList.add('picked'); grade(k); }}, el('span',{class:'k'},k), el('span',{},v)));
  parts.push(el('p',{class:'stem'},q.stem), opts, el('div',{class:'row'},el('span',{class:'timer',id:'timer'},'')));
  $app.replaceChildren(...parts);
}

async function grade(k){
  S.answer=k;
  const c=await callAgent('attempt='+S.attempt+'; ly_do='+S.reason+'; cau='+S.similar+'; tra_loi='+k);
  stopTimer(); S.correct=c.result.dung;
  $app.append(el('p',{class:'msg'}, S.correct?el('span',{class:'result-ok'},'Đúng. '):el('span',{class:'result-no'},'Chưa đúng. '), c.error?('Lỗi: '+c.error):(c.result.loi_nhan||'')),
    el('p',{class:'muted'},'Thời gian một vòng: '+S.seconds+' giây'),
    el('div',{class:'row'},el('button',{class:'primary',onclick:()=>screenFeedback(true)},'Sang nhận xét')));
}

function radio(name, values){ return el('div',{class:'radio'},...values.map(v=>el('label',{},el('input',{type:'radio',name,value:v}),v))); }
const val = id => (document.getElementById(id)?.value||'').trim();

function screenFeedback(entered){
  $app.replaceChildren(
    el('p',{class:'step'},'NHẬN XÉT SAU PHIÊN'),
    el('h2',{},entered?'Cảm ơn bạn — vài câu cuối':'Bạn đúng hết câu gốc — không vào vòng hỏi lại'),
    el('label',{},'Nếu mai không được dùng nữa, bạn thấy:'), radio('tiec',['rất tiếc','hơi tiếc','không sao']),
    el('label',{for:'khohieu'},'Chỗ nào làm bạn khó hiểu nhất?'), el('textarea',{id:'khohieu'}),
    el('label',{for:'goiy'},'Gợi ý vừa rồi có giúp bạn chọn câu tương tự không — vì sao?'), el('textarea',{id:'goiy'}),
    el('label',{for:'nhanxet'},'Nhận xét khác của người thử (nguyên văn)'), el('textarea',{id:'nhanxet'}),
    el('label',{for:'quansat'},'Quan sát của người ghi (chỗ do dự, chỗ hiểu sai)'), el('textarea',{id:'quansat'}),
    el('div',{class:'row'},el('button',{class:'primary',onclick:()=>save(entered)},'Lưu phiên')), techBox());
}

async function save(entered){
  const tiec=document.querySelector('input[name=tiec]:checked')?.value||'';
  const body={tester:S.tester, entered_loop:entered, roots_tried:S.rootLog, root_wrong:S.rootWrong, attempt:S.attempt,
    reason:S.reason, similar:S.similar, answer:S.answer, correct:S.correct, seconds:S.seconds,
    feedback:{tiec, kho_hieu:val('khohieu'), goi_y:val('goiy'), nhan_xet:val('nhanxet')}, observation:val('quansat'), calls:S.calls};
  const res=await post('/api/save',body);
  const row = entered ? ['| '+S.tester, S.rootWrong, S.attempt, S.reason||'(bỏ qua)', res.reason_group, S.similar||'—', S.answer||'—', S.correct===true?'đúng':(S.correct===false?'sai':'—'), S.seconds!=null?(S.seconds/60).toFixed(1):'—', ' |'].join(' | ')
                      : '| '+S.tester+' | không vào vòng |  |  |  |  |  |  |  |  |';
  $app.replaceChildren(el('p',{class:'step'},'ĐÃ LƯU'), el('h2',{},'Phiên đã lưu vào '+res.file),
    el('p',{class:'muted'},'Dòng để dán vào bảng "Kết quả vòng hỏi lại" trong validation/log.md:'), el('div',{class:'summary'},row),
    el('div',{class:'row'},el('button',{class:'primary',onclick:()=>location.reload()},'Phiên mới')), techBox());
}

fetch('/api/roots').then(r=>r.json()).then(d=>{ S.roots=d.roots; S.model=d.model; document.getElementById('meta').textContent='Phiên thử · nhóm Zebra · model '+d.model; screenStart(); });
</script>
</body></html>
"""


def main():
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print("Giao diện phiên thử: http://127.0.0.1:%d  (model: %s) — Ctrl+C để dừng" % (PORT, MODEL_NAME or MODEL_PROVIDER))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
