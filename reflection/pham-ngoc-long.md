# Reflection — Phạm Ngọc Long

1. Vai trò + phần mình làm: 
Đội trưởng (TV1). 
- Chốt bài toán A4 và kịch bản phỏng vấn (4e14dce)
- Tự phỏng vấn P1–P5 (fde1549, 3a7e766) 
- Đổi giả thuyết theo bằng chứng, tổng hợp ở evidence/summary.md (af379bb, 2fa50bd, f3b0939) 
- Viết spec / canvas (c8c590d, fc3081c) và chốt chuẩn "đạt" §7 trước CP2 (c47fc6c)
- Luồng agent workflow 1 bước AI (b870bfe, 034c306) và bản sửa cho lượt 2 (897db42)
- Chạy lượt 1 và phân xử 4 câu lệch (646618c, 487f503)
- Giao diện buổi thử bản 2 (5aebafe)
- Chạy lượt 2 + mô phỏng chi phí (2ef7fdd, c854311)
- Tự chạy buổi người dùng thử U1–U4 (c2d5ebd, c854311, f97b4bd)
- Nộp các checkpoint.

2. AI hỗ trợ mình thế nào: 
Dùng Claude Code cho gần như mọi việc viết: 
- Script đếm data và khảo sát, nháp spec / summary / báo cáo, code agent và giao diện. 
- Chỗ phải sửa lại output AI: 
    + Mốc so sánh "1/399" sai, vì mỗi ý chỉ có 1 câu ôn tập nên không thể có câu làm lại. 
    + Một dòng changelog AI ghi sai lý do; kết luận "55% chưa kiểm lại" ở n = 12 không bền (n = 25 còn 30%). 
    + Bản khai `docs/ai-usage.md` AI viết ban đầu ghi quá vai trò của mình ("đọc từng nhánh", "tự viết lại kịch bản"), mình sửa lại cho đúng việc mình thật sự làm. 
    + Lỗi mã đoạn kèm ngoặc `[D08-P1]` làm mất gợi ý thì mình phát hiện khi tự dùng giao diện, không phải AI tự thấy. 
    + Phần thiết kế giao diện (tên Zebra, tự hỏi khi sai, An nhắn riêng, An chỉ xuất hiện sau khi kiểm lại đúng) là mình quyết sau khi tự thử, AI viết code theo.

3. Một câu thử trượt và mình học được gì: 
- B18 ở lượt 1, khi học viên hỏi "Mình phải mở lại tài liệu để kiểm kiến thức. Chỉ giúp mình đoạn liên quan đến việc embedding gần nhau có bảo đảm trùng mã lỗi không.", agent lại đặt câu hỏi giả thuyết của bạn An và không đưa ra lời giải thích. 
- Với điều kiện pass cho eval này là agent chỉ giải thích nhưng không làm lộ câu trả lời, mình đã đặt câu hỏi lên Claude "Làm sao có thể giải thích mà không gây lộ đáp án?", từ đó Claude đã tạo ra bản fix: Khi học viên cần giải thích thì agent chỉ gợi ý 1 câu và không nói ra đáp án.
- Kết quả: Ở lần chạy 2 sau khi fix prompt, agent đã chủ động chọn `goi_y` và từ đó giải thích 1 câu cho đoạn [D08-P1]. Tổng điểm đi từ 17/21 -> 21/21.
- Bài học: B01 cần agent hỏi lại, B18 cần agent giải thích, tưởng rằng chúng rủi ro làm lộ câu trả lời nhưng vẫn có hướng giải, và vẫn đủ đáp ứng như cầu của học viên. Không nên dùng cứng 1 khung workflow cho mọi trường hợp.
