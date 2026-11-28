# Chi phí khi dùng thật

> CP4 · 14:30 Thứ Bảy 28/11/2026 · Lượt mô phỏng chính thức `simulate-1@20261128-131843`.

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

Lượt chính thức **`simulate-1@20261128-131843`**: 50 phiên (seed 42) chạy qua bản chạy thử thật, token lấy từ `usage` của API, **0/50 phiên lỗi**. Tỉ lệ đạt lấy từ lượt eval 2 (`--rate-from eval/run-2.csv`): 21/21. Số chép từ [`simulate-1-summary.md`](simulate-1-summary.md) (không sửa tay) · dữ liệu từng phiên: [`simulate-1.csv`](simulate-1.csv).

| Persona | Số phiên | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên |
|---|---:|---:|---:|---:|---:|
| Ít (`it`) | 9 | 3 | 1.026 | 69 | 0,9 |
| Vừa (`vua`) | 33 | 3 | 1.364 | 101 | 1,2 |
| Nhiều (`nhieu`) | 8 | 3 | 2.018 | 127 | 1,8 |

| Model | USD / phiên | **USD / task thành công** | USD / tháng · thấp 220 người | USD / tháng · **cơ sở 436 người** | USD / tháng · cao 721 người | USD / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| **`gpt-5.4-nano`** (model đang dùng) | $0,00041 | **$0,00041** | $0,99 | **$1,97** | $3,25 | $0,0045 |
| `gpt-5.4-mini` | $0,0015 | $0,0015 | $3,68 | $7,29 | $12,05 | $0,0167 |

- Token **đo trên `gpt-5.4-nano-2026-03-17`**; dòng `gpt-5.4-mini` là **giá mini áp lên token đo trên nano** (chưa đo trực tiếp trên mini) — số thật của mini có thể lệch.
- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Tỉ lệ đạt 21/21 là **một lượt** trên model có dao động giữa các lần gọi (lượt 1: 17/21) → nếu tỉ lệ đạt thật là 81% như lượt 1, chi phí / task thành công nano ≈ $0,00051 — vẫn cùng bậc.
- Mô phỏng rút ngẫu nhiên 3 đầu vào / phiên nên gọi model 0,9–1,8 lần / phiên, trong khi một vòng thật gọi model 1 lần → ước tính **dè dặt** (cao hơn thực tế).
- Chi phí chỉ tính lời gọi model; chưa tính máy chủ (bản thử chạy trên máy nhóm / gói Render miễn phí).

## 3. So với impact

- Impact ước tính khoảng 86 phút/người/tháng trong nhóm 69 học viên từng sai câu ôn tập (5.900 phút ÷ 69). Kịch bản chi phí cơ sở tính trên 436 học viên có hoạt động pre-class. [Đặc tả §2](../spec.md)
- Chi phí model ở kịch bản cơ sở: **$1,97 / tháng cho 436 học viên ($0,0045 / người / tháng)** với `gpt-5.4-nano`; cả kịch bản cao (721 người) dùng `gpt-5.4-mini` cũng chỉ ~$12 / tháng. So với ~86 phút / người / tháng tự kiểm lại *(tự ước tính, spec §2)*, chi phí model không phải điểm nghẽn.
- Điểm nghẽn để quyết định mở rộng là **hiệu quả học đo trên người thật** (metric `hieu_lai_tren_nguoi_thu`, `validation/log.md`) chứ không phải tiền model.
