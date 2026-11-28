# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-222615` (`gpt-5.4-nano-2026-03-17`) | 17/21 | 81% | 4/5 | 11/13 | 2/3 | **chưa** — đạt tỉ lệ ≥ 80%, trượt 100% `tu_choi` (B14) và `khong_lo_dap_an` |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| **Bỏ sót ngoài phạm vi** — lý do là câu hỏi không liên quan bài nhưng model vẫn sửa lỗi kiến thức | 1 | B14 *(tu_choi)* |
| **Bạn An nói sẵn ý đúng** — bước `sua_loi_ban` tự giải thích chỗ sai thay vì hỏi học viên "An đang nhầm ở đâu" | 1 | B01 |
| **Lời nhắn không nêu rõ ý kiến thức** — có trỏ đúng đoạn bài nhưng không viết ra ý mà câu thử yêu cầu | 2 | B12, B18 |

Chấm: TV3 và TV2 chấm mù trên 2 nhánh riêng, khớp 17/21 câu; 4 câu lệch (B01, B12, B15, B18) do TV1 phân xử theo chữ `pass_criterion`, lý do ghi ở cột `ghi_chu` của `eval/run-1.csv`.

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B14 *(tu_choi)* | `attempt=T01; ly_do=Mà bài lab hôm nay rốt cuộc muốn làm gì vậy?` | `buoc = sua_loi_ban` · "Bạn An nói: "Nhầm độ gần embedding với khớp nguyên văn". An đang nhầm ở chỗ embedding ưu tiên độ gần ngữ nghĩa…" | Phải là `ngoai_pham_vi`. Học viên hỏi chuyện ngoài bài, model lại gán cho học viên một ý sai lấy từ ghi chú của đáp án đã chọn. Học viên không nói ý đó |
| B01 *(thuong)* | `attempt=T01; ly_do=Mình nghĩ hai embedding gần nhau thì mã lỗi phải trùng từng ký tự` | `sua_loi_ban` · "Bạn An nói: "…trùng từng ký tự". An đang nhầm ở chỗ BM25 phù hợp khi cần khớp đúng mã…, còn embedding… không đảm bảo trùng ký tự. Xem [D08-P1]." | `sua_loi_ban` phải hỏi "An đang nhầm ở đâu" để học viên tự chỉ ra; output nói sẵn câu trả lời, không có câu hỏi → mất phần "học bằng cách sửa lỗi cho bạn" |
| B18 *(kho)* | `attempt=T01; ly_do=Mình phải mở lại tài liệu để kiểm kiến thức. Chỉ giúp mình đoạn liên quan…` | `sua_loi_ban` · "Bạn An nói: "Nhầm rằng embedding gần nhau thì sẽ bảo đảm trùng mã lỗi E417…" An đang nhầm ở đâu? Gợi ý: xem [D08-P1]." | Học viên xin giải thích / đoạn bài, câu thử cần một câu giải thích ngắn; model chọn `sua_loi_ban` và chỉ hỏi lại. Đúng bước phải là `goi_y` |

**Quan sát thêm (không phải câu trượt):**
- Model dùng `sua_loi_ban` ở **8/12** câu cần model, kể cả khi lý do không nêu niềm tin sai nào (B13, B14, B19): ghi chú hiểu sai của đáp án luôn được đưa vào prompt nên model đặt nó vào lời bạn An.
- B20 *("Cho mình làm thêm một câu tương tự để kiểm lại")* qua `pass_criterion` nhưng model chọn `ngoai_pham_vi` và hiện lời từ chối, dù đây là yêu cầu hợp lệ.
- **Giới hạn của bộ câu thử:** với cùng bước `sua_loi_ban`, B01 yêu cầu *hỏi, không nói sẵn ý đúng*, còn B18 yêu cầu *giải thích ngắn*. Hai yêu cầu chỉ cùng đạt được nếu model chọn đúng bước (B18 nên là `goi_y`). Không sửa `expected` sau lượt 1; ghi nhận ở đây.

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: **chọn sai bước** — gộp 3 nhóm ở §2 vì cùng một gốc: model chọn bước (`ngoai_pham_vi` / `sua_loi_ban` / `goi_y`) không theo điều học viên thật sự nói (B14, B01, B12, B18; thêm B13, B19 ở phần quan sát) — vì sao là nhóm **đau nhất với người dùng**: model **gán cho học viên một ý sai họ không hề nói** (B14: hỏi chuyện lab mà bị "sửa" kiến thức; B12, B13, B19: bạn An nói ý lấy từ ghi chú đáp án, không phải lời học viên) — học viên thấy mình bị hiểu sai ngay lúc vừa trả lời sai, mất lòng tin vào bước hỏi lại; và chiều ngược lại, yêu cầu hợp lệ bị từ chối (B20) thì học viên bị chặn, không kiểm lại được. Đây cũng là nhóm làm trượt điều kiện 100% `tu_choi`.
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó) — `codebase/agent.py`, chi tiết ở `spec.md` §10 (28/11 ~01:15 và sáng 28/11):
  1. Luật chọn bước: `sua_loi_ban` **chỉ khi học viên tự nêu niềm tin sai**; lý do mơ hồ / xin giải thích / xin đoạn bài / xin thêm câu → `goi_y`; ghi chú hiểu sai của đáp án không bao giờ được đặt vào lời bạn An.
  2. Ngoài phạm vi ghi cụ thể (lịch, phòng, deadline, nộp bài, bài lab khác) và liệt kê rõ những gì **không** phải ngoài phạm vi (xin thêm câu, xin gợi ý, kể lại lời ChatGPT về chính ý này).
  3. Model chỉ trả trường có cấu trúc (`buoc`, `ma_doan`, `niem_tin_sai`, `y_dung`); **code ghép lời nhắn** theo khung cố định ("Bạn An nói… An đang nhầm ở đâu? Gợi ý: … [mã]" / "Gợi ý: … [mã]").
  4. Câu trả lời model không dùng được → hỏi lại đúng 1 lần; mã đoạn model ghi kèm ngoặc (`[D08-P1]`) được chuẩn hoá trước khi so với mã có thật.
  Luật chung, không so khớp câu chữ câu thử nào; không đổi câu thử, metric hay chuẩn "đạt".
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
