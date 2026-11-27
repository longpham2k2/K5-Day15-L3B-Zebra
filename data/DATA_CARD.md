# Data card — dữ liệu bản chạy thử

## Ngân hàng câu hỏi

| Mục | Chi tiết |
|---|---|
| File | `data/question_bank.json` |
| Công cụ | `get_passage`, `get_similar_question`, `check_answer`, `learner_state` |
| Nội dung | Một ý mẫu `rag_bm25_vs_embedding`, một đoạn bài `D08-P1`, một câu gốc và hai câu tương tự |
| Nguồn | Nội dung mẫu do Codex soạn theo chủ đề người dùng cung cấp, ngày 27/11/2026 |
| Nhãn | `synthetic`, ví dụ viết trực tiếp, không dùng seed |
| Bổ sung | Long hoặc Khoa điền thêm 2–4 ý từ slide khoá. Mỗi ý có mã riêng và câu hỏi có ID duy nhất. Nhóm kiểm và duyệt trước khi đưa câu hỏi thật vào ngân hàng. |

## Lượt trả lời sai mẫu

| Mục | Chi tiết |
|---|---|
| File | `data/learner_states.json` |
| Công cụ | `learner_state` |
| Nội dung | Ba lượt sai `T01`–`T03` tham chiếu câu `Q1`, gồm ví dụ sai lần đầu và lần thứ hai |
| Nguồn | Ví dụ do Codex tạo ngày 27/11/2026 để thử tra cứu cục bộ |
| Nhãn | `synthetic`, không dùng seed |

Hai file phục vụ demo. Nhóm còn cần đối chiếu ý mẫu với slide, kiểm tay câu hỏi và đáp án trước khi dùng với học viên. Lượt sai mẫu chỉ minh họa cấu trúc dữ liệu.
