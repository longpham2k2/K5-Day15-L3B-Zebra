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

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
