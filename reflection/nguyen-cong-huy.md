# Reflection — Nguyễn Công Huy

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):
   Mình phụ trách công cụ của agent và mô phỏng chi phí.\
   Mình chốt đầu vào, đầu ra và cách xử lý khi thiếu dữ liệu cho bốn hàm đọc lượt sai, lấy đoạn bài, lấy câu tương tự và chấm đáp án trong [tools.py](../codebase/tools.py) (`588eaa1`).\
   Mình thêm [bài tự kiểm](../codebase/test_tools.py) (`bfd879b`) và đưa quy mô, tần suất sử dụng vào [cấu hình mô phỏng](../cost/personas.yaml) (`d37410d`).

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   Mình dùng Codex để viết các hàm theo đầu vào, đầu ra đã chốt và dựng dữ liệu mẫu cho Q1.\
   Ở phần chi phí, Codex giúp quy đổi token API của lượt eval 2 sang USD. Mình cung cấp tần suất theo khảo sát và mức giá mini từ bảng của BTC.\
   Khi rà bản tính của Codex, phần phải tính lại là sáu ô chi phí tháng cho hai model ở ba quy mô. Ước tính của mini dùng lượng token đo trên nano rồi áp giá mini. [Khai báo dùng AI](../docs/ai-usage.md)

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   Ở B18 lượt 1, học viên hỏi đoạn nào giải thích liệu embedding gần nhau có bảo đảm trùng mã lỗi. [Kết quả lượt 1](../eval/run-1.csv)\
   Agent trỏ đúng đoạn `D08-P1` nhưng lại gán một cách hiểu sai cho An rồi hỏi An nhầm ở đâu. Học viên vẫn chưa được giải thích rằng gần nhau về nghĩa không bảo đảm mã lỗi trùng từng ký tự.\
   Mình rút ra là khi kiểm công cụ lấy đoạn bài, mình có thể xác nhận mã và nội dung trả về. Khi kiểm cả luồng, mình còn phải đọc lời nhắn để xem agent đã dùng đoạn đó trả lời đúng câu học viên hỏi chưa.
