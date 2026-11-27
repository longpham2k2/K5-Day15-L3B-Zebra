# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

> 🚧 **Bản nháp — cập nhật 27/11/2026 ~17:40.** Khảo sát **24 phản hồi (bản lưu 3, form vẫn mở, chốt sáng 28/11)**. Số và kết luận dưới đây **có thể đổi** khi chốt khảo sát hoặc thêm nguồn.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ *(theo tự soát — chờ cả nhóm duyệt)* | `evidence/data-mining.md` · `evidence/count.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ 3 học viên khoá 5 (P1, P4, P5) · thêm 2 người ngoài khoá (P2, P3) không tính | `evidence/interviews/P1.md`… `P5.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ **24/20** (24/24 học viên ngoài nhóm — nhóm xác nhận không thành viên nào trả lời; 9/24 là L3B), form vẫn mở · form 2 (câu hỏi khác) n = 2, ghi riêng | `evidence/survey/results.csv` · `evidence/survey/count_survey.py` · `evidence/survey/form-2/` |

## 2. Số chính

- **Đào data** (pre-class, 05–25/11/2026, 436 học viên có hoạt động):
  - Câu ôn tập cuối ngày sai lần đầu: 399/1.968 (20,3%); 399/399 thấy lời giải ngay.
  - Câu sai lần đầu được làm lại chính câu đó: 2/424 (0,5%). Mỗi ý kiến thức chỉ có 1 câu ôn tập (156 ý · 156 câu) → app không có câu thứ hai cùng ý để kiểm lại.
  - Lời bạn học AI xen vào không được đáp lại: 7.903/7.992 (98,9%); bộ điều phối chỉ cho xen vào trong lúc giảng (385/385).
  - Chat của học viên không có ý riêng (`rubric_y_moi = 0`): 909/1.223 (74,3%).
  - Độ phủ: 220/721 (30,5%) tài khoản dùng pre-class ≥3 ngày; 77/436 (17,7%) học viên có hoạt động từng làm câu ôn tập.
- **Phỏng vấn** (học viên khoá 5): **1/3 gặp pain một phần** (P4), 2/3 không (P1, P5) · số lần / tháng: P1 không có lần nào nhận ra · P4 không đưa số · P5 "nhiều lúc", không đưa số · mỗi lần mất: P4 ~30 phút để nhớ lại kiến thức buổi trước; P1, P5 không hỏi / không có.
- **Khảo sát** (bản lưu 3, 27/11 17:24, n = 24 học viên khoá 5: 15 L3A, 9 L3B; đếm bằng `count_survey.py`). Câu 3–6 tính trên 23 người có một lần sai cụ thể (bỏ 1 người "Không nhớ"):
  - Lần sai gần nhất trong 7 ngày qua: **21/23 (91%)**.
  - Có kiểm lại xem đã hiểu chưa: **có, ngay trong ngày 12/23 (52%)** · có, vài ngày sau 2/23 · **chưa kiểm lại 7/23 (30%)** · không nhớ 2/23.
  - Ngay sau khi sai *(chọn nhiều)*: hỏi ChatGPT / AI ngoài 16/23 (70%) · xem lại slide / video 14/23 · đọc đáp án rồi học tiếp 13/23 · hỏi người 8/23 · hỏi trợ giảng AI của khoá 7/23 · làm thêm câu tương tự 2/23 · **chỉ đọc đáp án / bỏ qua mà không làm gì khác: 2/23 (9%)**.
  - Lần đó mất gì *(chọn nhiều)*: **mất thời gian tìm lại tài liệu / hỏi lại 19/23 (83%)** · làm lab / bài tập sai phải sửa 7/23 · bài nhóm chậm / sai 5/23 · bị hỏi trên lớp không trả lời được 3/23 · không mất gì đáng kể 5/23.
  - Ý đó quay lại làm vướng: **7/23 (30%)** · quay lại nhưng đã nắm 11/23 · chưa gặp lại 5/23. Lần vướng lại mất (n = 7): 5–15 phút 2 · 16–30 phút 4 · trên 30 phút 1.
  - Số lần / 7 ngày sai mà không chắc đã hiểu lại (n = 24): 0 lần 1 · 1 lần 3 · 2–3 lần 12 · 4–6 lần 3 · không nhớ 5.
  - Người dùng pre-class ≥3 ngày: 9/24; khi bạn học AI chen vào (n = 9): lướt qua 5 · không để ý 2 · đọc nhưng không trả lời 2 · **trả lời 0**.
  - Form 2 (TV2, 10 câu khác, n = 2): cả 2 "chỉ đọc hoặc xem lại lời giải", mất thêm 15–30 phút — ghi riêng, không cộng.

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
5. "Mất công hỏi lại, và tốn thời gian tìm tài liệu rồi chắt lọc đúng thông tin cần tìm" — khảo sát R07, câu 8
6. "tốn thời gian check lại kiến thức và lại phải mở lại tài liệu" — khảo sát R09, câu 8
7. "Tốn công và token để check lại việc cần làm đã đạt tiêu chí hay chưa" — khảo sát R05, câu 8
7b. "mất cả buổi chiều để xem hiểu là rốt quộc bài lab muốn làm gì, trong khi code rất nhiều, và nội dung kiến thức cũng nhiều" — khảo sát R21, câu 8
8. Câu ôn tập sai, đã thấy lời giải, không làm lại: `A00611` (`d01-on-chatbot-la-ung-dung`), `A00288`, `A02467`, `A01030`, `A00887` — data `answers.csv`
9. Lời bạn học AI xen vào không được đáp lại: `L0006` · `program-day01:ai-llm-foundation:module-1:chunk-4:director` — data `events.csv`

## 4. Các nguồn có khớp nhau không

*(Tạm — khảo sát n = 24, chưa chốt.)*

- **Khớp:**
  - "Bạn học AI chen vào bị bỏ qua": data 98,9% không đáp · khảo sát **0/9** người dùng pre-class ≥3 ngày trả lời.
  - "Kiểm lại tốn thời gian": khảo sát **19/23 (83%)** mất thời gian tìm lại / hỏi lại; 7/23 bị vướng lại, phần lớn 16–30 phút · P4 ~30 phút · R21 "mất cả buổi chiều".
  - "Học viên không thụ động": khảo sát chỉ 2/23 chỉ đọc đáp án / bỏ qua · phỏng vấn P1, P5 tự tra · data không thấy phần này vì nó xảy ra ngoài app.
- **Lệch:**
  - **Data** gợi ý "sai rồi không kiểm lại" (làm lại câu sai 2/424, app không có câu cùng ý); **khảo sát** cho thấy đa số **có** kiểm lại — 14/23 (61%) ngay trong ngày hoặc vài ngày sau, chỉ 7/23 (30%) chưa kiểm. Lý do lệch: data chỉ thấy hành vi **trong app**; việc kiểm lại diễn ra **ngoài app** (ChatGPT 16/23, slide 14/23, hỏi người 8/23).
  - Ở n = 12, số "chưa kiểm lại" là 6/11 (55%); thêm 12 người thì còn 30% → kết luận từ mẫu nhỏ không bền, ghi lại để không lặp lỗi này.

## 5. Kết luận

*(Tạm, chờ khảo sát chốt.)* Giả thuyết ở `evidence/hypothesis.md`: **phải đổi.**
- **Đúng:** lời bạn học AI xen vào gần như không được đáp lại (data 98,9%, khảo sát 0/9).
- **Sai:** học viên **không** thụ động sau khi sai và **phần lớn có kiểm lại** (61%); họ không bỏ qua câu hỏi giữa video (data 1%); đáp lại bạn học AI không đi kèm học tốt hơn rõ (85,1% vs 82,4%).
- **Pain sau khi đổi:** sau khi sai, học viên phải **tự xoay xở để kiểm lại** — hỏi ChatGPT, mở lại slide, hỏi người — và việc đó **tốn thời gian (83%)**; dù vậy 30% vẫn bị vướng lại ý đó về sau, phần lớn mất 16–30 phút. Thứ thiếu không phải ý muốn kiểm lại, mà là **một cách kiểm nhanh, đúng chỗ mình sai, có đáp án để biết chắc**.
- **Lưu ý cách đánh giá:** khảo sát **không có ngưỡng "đúng nếu" viết trước khi mở form** đã commit; ngưỡng viết trước duy nhất là ở `hypothesis.md` (dựa trên data). Các số khảo sát ở trên chỉ mô tả.
- **Điều vẫn chưa biết:** mỗi lần tự kiểm lại mất bao nhiêu phút (khảo sát không hỏi); người "chưa kiểm lại" là vì không có thời gian hay vì nghĩ mình đã hiểu.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3A, khoá 5 (P1) | 27/11 11:07 | ✅ |
| Học viên L2, khoá 5 (P4) | 27/11 11:45 | ✅ |
| Học viên L3A, khoá 5 (P5) | 27/11 13:53 | ✅ |
| *(các thành viên khác đang tìm thêm)* | | |
