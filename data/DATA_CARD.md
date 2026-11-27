# Data card — dữ liệu bản chạy thử

## Ngân hàng câu hỏi

| Mục | Chi tiết |
|---|---|
| File | `data/question_bank.json` |
| Công cụ | `get_passage`, `get_similar_question`, `check_answer`, `learner_state` |
| Nội dung | Sáu ý, mỗi ý có một đoạn bài, một câu gốc và hai câu tương tự |
| Nguồn | Q1 là ví dụ BM25/embedding tự soạn. Q2–Q3 dựa trên hướng dẫn Lab 01. Q4–Q6 dùng các tài liệu dưới đây. |
| Nhãn | `synthetic`, ví dụ viết trực tiếp, không dùng seed |

Nguồn đối chiếu cho ba đoạn mới, ngày 27/11/2026. Các mã đoạn dùng trong bản chạy thử.

| Đoạn | Tài liệu đã đối chiếu |
|---|---|
| D04-P1 | Hướng dẫn Lab 04, bài 1–2 về vòng lặp và lỗi công cụ. [Bài báo ReAct](https://arxiv.org/abs/2210.03629) |
| D07-P1 | Lab 09, công thức trong `src/lab9/stats.py`. [Introduction to Information Retrieval, mục 8.3](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html) |
| D08-P2 | Lab 08, *From Workflows to Agents*. [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents) |

Slide gốc của Q4–Q6 chưa được đối chiếu. Các phương án nhiễu là giả thuyết để nhóm kiểm qua buổi thử.

## Lượt trả lời sai mẫu

| Mục | Chi tiết |
|---|---|
| File | `data/learner_states.json` |
| Công cụ | `learner_state` |
| Nội dung | 15 lượt mẫu, gồm các lựa chọn sai cho Q1–Q6 và ca thiếu ý kiến thức T04. [Bảng tra mã lượt](../validation/quy-trinh.md#2-bảng-tra-mã-lượt-không-chia-sẻ-màn-hình) |
| Nguồn | Ví dụ tự tạo để thử tra cứu cục bộ ngày 27/11/2026 |
| Nhãn | `synthetic`, không dùng seed |

Hai file phục vụ demo. Nhóm còn cần đối chiếu ý mẫu với slide, kiểm tay câu hỏi và đáp án trước khi dùng với học viên. Lượt sai mẫu chỉ minh họa cấu trúc dữ liệu.
