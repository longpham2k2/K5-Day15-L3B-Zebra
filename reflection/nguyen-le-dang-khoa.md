# Reflection — Nguyễn Lê Đăng Khoa

1. Vai trò + phần mình làm (trỏ tới file / commit):
   Mình là TV3 trong các file eval. Mình làm phần bằng chứng từ người dùng và phần chuẩn bị buổi thử.\
   Bằng chứng: soạn và gửi [khảo sát](../evidence/survey/questions.md), lưu kết quả đã bỏ thông tin cá nhân đến khi chốt n = 25 (`b9c6755`, `9c4fc7f`, `052d033`, `e78a431`). Chép [phỏng vấn P6](../evidence/interviews/P6.md) từ log chat (`9846a87`, `95f0eb4`).\
   Đánh giá: thêm câu thử B11–B16 có nguồn từ khảo sát và phỏng vấn (`d8472a7`). Chấm thử với vai người thứ hai ([cham-thu-nguoi-thu-hai.md](../eval/cham-thu-nguoi-thu-hai.md), `19a4f8c`, `174a8cd`). Chấm mù run-2 trên nhánh `grade2-khoa`.\
   Buổi thử: thêm 2 ý Q2, Q3 từ hướng dẫn Lab 01 (`fbe2225`). Viết [quy trình buổi thử](../validation/quy-trinh.md) (`9c50250`) và giao diện web bản đầu (`af7a939`, `a963de7`).\
   Bàn giao và thuyết trình: viết HANDS-OFF.md cho Long (`b8ecce6`), slide và [script thuyết trình](../slides/script-thuyet-trinh.md) (`0f5e5a2`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   Mình dùng Claude Code cho khảo sát, câu thử, data Q2/Q3, quy trình buổi thử, giao diện web và script, và Claude (Design) cho slide. Chi tiết ở [khai báo dùng AI](../docs/ai-usage.md).\
   Ở khảo sát, AI soạn bộ câu hỏi. Mình duyệt lại và sửa câu 1 trên form trước khi gửi.\
   Ở data Q2/Q3, đoạn bài D01-P1 do AI viết bị thiếu token suy nghĩ (`thoughts_token_count`). Ghi chú hiểu sai cũng viết ở ngôi thứ ba, trong khi lý do phải là lời của học viên. Lỗi này phát hiện khi rà lại, Long sửa ở `5154ac8`.\
   Ở phần chấm thử, mình tự chấm trước rồi mới nhờ AI rà theo chữ định nghĩa. Sau khi rà, 14/20 ô đổi, nên mình giữ lại bản đầu ở mục 1a để không lẫn điểm của mình với điểm AI gợi ý.\
   Với slide, mình đối chiếu từng số với `validation/log.md` và `eval/report.md`, và cập nhật lại khi có kết quả buổi thử (0/3).

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   B14 là câu mình thêm, lấy từ câu trả lời R21 trong khảo sát ("mất cả buổi chiều để xem hiểu là rốt quộc bài lab muốn làm gì"). Ở lượt 1, học viên hỏi bài lab muốn làm gì, và model lại chọn `sua_loi_ban` và gán cho học viên một ý sai lấy từ ghi chú của đáp án ([report §2](../eval/report.md)). Đây là câu `tu_choi` bắt buộc, nên chỉ một câu trượt cũng làm cả lượt chưa đạt. Sau khi Long sửa luật chọn bước, B14 qua ở lượt 2.\
   Bài học đầu tiên của mình là câu thử lấy từ lời người dùng thật bắt được lỗi mà câu tự viết không bắt được. Học viên không nói theo khuôn, và model dễ đoán thay cho họ.\
   Buổi thử còn cho mình bài học thứ hai: trong quy trình, mình xếp "Mình đoán" vào nhóm lý do yếu để agent không khen nhầm. Thực tế, cả 3 học viên khoá 5 đều bấm nút này sau 5–9 giây cho nhanh, nên kết quả là 0/3. Một quy tắc đúng trên giấy vẫn có thể bị người dùng dùng thành lối tắt. Phải xem người dùng bấm gì thật thì mới biết thiết kế có đo được điều mình muốn đo hay không.
