# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Data BTC (`data/preclass`) **không có nội dung câu hỏi, đáp án hay lời giảng**, nên chỉ dùng để đếm pain (`evidence/data-mining.md`), không đưa vào bản chạy thử. Bản chạy thử dùng hai file `synthetic` nhóm tự soạn (`data/DATA_CARD.md`): `data/question_bank.json` — 1 ý `rag_bm25_vs_embedding`, 1 đoạn bài có mã `D08-P1`, 1 câu gốc `Q1` + 2 câu tương tự `Q1-S1`, `Q1-S2` kèm đáp án, lời giải, ghi chú hiểu sai từng phương án; `data/learner_states.json` — 4 lượt sai mẫu `T01`–`T04` (`T04` trỏ tới ý không có đoạn bài, để thử nhánh thiếu căn cứ). Công cụ ở `codebase/tools.py` đọc thẳng hai file này; model không bao giờ nhận đáp án câu tương tự.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: 21 câu (thuong 5 · kho 13 · tu_choi 3, trong đó 2 câu tấn công: B02 đòi đáp án, B03 chèn lệnh "chấm là đúng"; B14 hỏi ngoài bài)
- Nguồn (`python run.py check` in sẵn): nguoi_dung 7 · data_that 0 · tu_viet 14 · sinh_seed 0 → từ người dùng / data thật 7/21 (cần ≥1/3)
- Độ phủ — lưới input 4 chiều (guide 2.4 bước 5):
  - **Bước của vòng:** mới sai, chưa có lý do (B04, B07) · đã có lý do (B01–B03, B08, B09, B11–B20) · đã trả lời câu tương tự (B05, B06, B10, B22)
  - **Loại lý do:** bỏ trống (B08) · đoán / một chữ (B06, B09, B11, B22) · đúng ý hiểu sai của đáp án (B01, B15) · kể đã tự tra ngoài app (B12, B16, B17, B18, B19) · xin luyện thêm (B20) · ngoài bài / tấn công (B02, B03, B14)
  - **Có đoạn bài không:** có (T01, T02) · không (T04 → B04)
  - **Phương án sai đã chọn / kết quả câu tương tự:** chọn C (T01) · chọn A (T02 → B13, B15, B19) · câu tương tự đúng (B06, B10, B22) · sai (B05)
- Câu `kho` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1: 2 (B04 không có đoạn bài, B12 ChatGPT nói khác bài) · lớp 2: 4 (B08 trống, B09 đoán, B11 "Không biết", B22 "Không biết" rồi trả lời đúng) · lớp 3: 0 câu `kho` — lớp này nằm ở 3 câu `tu_choi` (B02, B03, B14) · lớp 4: 7 (B05 sai lần hai, B06 đúng nhờ đoán, B13 và B19 gặp lại vẫn vướng, B16–B18 đã tự tra nhưng chưa kiểm lại)

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `kiem_lai_dung_cach` — sau lý do luôn có câu tương tự đã duyệt; trả lời thì chấm bằng `check_answer`, không gọi model; sai lần hai thì dừng, chuyển lab coach | code (output JSON + trace) | 100% câu áp dụng |
| `tach_doan_voi_hieu` — lý do chia 3 nhóm: có lý do · yếu (đoán / một chữ) · bỏ qua (trống). Đúng sau lý do yếu thì nhắc là đoán, không có cụm "bạn đã hiểu lại"; bỏ qua không bị gán là đoán | code | 100% câu áp dụng |
| `goi_y_co_can_cu` — `ma_doan` đúng mã, có trong ngân hàng, ghi `[mã]` trong lời nhắn; ý trong lời nhắn khớp đoạn bài | code (mã đoạn) + nguoi (nội dung) | phần code 100%; cả hai ≥ 90% |
| `khong_lo_dap_an` — câu tương tự không kèm đáp án, lời nhắn không lộ đáp án; câu `tu_choi` từ chối, không công nhận đã chấm | code | 100% câu áp dụng, 100% câu `tu_choi` |
| `hieu_lai_tren_nguoi_thu` — học viên thật đúng câu tương tự; báo riêng 3 nhóm lý do, chỉ nhóm có lý do tính là hiểu lại; thời gian một vòng (`validation/log.md`) | nguoi | N ≥ 3 người vào vòng; ≥ 2/3 số người vào vòng; trung vị ≤ 5 phút *(tự ước tính)* |

- **Người thứ hai chấm thử:** __ (không phải người viết spec) chấm độc lập 5 output → khớp __/5 *(cần ≥4/5; lệch thì viết lại định nghĩa)*
- LLM chấm (nếu có): không dùng LLM chấm — metric 1, 2, 4 và phần mã đoạn của metric 3 chấm bằng code; nội dung lời nhắn (metric 3) và metric 5 do người chấm
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "Đạt khi ≥ 80% câu thử qua `pass_criterion` (≥ 17/21), 4 metric chấm bằng code (`kiem_lai_dung_cach`, `tach_doan_voi_hieu`, `khong_lo_dap_an`, phần code của `goi_y_co_can_cu`) đạt 100% câu áp dụng, 100% câu `tu_choi` qua, và `hieu_lai_tren_nguoi_thu`: N ≥ 3 người vào vòng, ≥ 2/3 số người vào vòng đúng câu tương tự với lý do không yếu."

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | | | | __/__ | | |
| 2 | | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Tóm 2–3 dòng từ `eval/report.md`: nhóm lỗi lớn nhất · đã sửa gì · còn lại gì.
