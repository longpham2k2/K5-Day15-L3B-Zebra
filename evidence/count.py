"""Đào data pre-class cho hướng A4 (lớp học kiểu mới).

Chạy:  python evidence/count.py <đường-dẫn-tới-data/preclass>
       (hoặc đặt biến môi trường PRECLASS_DIR)
Chỉ dùng thư viện chuẩn. Chỉ in số đã tổng hợp + vài mã dòng ví dụ (đã ẩn danh).
Mỗi số in kèm: đếm gì · mẫu số · lọc gì.
"""
import csv
import json
import os
import statistics as st
import sys
from collections import Counter, defaultdict

D = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PRECLASS_DIR", "data/preclass")


def rows(name):
    with open(os.path.join(D, name), encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def js(s):
    try:
        return json.loads(s) if s else {}
    except json.JSONDecodeError:
        return {}


def pct(x, n):
    return f"{x}/{n} ({100 * x / n:.1f}%)" if n else f"{x}/0 (-)"


def q(vals, ps=(25, 50, 75, 90)):
    vals = sorted(vals)
    if not vals:
        return "-"
    return " · ".join(f"p{p}={vals[min(len(vals) - 1, int(len(vals) * p / 100))]:g}" for p in ps)


def h(t):
    print(f"\n## {t}")


events = list(rows("events.csv"))
answers = list(rows("answers.csv"))
chat = list(rows("chat.csv"))
class_ev = list(rows("class_events.csv"))
rewards = list(rows("rewards.csv"))
learners = list(rows("learners.csv"))

active = {e["hv"] for e in events if e["actor"] == "learner" and e["hv"]}
print(f"Tài khoản: {len(learners)} · học viên có hoạt động (≥1 event actor=learner): {len(active)}")

# ---------------------------------------------------------------- 1. Bộ điều phối
h("1. Bộ điều phối quyết định (class_events, type=director_decided)")
dec = [js(e["data"]) for e in class_ev if e["type"] == "director_decided"]
ins = [d for d in dec if d.get("inserted")]
print("Đoạn bài giảng được quyết định:", len(dec), "· cho bạn học AI xen vào:", pct(len(ins), len(dec)))
print("Xen vào theo bạn học:", dict(Counter(d.get("classmate_id") for d in ins).most_common()))
print("Xen vào theo kiểu:", dict(Counter(d.get("intervention_type") for d in ins).most_common()))
print("expected_icap (lúc xen vào):", dict(Counter(d.get("expected_icap") for d in ins).most_common()))
print("lesson_phase (lúc xen vào):", dict(Counter(d.get("lesson_phase") for d in ins).most_common()))

# ---------------------------------------------------------------- 2. Lời xen vào và phản hồi
h("2. Lời bạn học AI xen vào → học viên có đáp lại không")
# Lượt tiếp xúc = cặp (hv, intervention_id) duy nhất từ agent_message_shown có intervention_id
# và agent_id là bạn học AI (không tính trợ giảng trả lời câu hỏi).
expo = {}
expo_agent = {}
for e in events:
    if e["type"] != "agent_message_shown":
        continue
    d = js(e["data"])
    iid, ag = d.get("intervention_id"), d.get("agent_id", "")
    if iid and ag.startswith("classmate"):
        k = (e["hv"], iid)
        expo.setdefault(k, e["occurred_at"])
        expo_agent[k] = ag
resp = set()
for c in chat:
    if c["intervention_id"]:
        resp.add((c["hv"], c["intervention_id"]))
for a in answers:
    if a["intervention_id"]:
        resp.add((a["hv"], a["intervention_id"]))
# Tab có đang hiện lúc lời xen vào hiện ra không (app_visibility_changed gần nhất trước đó)
import bisect
vis = defaultdict(list)
for e in events:
    if e["type"] == "app_visibility_changed":
        vis[e["hv"]].append((e["occurred_at"], js(e["data"]).get("visible")))
for v in vis.values():
    v.sort()
def hidden_at(hv, t):
    v = vis.get(hv, [])
    i = bisect.bisect_left(v, (t,)) - 1
    return i >= 0 and v[i][1] is False
answered_expo = {k for k in expo if k in resp}
exp_learners = {k[0] for k in expo}
resp_learners = {k[0] for k in answered_expo}
print("Lượt tiếp xúc (hv × intervention_id, bạn học AI):", len(expo))
print("  có đáp lại (chat/answers cùng hv + intervention_id):", pct(len(answered_expo), len(expo)))
print("  KHÔNG đáp lại:", pct(len(expo) - len(answered_expo), len(expo)))
print("Học viên từng thấy lời xen vào:", pct(len(exp_learners), len(active)), "(mẫu số = học viên có hoạt động)")
print("  trong đó từng đáp lại ≥1 lần:", pct(len(resp_learners), len(exp_learners)))
vis_expo = {k for k, t in expo.items() if not hidden_at(k[0], t)}
print("Lượt tiếp xúc lúc tab ĐANG HIỆN (loại lượt hiện ra khi tab ẩn):", pct(len(vis_expo), len(expo)))
print("  trong đó có đáp lại:", pct(len(vis_expo & answered_expo), len(vis_expo)))
by_ag = defaultdict(lambda: [0, 0])
for k, ag in expo_agent.items():
    by_ag[ag][0] += 1
    by_ag[ag][1] += k in resp
for ag, (n, r) in sorted(by_ag.items()):
    print(f"  {ag}: đáp lại {pct(r, n)}")
per_l = Counter(k[0] for k in expo)
print("Số lời xen vào mỗi học viên thấy:", q(per_l.values()))
print("Ví dụ lượt không đáp lại:", [f"{k[0]}·{k[1]}" for k in sorted(set(expo) - answered_expo)[:3]])

# ---------------------------------------------------------------- 3. Câu hỏi giữa video
h("3. Câu hỏi bật lên giữa video (quiz_item_opened / dismissed / answer_submitted video_quiz)")
opened = {}
for e in events:
    if e["type"] == "quiz_item_opened":
        d = js(e["data"])
        opened.setdefault((e["hv"], d.get("question_id")), e["occurred_at"])
skipped = set()
for e in events:
    if e["type"] == "quiz_item_dismissed":
        d = js(e["data"])
        if d.get("skipped_stop"):
            skipped.add((e["hv"], d.get("question_id")))
vq = [a for a in answers if a["nguon"] == "video_quiz"]
dis = [js(e["data"]) for e in events if e["type"] == "quiz_item_dismissed"]
print("Cặp (hv × câu) có câu hỏi bật lên:", len(opened), "· học viên:", len({k[0] for k in opened}))
print("Lượt đóng câu hỏi: bấm BỎ QUA (skipped_stop=true):", pct(sum(bool(d.get("skipped_stop")) for d in dis), len(dis)))
print("LƯU Ý: answers video_quiz chỉ có", len(vq), "dòng, ngày", sorted({a['created_at'][:10] for a in vq}),
      "→ loại câu này mới ghi từ 25/11, KHÔNG dùng để đo tỉ lệ trả lời / đúng câu giữa video.")
print("LƯU Ý: last_rate luôn = 1 và crossed_stop luôn = false trong bản này → không đo được tua nhanh / tua qua câu hỏi.")
seeks = [js(e["data"]) for e in events if e["type"] == "video_seeked" and e["actor"] == "learner"]
fwd = [x for x in seeks if isinstance(x.get("to"), (int, float)) and isinstance(x.get("from"), (int, float)) and x["to"] > x["from"]]
print("Lượt tua (video_seeked):", len(seeks), "· tua tới:", pct(len(fwd), len(seeks)))

# ---------------------------------------------------------------- 4. Trả lời đúng lần đầu
h("4. Đúng lần đầu (answers, lan_thu=1, was_correct không trống)")
first = [a for a in answers if a["lan_thu"] == "1" and a["was_correct"] in ("True", "False")]
for src in sorted({a["nguon"] for a in first}):
    s = [a for a in first if a["nguon"] == src]
    print(f"  {src}: đúng {pct(sum(a['was_correct'] == 'True' for a in s), len(s))}")
for flag in ("True", "False"):
    s = [a for a in first if a["du_doan"] == flag]
    print(f"  du_doan={flag}: đúng {pct(sum(a['was_correct'] == 'True' for a in s), len(s))}")
print("Phân bố số lần trả lời (mọi nguồn chấm đúng/sai):", dict(sorted(Counter(a["lan_thu"] for a in answers if a["was_correct"]).items(), key=lambda x: int(x[0] or 0))))

# Sai lần đầu → có làm lại cùng câu và đúng không
by_q = defaultdict(list)
for a in answers:
    if a["was_correct"] in ("True", "False"):
        by_q[(a["hv"], a["ref"])].append(a)
wrong1 = [k for k, v in by_q.items() if any(x["lan_thu"] == "1" and x["was_correct"] == "False" for x in v)]
retried = [k for k in wrong1 if any(x["lan_thu"] not in ("", "1") for x in by_q[k])]
fixed = [k for k in retried if any(x["lan_thu"] not in ("", "1") and x["was_correct"] == "True" for x in by_q[k])]
pp1 = [a for a in first if a["nguon"] == "pre_post_post"]
ppw = [a for a in pp1 if a["was_correct"] == "False"]
print("Ôn tập cuối ngày (pre_post_post) sai lần đầu:", pct(len(ppw), len(pp1)),
      "· trong số sai, thấy lời giải ngay (co_feedback):", pct(sum(a["co_feedback"] == "True" for a in ppw), len(ppw)))
from datetime import datetime
T = datetime.fromisoformat
chat_t = defaultdict(list)
for c in chat:
    chat_t[c["hv"]].append(T(c["asked_at"]))
after = sum(any(0 <= (t - T(a["created_at"])).total_seconds() <= 1800 for t in chat_t[a["hv"]]) for a in ppw)
print("  sai rồi nhắn AI (bất kỳ câu nào) trong 30 phút sau:", pct(after, len(ppw)))
by_kc = defaultdict(list)
for a in answers:
    if a["was_correct"] in ("True", "False"):
        by_kc[(a["hv"], a["kc_code"])].append(a)
try_kc = fix_kc = 0
for a in ppw:
    nxt = [b for b in by_kc[(a["hv"], a["kc_code"])] if b["created_at"] > a["created_at"] and b["ref"] != a["ref"]]
    try_kc += bool(nxt)
    fix_kc += any(b["was_correct"] == "True" for b in nxt)
print("  sai rồi sau đó làm câu KHÁC cùng kc_code:", pct(try_kc, len(ppw)), "· và đúng:", pct(fix_kc, len(ppw)))
print("  ví dụ dòng sai:", [a["id"] for a in ppw[:5]])
pq = defaultdict(lambda: [0, 0])
for a in pp1:
    pq[a["ref"]][0] += 1
    pq[a["ref"]][1] += a["was_correct"] == "False"
print("  câu ôn tập sai nhiều nhất (n≥20):")
for r, n, k in sorted([(v[1] / v[0], v[0], k) for k, v in pq.items() if v[0] >= 20], reverse=True)[:5]:
    print(f"     {k}: sai {round(r * n)}/{n} ({r:.0%})")
print("Sai lần đầu:", len(wrong1), "· có làm lại:", pct(len(retried), len(wrong1)), "· làm lại rồi đúng:", pct(len(fixed), len(wrong1)))

# Thời gian trả lời (answer_submitted.answered_after_ms) — đoán nhanh?
ms = defaultdict(list)
fast = defaultdict(lambda: [0, 0, 0])  # n, nhanh<3s, nhanh&đúng
for e in events:
    if e["type"] != "answer_submitted":
        continue
    d = js(e["data"])
    t = d.get("answered_after_ms")
    if not isinstance(t, (int, float)) or d.get("lan_thu") != 1:
        continue
    src = d.get("nguon")
    ms[src].append(round(t / 1000, 1))
    fast[src][0] += 1
    if t < 3000:
        fast[src][1] += 1
        fast[src][2] += bool(d.get("correct"))
for src, v in ms.items():
    n, f, fc = fast[src]
    print(f"  {src}: giây tới lúc trả lời {q(v)} · trả lời <3s {pct(f, n)} · trong số <3s đúng {pct(fc, f)}")

# ---------------------------------------------------------------- 5. Độ sâu khi viết
h("5. Độ sâu khi học viên viết (chat, giai_thich, rubric)")
lens = [int(c["do_dai_cau_hoi"]) for c in chat if c["do_dai_cau_hoi"].isdigit()]
print("Lượt chat:", len(chat), "· độ dài câu nhắn (ký tự):", q(lens), "· ≤15 ký tự:", pct(sum(x <= 15 for x in lens), len(lens)))
print("Chat theo kênh:", dict(Counter(c["channel"] for c in chat).most_common()))
print("Chat theo kiểu:", dict(Counter(c["kind"] for c in chat).most_common()))
print("Chat nhắn tới:", dict(Counter(c["addressed_agent_id"] for c in chat).most_common()))
rep = [c for c in chat if c["intervention_id"]]
rl = [int(c["do_dai_cau_hoi"]) for c in rep if c["do_dai_cau_hoi"].isdigit()]
print("Câu đáp lại lời xen vào:", len(rep), "· độ dài:", q(rl), "· ≤15 ký tự:", pct(sum(x <= 15 for x in rl), len(rl)))
graded = [a for a in answers if a["nguon"] == "chat" and a["trang_thai_cham"] == "da_cham"]
for col in ("rubric_bam_bai", "rubric_y_moi", "rubric_dung_ngu_canh"):
    c = Counter(a[col] for a in graded if a[col] != "")
    n = sum(c.values())
    print(f"  {col} (chat đã chấm, n={n}):", {k: pct(v, n) for k, v in sorted(c.items())})
gt = [a for a in answers if a["nguon"] == "giai_thich"]
gl = [int(a["do_dai_noi_dung"]) for a in gt if a["do_dai_noi_dung"].isdigit()]
print("Tự giải thích (giai_thich):", len(gt), "dòng ·", len({a['hv'] for a in gt}), "học viên · độ dài:", q(gl), "· ≤15 ký tự:", pct(sum(x <= 15 for x in gl), len(gl)))
print("  trạng thái chấm:", dict(Counter(a["trang_thai_cham"] for a in gt)))
ts = [js(e["data"]) for e in events if e["type"] == "text_submitted"]
print("text_submitted có dán chữ:", pct(sum((t.get("paste_count") or 0) > 0 for t in ts), len(ts)))

# ---------------------------------------------------------------- 6. Điểm thưởng
h("6. Điểm thưởng (rewards)")
print("Theo hành vi:", dict(Counter(r["hanh_vi"] for r in rewards)))
aid = {a["id"]: a for a in answers}
dd = [aid[r["evidence_id"]] for r in rewards if r["hanh_vi"] == "du_doan" and r["evidence_id"] in aid]
print("LƯU Ý: mọi câu du_doan đều ở thuc_hanh và đều was_correct=True → không đo được 'đoán đúng/sai'.")
print("Thưởng du_doan mà câu đó trả lời SAI:", pct(sum(a["was_correct"] == "False" for a in dd), len(dd)))

# ---------------------------------------------------------------- 7. So sánh (tương quan)
h("7. Có đáp lại bạn học AI vs không — đúng lần đầu (tương quan, KHÔNG phải nhân quả)")
grp = {"co_dap_lai": resp_learners, "thay_nhung_khong_dap": exp_learners - resp_learners}
for g, S in grp.items():
    s = [a for a in first if a["hv"] in S]
    print(f"  {g} ({len(S)} hv): đúng lần đầu {pct(sum(a['was_correct'] == 'True' for a in s), len(s))}")
    for src in ("video_quiz", "pre_post_post"):
        s2 = [a for a in s if a["nguon"] == src]
        print(f"     {src}: {pct(sum(a['was_correct'] == 'True' for a in s2), len(s2))}")

# ---------------------------------------------------------------- 8. Phễu
h("8. Phễu học viên (mẫu số = học viên có hoạt động)")
def who(t):
    return {e["hv"] for e in events if e["type"] == t}
steps = [
    ("mở video", who("video_opened")),
    ("thấy câu hỏi giữa video", {k[0] for k in opened}),
    ("thấy bạn học AI xen vào", exp_learners),
    ("nhắn AI ≥1 lần", {c["hv"] for c in chat}),
    ("đáp lại bạn học AI ≥1 lần", resp_learners),
    ("tự giải thích ≥1 lần", {a["hv"] for a in gt}),
    ("mở Sổ hiểu bài", who("so_hieu_bai_opened")),
]
for name, S in steps:
    print(f"  {name}: {pct(len(S & active), len(active))}")

# ---------------------------------------------------------------- 9. Độ phủ
h("9. Số ngày có dùng pre-class (ngày giờ Việt Nam, mẫu số = mọi tài khoản)")
from datetime import timedelta
days = defaultdict(set)
for e in events:
    if e["actor"] == "learner" and e["hv"]:
        days[e["hv"]].add((datetime.fromisoformat(e["occurred_at"]) + timedelta(hours=7)).date())
for k in (1, 2, 3, 5, 8):
    print(f"  dùng ≥{k} ngày: {pct(sum(len(v) >= k for v in days.values()), len(learners))}")
print(f"  chưa từng dùng: {pct(len(learners) - len(days), len(learners))}")
