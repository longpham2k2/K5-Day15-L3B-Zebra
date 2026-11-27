# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

> 🚧 **Bản nháp — cập nhật 27/11/2026 ~14:15.** Chưa có kết quả khảo sát; các thành viên khác còn đang tìm người phỏng vấn. Số và kết luận dưới đây **có thể đổi** khi thêm nguồn.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ *(theo tự soát — chờ cả nhóm duyệt)* | `evidence/data-mining.md` · `evidence/count.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ 3 học viên khoá 5 (P1, P4, P5) · thêm 2 người ngoài khoá (P2, P3) không tính | `evidence/interviews/P1.md`… `P5.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ đang thu | `evidence/survey/` |

## 2. Số chính

- **Đào data** (pre-class, 05–25/11/2026, 436 học viên có hoạt động):
  - Câu ôn tập cuối ngày sai lần đầu: 399/1.968 (20,3%); 399/399 thấy lời giải ngay.
  - Câu sai lần đầu được làm lại chính câu đó: 2/424 (0,5%). Mỗi ý kiến thức chỉ có 1 câu ôn tập (156 ý · 156 câu) → app không có câu thứ hai cùng ý để kiểm lại.
  - Lời bạn học AI xen vào không được đáp lại: 7.903/7.992 (98,9%); bộ điều phối chỉ cho xen vào trong lúc giảng (385/385).
  - Chat của học viên không có ý riêng (`rubric_y_moi = 0`): 909/1.223 (74,3%).
  - Độ phủ: 220/721 (30,5%) tài khoản dùng pre-class ≥3 ngày; 77/436 (17,7%) học viên có hoạt động từng làm câu ôn tập.
- **Phỏng vấn** (học viên khoá 5): **1/3 gặp pain một phần** (P4), 2/3 không (P1, P5) · số lần / tháng: P1 không có lần nào nhận ra · P4 không đưa số · P5 "nhiều lúc", không đưa số · mỗi lần mất: P4 ~30 phút để nhớ lại kiến thức buổi trước; P1, P5 không hỏi / không có.
- **Khảo sát:** n = __ · __/__ (__%) … *(chờ kết quả)*

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung. Người ngoài khoá (P2, P3) ghi riêng, không cộng.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Học viên L3A, khoá 5 | Không — không nhận ra lần hiểu sai nào | không có *(dùng ChatGPT giảng lại ~4 lần)* | không hỏi | Hỏi ChatGPT giảng lại |
| P4 | Học viên L2, khoá 5 | Một phần — "chưa kịp hiểu", quên kiến thức buổi trước | không đưa số | ~30 phút (nhớ lại kiến thức buổi trước) | Sửa theo hướng dẫn · xem lại slide · hỏi người khác |
| P5 | Học viên L3A, khoá 5 | Không — hiểu sai "nhiều lúc" nhưng tự phát hiện, tự sửa | "nhiều lúc", không đưa số | không hỏi | Tra mạng + hỏi AI → ghi chép → làm lab |
| *P2* | *Ngoài khoá — không tính* | *Một phần* | *~2 lần* | *15 phút học lại khi quên* | *ChatGPT, giải thích cho bạn, áp dụng* |
| *P3* | *Ngoài khoá — không tính* | *Không* | *2 lần* | *2 ngày để nắm lại* | *Thực hành lại, hỏi bạn nhóm, hỏi lại lab coach* |

**Cách chọn mẫu phỏng vấn:** 3 học viên khoá 5 (2 L3A, 1 L2; không có L3B), tìm qua quen biết của TV1, phỏng vấn qua tin nhắn ngày 27/11. Một số câu có gợi ý sẵn lựa chọn hoặc là câu đóng — đánh dấu ⚠️ trong từng file.

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "Kiến thức nhiều với chiều thực hành luôn ạ" · "Chưa kịp hiểu ạ" — P4
2. "Xem lại slides với hỏi ai ạ" *(khi quên kiến thức buổi trước, mất ~30 phút)* — P4
3. "Đa số mình toàn ghi chép lại, nên nếu có quên thì mình mở vở coi lại" — P5
4. "Có chuẩn bị méo gì đâu. Làm build phase còn chưa xong." — P1
5. Câu ôn tập sai, đã thấy lời giải, không làm lại: `A00611` (`d01-on-chatbot-la-ung-dung`), `A00288`, `A02467`, `A01030`, `A00887` — data `answers.csv`
6. Lời bạn học AI xen vào không được đáp lại: `L0006` · `program-day01:ai-llm-foundation:module-1:chunk-4:director` — data `events.csv`

## 4. Các nguồn có khớp nhau không

*(Tạm, chờ khảo sát.)* **Data nói** học viên trên pre-class sai rồi đọc lời giải và đi tiếp, gần như không làm lại (2/424), và app không có câu thứ hai cùng ý để kiểm lại. **Người dùng nói** hiểu sai là chuyện thường (P4, P5), nhưng người có thời gian **tự kiểm ở ngoài app** — tra mạng, hỏi ChatGPT, ghi chép, làm lab (P5, P1) — còn người không có thời gian thì "chưa kịp hiểu" và quên, mất ~30 phút nhớ lại (P4).

**Lệch ở đâu, vì sao:** data chỉ thấy hành vi **trong app**; việc kiểm lại xảy ra **ngoài app** (ChatGPT, vở ghi, lab, hỏi người) nên data không thấy. Data có thể đang phóng đại pain "không ai kiểm lại", còn phỏng vấn cho thấy pain có thể chỉ nặng ở nhóm ít thời gian. Ngoài ra 2/3 người được hỏi không dùng pre-class, nên phỏng vấn và data không cùng một nhóm người.

## 5. Kết luận

*(Tạm, chờ khảo sát và phỏng vấn thêm.)* Giả thuyết ở `evidence/hypothesis.md`: **đang nghiêng về "phải đổi"** — vì phỏng vấn chưa xác nhận "sai rồi không kiểm lại" ở mọi học viên (1/3 một phần); pain có vẻ hẹp hơn: học viên **ít thời gian** không kịp hiểu và quên, mất thời gian lấy lại. Điều vẫn chưa biết: bao nhiêu học viên khoá 5 "sai rồi không kiểm lại" và "lại vướng" ý đó về sau, mỗi lần mất bao lâu (khảo sát câu 5, 6, 6b, 7).

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3A, khoá 5 (P1) | 27/11 11:07 | ✅ |
| Học viên L2, khoá 5 (P4) | 27/11 11:45 | ✅ |
| Học viên L3A, khoá 5 (P5) | 27/11 13:53 | ✅ |
| *(các thành viên khác đang tìm thêm)* | | |
