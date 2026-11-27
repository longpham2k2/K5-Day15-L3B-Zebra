# Người dùng thử *(bonus)*

> Điền ở guide bước 4.3 — 2–3 người ngoài nhóm, ~10 phút / người, theo 5 nhịp: làm quen · bối cảnh · giao việc · quan sát · hỏi sau. Ôn lại: ngày 5, ngày 13. Chấm ở rubric Bonus.
> Không ghi tên: ghi vai. Hành vi quan sát được nặng hơn lời nói; toàn lời khen = phiên chưa đạt, giao việc khó hơn.
> Người dùng thử **không thay được** bằng chứng pain ở `evidence/`.

## Lịch hẹn người dùng thử (chỉ ghi vai và giờ, không tên)

> Cũng là nơi đo metric `hieu_lai_tren_nguoi_thu` (`eval/metric_spec.yaml`): cần **≥ 3 học viên khoá 5 ngoài nhóm vào được vòng** hỏi lại (sai một câu gốc). Người làm đúng hết câu gốc ghi "không vào vòng", không tính vào N.
> **Khung giờ chung (Long chốt 27/11 ~22:25):** 28/11 **10:30–12:30**, sau CP3 10:00 — để còn kịp ghi kết quả và đưa vào slide trước CP4 14:30. Hẹn **4–5 người** để chắc có ≥ 3 người vào vòng.
> **Cách chạy online:** người thử đọc to lựa chọn (câu gốc, lý do, câu tương tự); người trong nhóm gõ input vào `python run.py` và chia sẻ màn hình; không quay. Bấm giờ từ lúc agent hỏi lý do tới lúc có kết quả chấm câu tương tự.

| # | Vai | Từ đâu | Ai hẹn | Giờ hẹn | Hình thức | Ai cầm máy / ghi | Đã xong? |
|---|---|---|---|---|---|---|---|
| U1 | Học viên L3A, khoá 5 | Khảo sát — tự để lại liên hệ ở câu 11 | Khoa | 28/11, giờ cụ thể: __ (đã hẹn trong 10:00–13:00 — **cần báo lại khung mới 10:30–12:30**) | Online · chia sẻ màn hình, không quay; người thử để lại nhận xét bằng lời / chữ | __ / __ | Chưa |
| U2 | __ | __ | Long | __ | __ | __ / __ | Chưa |
| U3 | __ | __ | Long | __ | __ | __ / __ | Chưa |
| U4 | __ | __ | __ | __ | __ | __ / __ | Chưa hẹn |
| U5 | __ | __ | __ | __ | __ | __ / __ | Chưa hẹn |

Cách chạy từng người: [quy-trinh.md](quy-trinh.md).

## Kết quả vòng hỏi lại (metric `hieu_lai_tren_nguoi_thu`)

Model dùng: OpenAI `gpt-5.4-nano` (cùng model với eval lượt 1, lượt 2) · máy cầm: __ · chạy bằng `python codebase/web.py`, mỗi phiên lưu ở `validation/phien-thu/`

| # | Câu gốc sai (lựa chọn) | Mã lượt | Lý do (nguyên văn) | Nhóm lý do (có lý do / yếu / bỏ qua) | Câu tương tự | Trả lời | Đúng? | Thời gian (phút) | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| U1 | | | | | | | | | |
| U2 | | | | | | | | | |
| U3 | | | | | | | | | |
| U4 | | | | | | | | | |
| U5 | | | | | | | | | |

Người đúng cả 3 câu gốc: ghi "không vào vòng" ở cột "Câu gốc sai", để trống các cột còn lại.

**Tổng kết:** N (vào vòng) = __ · đúng với **có lý do** __/N · đúng với **yếu (đoán)** __ · đúng với **bỏ qua** __ · trung vị thời gian __ phút → **đạt / chưa đạt** (cần N ≥ 3, có lý do ≥ 2/3 N, trung vị ≤ 5 phút).

## Quan sát (bonus)

| Người thử (vai) | Việc giao (theo kết quả, không theo nút) | Quan sát (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai) | Trích nguyên văn | Mức nghiêm trọng (cao / vừa / thấp) |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

Câu hỏi sau: *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* → __ / __ / __

## Tổng hợp

- Chủ đề lặp nhiều nhất: __
- Sửa gì trước demo (ghi `spec.md` §10): __
- Giữ gì và vì sao: __
- Để dành sau: __
