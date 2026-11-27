# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.

*(Bản nháp do coding agent soạn từ đề A4 và README của data pack, trước khi đọc dòng data nào. Nhóm duyệt / sửa trước khi commit.)*

- Ngày giờ viết: 27/11/2026, trước khi chạy `evidence/count.py`
- Người dùng chính (một vai cụ thể): học viên AI20K L3-4 khoá 5 tự học trang pre-class trước buổi lên lớp
- **Mình nghĩ:** học viên học pre-class gặp khó khi **xem một đoạn bài giảng rồi trả lời câu kiểm tra sau đoạn đó** vì họ học **thụ động**: xem / tua video, bỏ qua câu hỏi giữa video và **phớt lờ lời bạn học AI xen vào** (bộ điều phối cho xen vào nhưng học viên không tương tác lại). Khi có tương tác thì cũng nông: tự giải thích / nhắn AI chỉ vài chữ. Hậu quả là trả lời sai lần đầu và không sửa được, đến lớp chưa hiểu bài.
- **Có thể còn cách giải thích khác:**
  - Học viên bỏ qua vì thiếu thời gian (học dồn sát giờ), không phải vì trải nghiệm thụ động.
  - Lời bạn học AI xen vào không đáng trả lời (lạc đề, ngắt mạch), nên phớt lờ là hợp lý.
  - Câu hỏi giữa video quá dễ / quá khó, nên tỉ lệ đúng không phản ánh mức hiểu.
- **Mình đúng nếu thấy:**
  - ≥80% lượt bạn học AI xen vào (theo `intervention_id`) **không** có học viên trả lời lại, **và**
  - ≥25% câu hỏi giữa video bật lên bị bỏ qua hoặc tua qua, **và**
  - học viên có tương tác với bạn học AI trả lời đúng lần đầu cao hơn rõ (≥10 điểm %) so với học viên không tương tác *(tương quan, không phải nhân quả)*.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [x] đào data · [x] phỏng vấn ≥3 · [ ] khảo sát ≥20 — nguồn chính: đào data `data/preclass` · nguồn để kiểm lại: phỏng vấn ≥3 học viên cùng khoá (vì sao bỏ qua lời xen vào / câu hỏi)
