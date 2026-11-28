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

B01 ở lượt 1 chấm là 0 vì agent chọn sua_loi_ban nhưng tự giải thích luôn, thay vì yêu cầu người dùng chỉ cho An nhầm khiến học viên mất cơ hội để giải thích lại. Ở lượt 2, agent đã nhắc đúng ý sai và yêu cầu xem An đã nhầm ở đâu kèm gợi ý, tiếp tục đưa câu kiểm lại nên được chấm là 1. Học được rằng khi chấm cho sua_loi_ban cần đọc cả lời nhắn để xem agent có thực sự yêu cầu sửa hay không, hay tự đưa lời giải thích luôn, đảm bảo để cho học viên giải thích đúng theo mục tiêu của dự án.
