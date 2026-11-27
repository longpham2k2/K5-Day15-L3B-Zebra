# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

> 🚧 **Bản nháp — cập nhật 27/11/2026 ~16:50.** Khảo sát mới có **12 phản hồi (chưa chốt, cần ≥20)**; các thành viên khác còn đang tìm người phỏng vấn. Số và kết luận dưới đây **có thể đổi** khi thêm nguồn.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ *(theo tự soát — chờ cả nhóm duyệt)* | `evidence/data-mining.md` · `evidence/count.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ 3 học viên khoá 5 (P1, P4, P5) · thêm 2 người ngoài khoá (P2, P3) không tính | `evidence/interviews/P1.md`… `P5.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ **12/20**, đang thu · form 2 (câu hỏi khác) n = 2, ghi riêng | `evidence/survey/results.csv` · `evidence/survey/count_survey.py` · `evidence/survey/form-2/` |

## 2. Số chính

- **Đào data** (pre-class, 05–25/11/2026, 436 học viên có hoạt động):
  - Câu ôn tập cuối ngày sai lần đầu: 399/1.968 (20,3%); 399/399 thấy lời giải ngay.
  - Câu sai lần đầu được làm lại chính câu đó: 2/424 (0,5%). Mỗi ý kiến thức chỉ có 1 câu ôn tập (156 ý · 156 câu) → app không có câu thứ hai cùng ý để kiểm lại.
  - Lời bạn học AI xen vào không được đáp lại: 7.903/7.992 (98,9%); bộ điều phối chỉ cho xen vào trong lúc giảng (385/385).
  - Chat của học viên không có ý riêng (`rubric_y_moi = 0`): 909/1.223 (74,3%).
  - Độ phủ: 220/721 (30,5%) tài khoản dùng pre-class ≥3 ngày; 77/436 (17,7%) học viên có hoạt động từng làm câu ôn tập.
- **Phỏng vấn** (học viên khoá 5): **1/3 gặp pain một phần** (P4), 2/3 không (P1, P5) · số lần / tháng: P1 không có lần nào nhận ra · P4 không đưa số · P5 "nhiều lúc", không đưa số · mỗi lần mất: P4 ~30 phút để nhớ lại kiến thức buổi trước; P1, P5 không hỏi / không có.
- **Khảo sát** (bản lưu giữa chừng 27/11 16:34, n = 12 học viên khoá 5: 7 L3A, 5 L3B; đếm bằng `count_survey.py`). Câu 3–6 tính trên 11 người có một lần sai cụ thể (bỏ 1 người "Không nhớ"):
  - Lần sai gần nhất trong 7 ngày qua: **10/11 (91%)**.
  - **Chưa kiểm lại** xem đã hiểu chưa: **6/11 (55%)** · có, ngay trong ngày 3/11 · có, vài ngày sau 1/11 · không nhớ 1/11.
  - Ngay sau khi sai *(chọn nhiều)*: hỏi ChatGPT / AI ngoài 8/11 · đọc đáp án rồi học tiếp 7/11 · xem lại slide / video 7/11 · hỏi người 5/11 · hỏi trợ giảng AI của khoá 4/11 · làm thêm câu tương tự 2/11 · **chỉ đọc đáp án / bỏ qua mà không làm gì khác: 0/11**.
  - Lần đó mất gì *(chọn nhiều)*: **mất thời gian tìm lại tài liệu / hỏi lại 8/11 (73%)** · làm lab / bài tập sai phải sửa 5/11 · không mất gì đáng kể 3/11.
  - Ý đó quay lại làm vướng: 4/11 · quay lại nhưng đã nắm 4/11 · chưa gặp lại 3/11. Lần vướng lại mất (n = 4): 5–15 phút 1 · 16–30 phút 2 · trên 30 phút 1.
  - Số lần / 7 ngày sai mà không chắc đã hiểu lại (n = 12): 2–3 lần 6 · 4–6 lần 1 · 1 lần 1 · không nhớ 4.
  - Người dùng pre-class ≥3 ngày: 4/12; khi bạn học AI chen vào (n = 4): lướt qua 2 · không để ý 2 · **trả lời 0**.
  - Form 2 (TV2, 10 câu khác, n = 2): cả 2 "chỉ đọc hoặc xem lại lời giải", mất thêm 15–30 phút, 3–5 lần / 7 ngày chuyển bài khi chưa chắc hiểu — ghi riêng, không cộng.

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
8. Câu ôn tập sai, đã thấy lời giải, không làm lại: `A00611` (`d01-on-chatbot-la-ung-dung`), `A00288`, `A02467`, `A01030`, `A00887` — data `answers.csv`
9. Lời bạn học AI xen vào không được đáp lại: `L0006` · `program-day01:ai-llm-foundation:module-1:chunk-4:director` — data `events.csv`

## 4. Các nguồn có khớp nhau không

*(Tạm — khảo sát mới 12/20.)*

- **Khớp:**
  - "Sai rồi không kiểm lại": data — làm lại câu sai 2/424, app không có câu thứ hai cùng ý · khảo sát — **6/11 chưa kiểm lại**.
  - "Bạn học AI chen vào bị bỏ qua": data 98,9% không đáp · khảo sát 0/4 trả lời.
  - "Tốn thời gian lấy lại": P4 ~30 phút · khảo sát 8/11 mất thời gian tìm lại / hỏi lại, lần vướng lại phần lớn 16–30 phút.
- **Lệch:**
  - Data thấy học viên đọc lời giải rồi đi tiếp **trong app**; khảo sát và phỏng vấn cho thấy **không ai chỉ dừng ở đó** (0/11) — họ xoay xở **ngoài app**: ChatGPT (8/11), slide, hỏi người. Data không thấy phần này.
  - Phỏng vấn: 2/3 không gặp pain (P1, P5 có cách tự kiểm riêng); khảo sát: 55% chưa kiểm lại. Có thể do mẫu phỏng vấn nhỏ và đều qua quen biết của TV1, hoặc người chăm (P5) tự kiểm được còn người ít thời gian thì không (P4).
- **Diễn giải tạm:** pain không phải "không làm gì sau khi sai", mà là **tự xoay xở tốn thời gian và vẫn không chắc đã hiểu**: tra ChatGPT, mở lại tài liệu, hỏi lại — rồi hơn nửa số người không kiểm lại.

## 5. Kết luận

*(Tạm, chờ khảo sát đủ 20 và phỏng vấn thêm.)* Giả thuyết ở `evidence/hypothesis.md`: **phải đổi.**
- Phần **đúng**: lời bạn học AI xen vào gần như không được đáp lại (data 98,9%, khảo sát 0/4); hơn nửa số người sai không kiểm lại (khảo sát 6/11).
- Phần **sai**: học viên **không** thụ động sau khi sai — ai cũng làm gì đó (0/11 chỉ đọc đáp án / bỏ qua); họ không bỏ qua câu hỏi giữa video (data 1%); đáp lại bạn học AI không đi kèm học tốt hơn rõ (85,1% vs 82,4%).
- **Pain sau khi đổi:** sau khi sai, học viên tự tra (ChatGPT, tài liệu, hỏi người) — tốn thời gian (8/11) — nhưng **không có cách nhanh để kiểm xem mình đã hiểu đúng chưa**, nên hơn nửa bỏ bước kiểm và một phần bị vướng lại về sau (4/11, phần lớn 16–30 phút).
- **Lưu ý cách đánh giá:** khảo sát **không có ngưỡng "đúng nếu" viết trước khi mở form** đã commit; ngưỡng viết trước duy nhất là ở `hypothesis.md` (dựa trên data). Các số khảo sát ở trên chỉ mô tả, chưa so với ngưỡng định sẵn.
- **Điều vẫn chưa biết:** con số khi đủ ≥20 phản hồi; bao nhiêu phút mỗi tuần cho việc tự kiểm lại; người "chưa kiểm lại" là vì không có thời gian hay vì nghĩ mình đã hiểu.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| Học viên L3A, khoá 5 (P1) | 27/11 11:07 | ✅ |
| Học viên L2, khoá 5 (P4) | 27/11 11:45 | ✅ |
| Học viên L3A, khoá 5 (P5) | 27/11 13:53 | ✅ |
| *(các thành viên khác đang tìm thêm)* | | |
