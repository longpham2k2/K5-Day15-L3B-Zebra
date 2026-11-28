# Reflection — Trần Trọng Đạt

## 1. Vai trò và phần việc làm

Chuẩn bị bộ benchmark, và metrics để đánh giá.    
Bổ sung và chỉnh [bộ benchmark](../eval/benchmark.csv), trong đó có các tình huống dựa trên hành vi ghi nhận qua khảo sát và phỏng vấn (`909977f`).  
Chấm độc lập 5 đầu ra mẫu rồi đối chiếu với Khoa trong [bảng chấm thử](../eval/cham-thu-nguoi-thu-hai.md) (`e24524d`).  
Chấm mù hai lượt benchmark theo `pass_criterion` của từng câu (`849b06c`, `4178f01`).

## 2. AI hỗ trợ

Codex để liệt kê câu thử, gợi ý các chỉ số phù hợp và đối chiếu nguồn của benchmark.  
Khi lọc câu thử, sửa lại câu chữ và đối chiếu thông tin cột `source`.
Claude hoàn thiện bản cuối của [metric spec](../eval/metric_spec.yaml) và giải thích từng chỉ số đo gì, dùng để đánh giá phần nào.  
Các phần được đề xuất và liệt kê đều được đọc và xác nhận lại.

## 3. Một câu thử trượt và điều học được

Câu B08 ở lượt chấm thứ 2, khi người dùng để trống lý do, thì hệ thống cho sang câu hỏi tương tự để xác nhận xem người dùng đã thực sự hiểu chưa thay vì yêu cầu hỏi lại lý do. Điều học được khi học viên bỏ qua lý do, hệ thống vẫn cần cho câu hỏi tương tự để tự kiểm lại, hệ thống vẫn ghi nhận câu đó nếu đúng nhưng chưa kết luận họ đã hiểu lại.
