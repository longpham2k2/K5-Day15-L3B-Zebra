# Nội dung slide — bản nháp trang 1–3

> Nguồn số: `evidence/summary.md`, `spec.md` §1, §2, §4 (bản trên `main` lúc 27/11 23:48). Mỗi trang ≥1 số có nguồn (luật `slides/outline.md`).
> Mỗi trang: **tiêu đề = một câu kết luận**, 3–4 dòng chữ, 1 hình. Phần "Lời nói" là để người trình bày đọc, không đưa lên slide.
> *(Bản nháp do coding agent soạn từ các file trên; Khoa duyệt, chốt chữ trước khi dựng slide.)*

---

## Trang 0 · Bìa

- **Học từ lỗi: hỏi lại ngay sau câu sai**
- Nhóm Zebra · L3B · Track A4 — Lớp học kiểu mới
- Long · Đạt · Khoa · Huy

---

## Trang 1 · Người dùng & pain

**Tiêu đề:** Sai một câu, học viên tự tra lại mất thời gian — mà vẫn không biết chắc mình đã hiểu.

**Người dùng:** học viên AI20K khoá 5 đang làm build phase, vừa trả lời sai một câu kiểm tra.

| Số | Nguồn |
|---|---|
| **19/23 (83%)** mất thời gian tìm lại tài liệu / hỏi lại sau khi sai | Khảo sát n = 25, câu 5 |
| **16/23 (70%)** hỏi ChatGPT / AI ngoài ngay sau khi sai | Khảo sát, câu 3 |
| **7/23 (30%)** bị chính ý đó quay lại làm vướng — phần lớn mất 16–30 phút | Khảo sát, câu 6, 6b |
| Làm lại câu sai trong app: **2/424 (0,5%)** — mỗi ý chỉ có 1 câu, không có câu thứ hai để kiểm | Data pre-class, `count.py` |

**Trích dẫn (chọn 1):** *"mất cả buổi chiều để xem hiểu là rốt quộc bài lab muốn làm gì"* — khảo sát R21

**Hình:** 3 cột số lớn (83% · 70% · 30%) + câu trích ở dưới.

**Lời nói (~40 giây):** "Học viên khoá 5 không lười — sau khi sai, gần như ai cũng làm gì đó: 70% hỏi ChatGPT, 61% xem lại slide. Vấn đề là việc đó tốn thời gian — 83% nói vậy — và kết thúc bằng cảm giác 'chắc là hiểu rồi'. Gần một phần ba bị chính ý đó quay lại làm vướng ở buổi sau hay lúc làm lab. Trong app cũng không có cách kiểm: mỗi ý chỉ có một câu, và chỉ 2 trên 424 câu sai được làm lại."

**Ghi chú cho người nói — đừng nói quá:** phỏng vấn 3 học viên chỉ 1/3 gặp pain một phần (P4); P1, P5 tự xoay xở được. Nếu bị hỏi: "người có thời gian thì tự kiểm được; người ít thời gian thì không — đó là người dùng của mình."

---

## Trang 2 · Vì sao chọn bài này

**Tiêu đề:** Chọn "học từ lỗi" vì có người gặp thật, có số đo được, và làm kịp trong 2 ngày.

| Hướng | Gặp | Impact / tháng | Chọn? |
|---|---|---|---|
| **H1 · Hỏi lại ngay sau câu sai** | 69 học viên từng sai câu ôn tập | **≈ 99 giờ / tháng / khoá** *(tự ước tính)* | ✅ |
| H2 · Làm lời bạn học AI xen vào được đáp lại | 273 học viên thấy lời xen vào | chưa đo được | ❌ đáp lại không làm học tốt hơn rõ (85,1% vs 82,4% đúng lần đầu) |
| H3 · Kéo học viên dùng pre-class nhiều hơn | 285/721 chưa từng dùng | — | ❌ bài toán độ phủ, không phải "hiểu sâu hơn" |

**Cách tính 99 giờ** (dòng chữ nhỏ dưới bảng): 69 người × ~13 lần sai / tháng × ~6,6 phút vướng lại / lần — số người và số lần từ data pre-class, số phút từ khảo sát câu 6–6b; quy đổi và điểm giữa khoảng là *tự ước tính*; **chưa tính** thời gian tự tra lại ngay sau khi sai → con số thấp hơn thực tế.

**Hình:** bảng 3 dòng, dòng H1 tô đậm.

**Lời nói (~30 giây):** "Bọn mình cân ba hướng. Hướng làm bạn học AI được đáp lại nhiều hơn nghe hấp dẫn — 98,9% lời xen vào bị bỏ qua — nhưng data cho thấy người có đáp lại cũng không học tốt hơn rõ. Nên bọn mình chọn chỗ có thiệt hại đo được: khoảng 99 giờ một tháng cho một khoá, và đó là mức thấp."

---

## Trang 3 · Giải pháp

**Tiêu đề:** Một vòng ngắn ngay sau câu sai: hỏi lý do → gợi ý có căn cứ → một câu cùng ý, chấm bằng đáp án.

**Lát cắt một câu:** Một học viên vừa trả lời sai một câu ôn tập, AI chọn cách hỏi lại (gợi ý đúng chỗ hay để học viên sửa lỗi cho một bạn học AI) dựa trên đáp án đã chọn và đoạn bài liên quan, và học viên trả lời đúng một câu tương tự cùng ý.

**Sơ đồ (rút gọn từ `spec.md` §4):**
```
Sai câu gốc → hỏi lý do (lấy từ ghi chú hiểu sai) → [AI chọn: gợi ý / sửa lỗi bạn học / ngoài phạm vi, kèm mã đoạn]
           → câu tương tự đã duyệt → chấm bằng đáp án (không dùng AI) → đúng: xong · sai: lời giải + hỏi lab coach
```

**AI tự làm đến đâu:** AI chỉ quyết định **1 chỗ** — chọn bước tiếp và viết lời nhắn. Mọi thứ khác là code:
- Gợi ý **phải có mã đoạn bài** — không có căn cứ thì nói rõ, chuyển lab coach.
- AI **không thấy đáp án** câu tương tự, **không chấm** — chấm bằng đáp án đã duyệt.
- Lý do trống / một chữ / "Mình đoán" → code bỏ chẩn đoán, sang thẳng câu tương tự; đúng nhờ đoán thì **không** nói "đã hiểu".

**Vì sao:** dạy sai kiến thức là đắt nhất — học viên mang hiểu sai vào lab.

**Khác ChatGPT ở đâu:** bắt đầu từ **đúng đáp án học viên đã chọn** (không phải tự mô tả lỗi) · chỉ nói trong đoạn bài của khoá · **kết thúc bằng một câu kiểm, chấm theo đáp án** — biết chắc thay vì "có thể hiểu".

**Hình:** sơ đồ 5 ô ngang; ô "AI" tô màu khác để thấy AI chỉ ở 1 chỗ.

**Lời nói (~45 giây):** "Giải pháp là một vòng ngắn ngay sau câu sai… AI chỉ quyết định một chỗ; chấm đúng sai là code so với đáp án đã duyệt, nên AI không thể nói 'bạn đúng rồi' khi bạn sai, cũng không lộ đáp án."
