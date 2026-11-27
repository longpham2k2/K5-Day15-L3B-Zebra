# Khảo sát — "Hiểu sai rồi thì sao?"

> Chép sang Google Form. **8 câu, 7 câu chỉ cần bấm, ~90 giây.** Không thu tên, email, mã học viên.
> Kiểm lại D2 ở [data-mining.md](../data-mining.md) (sai → đọc đáp án → đi tiếp, 1/399 luyện lại) trên cả người không dùng pre-class; câu 7 kiểm D1 (98,9% lời bạn học AI xen vào không được đáp lại).
> Ngưỡng R1: **≥20 người ngoài nhóm**, học viên khoá 5.

- Kênh gửi: __ (Discord / Zalo lớp nào)
- Giờ mở: __ · giờ chốt: __
- Người gửi: TV__

---

## Nội dung form

**Tiêu đề:** Hiểu sai rồi thì sao? — 90 giây

**Mô tả:** Nhóm L3B-Zebra đang tìm hiểu xem mọi người làm gì khi hiểu sai một ý trong khoá AI20K. Không có đúng / sai, không hỏi tên hay điểm. 7 câu bấm chọn + 1 câu tuỳ ý. Cảm ơn bạn!

| # | Câu hỏi | Kiểu | Lựa chọn |
|---|---|---|---|
| 1 | Bạn đang học lớp nào? | Chọn một · bắt buộc | L3A · L3B · L2A · L2B · Khác (không phải học viên) |
| 2 | Lần gần nhất bạn **trả lời sai hoặc nhận ra mình hiểu sai** một ý trong khoá là khi nào? | Chọn một · bắt buộc | Trong 3 ngày qua · Trong tuần này · Tuần trước · Lâu hơn · Không nhớ có lần nào |
| 3 | Lần đó bạn phát hiện mình sai nhờ đâu? | Chọn một · bắt buộc | Thấy đáp án quiz / câu ôn tập · Giảng viên / lab coach sửa · Code, lab chạy sai · Bạn cùng nhóm chỉ ra · Tự thấy khi học tiếp · Khác |
| 4 | Ngay sau đó bạn đã làm gì? | **Chọn nhiều** · bắt buộc | Đọc đáp án / lời giải rồi học tiếp · Xem lại slide / video · Hỏi ChatGPT / AI khác · Hỏi trợ giảng AI trên pre-class · Hỏi bạn / lab coach / giảng viên · Chưa làm gì, để sau · Khác |
| 5 | Sau đó, bạn có **kiểm lại** xem mình đã hiểu ý đó chưa không? (làm câu tương tự, giải thích lại cho ai, dùng lại trong lab…) | Chọn một · bắt buộc | Có, ngay hôm đó · Có, vài hôm sau · Chưa, nhưng thấy mình đã hiểu · Chưa, và vẫn chưa chắc |
| 6 | Trong 1 tháng qua, khoảng **mấy lần** bạn sai một ý mà không chắc mình đã hiểu lại? | Chọn một · bắt buộc | 0 · 1–2 · 3–5 · 6–10 · Trên 10 |
| 7 | Trên trang pre-class, khi một **bạn học AI** tự nói chen vào lúc bạn xem video, bạn thường… | Chọn một · bắt buộc | Mình chưa dùng pre-class · Có dùng nhưng không để ý thấy · Đọc rồi xem tiếp · Đọc và đôi khi trả lời · Thấy phiền, bỏ qua |
| 8 | *(Tuỳ ý)* Lần hiểu sai gần nhất đó là ý gì, và nó gây rắc rối gì cho bạn? | Đoạn văn · không bắt buộc | — |

**Cuối form (không bắt buộc):** Bạn có sẵn lòng cho nhóm hỏi thêm 10 phút không? Nếu có, để lại Discord / Zalo. *(Xoá cột này trước khi commit `results.csv`.)*

---

## Cách đọc kết quả — viết TRƯỚC khi mở form

- **Mẫu số:** người trả lời câu 1 là học viên (bỏ "Khác"). Câu 3–5 chỉ tính người **không** chọn "Không nhớ có lần nào" ở câu 2.
- **Số chính:** câu 5 = "Chưa, nhưng thấy mình đã hiểu" + "Chưa, và vẫn chưa chắc" → *sai rồi không kiểm lại*. Ghi x/N (%).
- **Mình đúng nếu thấy:** ≥50% người từng sai **không kiểm lại** (câu 5), **và** ≥30% chọn "Đọc đáp án / lời giải rồi học tiếp" hoặc "Chưa làm gì" ở câu 4 mà **không** chọn cách nào khác.
- **Ngược giả thuyết nếu:** đa số chọn "Có, ngay hôm đó" ở câu 5, hoặc câu 6 phần lớn là "0" → pain nhẹ, ghi đúng như vậy vào `summary.md`.
- **Câu 7:** chỉ tính người không chọn "Mình chưa dùng pre-class"; tỉ lệ "không để ý thấy" giúp phân biệt *không thấy* với *thấy mà không muốn đáp*.
- Câu 8: chép ≥3 câu nguyên văn (bỏ chi tiết nhận ra người) vào `summary.md` §3.
- Dưới 10 người: chỉ ghi x/n, không ghi %.
