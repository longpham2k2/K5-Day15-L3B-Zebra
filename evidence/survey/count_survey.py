"""Đếm khảo sát A4 từ evidence/survey/results.csv.

Chạy: python evidence/survey/count_survey.py [results.csv]
Mẫu số ghi cạnh mỗi số. Câu chọn nhiều: tổng có thể vượt 100%.
"""
import csv
import os
import sys
from collections import Counter

P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "results.csv")
rows = list(csv.DictReader(open(P, encoding="utf-8-sig", newline="")))
cols = list(rows[0].keys())
C = {k: next(c for c in cols if c.startswith(f"Câu {k}.")) for k in ("1", "2", "3", "4", "5", "6", "6b", "7", "8", "9", "10", "10b")}


def pct(x, n):
    return f"{x}/{n} ({100 * x / n:.0f}%)" if n >= 10 else f"{x}/{n}"


def multi(r, k):
    # Google Forms nối lựa chọn bằng ", " nhưng vài lựa chọn tự có dấu phẩy
    # ("Bỏ qua, chưa làm gì") → mảnh bắt đầu bằng chữ thường là phần tiếp của lựa chọn trước.
    out = []
    for x in (p.strip() for p in r[C[k]].split(",") if p.strip()):
        if out and x[0].islower():
            out[-1] += ", " + x
        else:
            out.append(x)
    return out


def show(title, sub, k, is_multi=False):
    c = Counter()
    for r in sub:
        for x in (multi(r, k) if is_multi else [r[C[k]].strip() or "(trống)"]):
            c[x] += 1
    print(f"\n{title} (n={len(sub)}{', chọn nhiều' if is_multi else ''})")
    for x, v in c.most_common():
        print(f"  {pct(v, len(sub))}  {x}")


hv = [r for r in rows if r[C["1"]].startswith("Học viên")]
print(f"Phản hồi: {len(rows)} · học viên: {len(hv)}")
show("Câu 1 · lớp", hv, "1")
show("Câu 2 · lần sai gần nhất", hv, "2")
err = [r for r in hv if not r[C["2"]].startswith("Không nhớ")]
recent = [r for r in err if r[C["2"]] in ("Hôm nay", "1–3 ngày trước", "4–7 ngày trước")]
print(f"  → có lần sai trong 7 ngày qua: {pct(len(recent), len(err))} (mẫu số: người không chọn 'Không nhớ')")
show("Câu 3 · ngay sau khi biết sai (mẫu số: người có lần sai)", err, "3", True)
only_passive = [r for r in err if set(multi(r, "3")) <= {"Đọc đáp án / lời giải rồi học tiếp", "Bỏ qua, chưa làm gì"}]
print(f"  → CHỈ đọc đáp án / bỏ qua, không làm gì khác: {pct(len(only_passive), len(err))}")
show("Câu 4 · có kiểm lại không (mẫu số: người có lần sai)", err, "4")
show("Câu 5 · lần đó mất gì", err, "5", True)
show("Câu 6 · ý đó có quay lại làm vướng", err, "6")
show("Câu 6b · lần vướng lại mất bao lâu (chỉ người 'lại vướng')", [r for r in err if r[C["6"]].startswith("Có, và mình lại vướng")], "6b")
show("Câu 7 · số lần / 7 ngày sai mà không chắc đã hiểu lại", hv, "7")
show("Câu 9 · số ngày dùng pre-class", hv, "9")
pc = [r for r in hv if r[C["9"]] in ("3–5 ngày", "Trên 5 ngày")]
show("Câu 10 · khi bạn học AI chen vào (chỉ người dùng pre-class ≥3 ngày)", pc, "10")
print("\nCâu 8 · nguyên văn:")
for r in hv:
    if r[C["8"]].strip():
        print(f"  {r['id']}: {r[C['8']].strip()}")
print("Câu 10b · nguyên văn:")
for r in hv:
    if r[C["10b"]].strip():
        print(f"  {r['id']}: {r[C['10b']].strip()}")
