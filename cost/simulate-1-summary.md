# Tóm tắt mô phỏng simulate-1@20261128-131843

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| it | 9 | 3 | 1026 | 69 | 0.9 | 7.1 |
| vua | 33 | 3 | 1364 | 101 | 1.2 | 7.8 |
| nhieu | 8 | 3 | 2018 | 127 | 1.8 | 8.1 |

Tỉ lệ đạt dùng để tính: 21/21 (100%) — lượt run-2@20261128-095614

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (220 người) | Chi phí / tháng — cơ sở (436 người) | Chi phí / tháng — cao (721 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.4-nano (vào 0.2 · ra 1.25 $/1M) | $0.00041 | $0.00041 | $0.00014 | $0.9924 | $1.97 | $3.25 | $0.0045 |
| gpt-5.4-mini (vào 0.75 · ra 4.5 $/1M) | $0.0015 | $0.0015 | $0.00050 | $3.68 | $7.29 | $12.05 | $0.0167 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (3.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5.4-nano-2026-03-17. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
