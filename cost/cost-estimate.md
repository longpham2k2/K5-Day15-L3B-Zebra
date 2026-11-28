# Chi phí khi dùng thật

> CP4 · 14:30 Thứ Bảy 28/11/2026 · Ước tính tạm từ token API của lượt eval 2.

## 1. Đầu vào

- **Quy mô** gồm 220 tài khoản dùng pre-class ≥3 ngày, 436 học viên có hoạt động pre-class và 721 tài khoản tổng cộng. Nguồn là dữ liệu pre-class 05–25/11/2026. [Cách đếm](../evidence/data-mining.md) · [Script](../evidence/count.py)
- **Tần suất** dựa trên 20/25 người nhớ số lần trả lời sai mà chưa chắc đã hiểu lại trong 7 ngày. Quy đổi tuần → tháng bằng ×4 *(tự ước tính)*. [Khảo sát câu 7](../evidence/survey/results.csv)

| Persona | Số lần/tuần | Tỉ lệ | Phiên/người/tháng |
|---|---:|---:|---:|
| Ít (`it`) | 0–1 | 4/20 (20%) | 4 |
| Vừa (`vua`) | 2–3 | 13/20 (65%) | 10 |
| Nhiều (`nhieu`) | 4–6 | 3/20 (15%) | 20 |

Một vòng có 3 lượt gọi agent (hỏi lý do → gợi ý → chấm) và thực tế gọi model 1 lần. Khung lấy ngẫu nhiên 3 đầu vào thường/khó cho mỗi phiên, nên có thể gọi model nhiều hơn một vòng thực tế. Vì vậy, đây là ước tính dè dặt. [Cấu hình](personas.yaml)

| Model | USD/1 triệu token vào | USD/1 triệu token ra | Nguồn |
|---|---:|---:|---|
| `gpt-5.4-nano` | 0,20 | 1,25 | Tài liệu OpenAI, xem 28/11/2026. [Giá GPT-5.4 nano](https://developers.openai.com/api/docs/models/gpt-5.4-nano#pricing) |
| `gpt-5.4-mini` | 0,75 | 4,50 | Bảng BTC (`further-reading/model-prices.md` trong repo đề), xem 25/11/2026. [Đối chiếu giá OpenAI](https://developers.openai.com/api/docs/models/gpt-5.4-mini#pricing) |

## 2. Kết quả mô phỏng

Lượt `--try` đi hết 10 phiên ở chế độ giả. Máy chạy cần cấu hình OpenAI để đo token mới và sinh `cost/simulate-1.csv`. Bảng tạm dùng kế hoạch 50 phiên (seed 42), lấy token API và số lần gọi đã ghi cho từng đầu vào tương ứng trong lượt `run-2@20261128-095614`, rồi áp dụng công thức của khung. Token được đo trên `gpt-5.4-nano-2026-03-17` và quy giá theo cả hai model. Chi phí của mini có thể thay đổi khi đo token trực tiếp trên mini. [Lượt eval 2](../eval/run-2.csv)

| Model | USD/phiên | USD/task thành công | USD/tháng · 220 người | USD/tháng · 436 người | USD/tháng · 721 người | USD/người/tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `gpt-5.4-nano` | $0.00041 | Chờ chấm lượt 2 | $1.00 | $1.99 | $3.29 | $0.0046 |
| `gpt-5.4-mini` | $0.0015 | Chờ chấm lượt 2 | $3.72 | $7.36 | $12.18 | $0.0169 |

Khung tính chi phí/task thành công bằng chi phí trung bình mỗi phiên chia cho tỉ lệ đạt. Khi Long chấm xong lượt 2, chạy `python run.py simulate --rate-from eval/run-2.csv` để ghi kế tiếp sau lần đo chính thức và lấy số cho slide 6. Tỉ lệ đạt của lượt 2 đo trên nano. Cột chi phí cho mini khi đó chỉ là ước tính theo giá mini với cùng tỉ lệ đạt.

## 3. So với impact

- Impact ước tính khoảng 86 phút/người/tháng trong nhóm 69 học viên từng sai câu ôn tập (5.900 phút ÷ 69). Kịch bản chi phí cơ sở tính trên 436 học viên có hoạt động pre-class. [Đặc tả §2](../spec.md)
- Chi phí model ước tính ở kịch bản cơ sở là $0.0046/người/tháng với nano. Mức này phù hợp để chạy thử, còn quyết định mở rộng cần tỉ lệ đạt và thời gian tiết kiệm đo được.
