# HANDS-OFF — việc cần Long làm (Khoa bàn giao lúc 28/11 ~01:00)

> Khoa soạn cùng coding agent (Claude Code) từ trạng thái `origin/main` lúc 00:56 (commit `897db42`). Không chứa key hay mật khẩu.
> Làm xong mục nào thì đánh `[x]`. Xoá file này sau CP4 nếu nhóm không muốn để trong repo nộp bài.

## 0. Đã xong — để Long nắm

- **Khảo sát** đóng ~21:05, chốt n = 25 (25/25 ngoài nhóm) · `evidence/survey/results.csv`, `questions.md` (log gửi đủ).
- **Ngân hàng câu**: Khoa thêm Q2, Q3 (từ hướng dẫn Lab 01 của khoá) + Huy thêm Q4–Q6 · Long đã sửa Q2/Q3 lúc 00:45.
- **Giao diện buổi người dùng thử**: `codebase/web.py` (commit `af7a939`, `a963de7`). Gọi đúng `answer()` với cùng input như bộ câu thử, tự bấm giờ, lưu phiên vào `validation/phien-thu/`, có bản chạy Render (bắt buộc `APP_PASSCODE`, giới hạn 20 lượt gọi / phút, nút tải toàn bộ phiên). Cách dùng: `validation/quy-trinh.md` mục "Cách chạy chính" và "Chạy trên Render".
- **Chấm mù run-1**: Khoa đã push nhánh `grade-khoa` (Long đã chốt 17/21 ở `487f503`).
- **Slide 5 trang** (Claude Design): bìa · vấn đề · giải pháp · demo · kết quả & kết luận. Trang 3–4 còn khung chờ số. Khoa sẽ gửi link (đang để riêng tư).

## 1. Trước 10:00 — key OpenAI cho buổi người dùng thử

Buổi thử chốt dùng **`gpt-5.4-nano`** (cùng model với eval). Chỉ Long có key OpenAI.

- [ ] Chọn **một** cách:
  - **(a) Render** — Khoa tạo Web Service từ URL repo công khai (không cần Long cấp quyền GitHub). Long gửi key **riêng cho Khoa** (tin nhắn riêng, không dán vào nhóm chat, repo hay file), Khoa dán vào biến `API_KEY` trên Render. Lưu ý: deploy từ URL công khai **không tự deploy lại** khi có commit mới — sau mỗi lần Long push (vd sửa `agent.py` cho lượt 2), báo Khoa bấm **Manual Deploy**.
  - **(b) Máy Long** — Long cầm máy buổi thử: `git pull` → `python codebase/web.py` → mở http://127.0.0.1:8765, chia sẻ cửa sổ trình duyệt.
- [ ] Đặt **giới hạn chi tiêu** cho key trên trang OpenAI. Ước tính cả buổi 5 người ≈ 0,0013 USD (mỗi người tối đa 1 lần gọi model, ~797 token vào / ~72 ra theo run-1; giá $0,20 / $1,25 mỗi 1M token — nguồn bên thứ ba, đối chiếu trang giá OpenAI). Rủi ro duy nhất là lộ key.
- [ ] Sau hackathon: **thu hồi key** (hoặc ngay khi nghi lộ).

## 2. Trước 10:30 — chốt cách chạy buổi thử

- [ ] **Ai bấm?** `eval/metric_spec.yaml` (đã khoá) ghi metric `hieu_lai_tren_nguoi_thu` chạy bằng `python run.py`, *người trong nhóm gõ input theo lựa chọn học viên đọc ra*.
  - Người trong nhóm bấm trên `web.py` (cùng `answer()`) → gần đúng định nghĩa, chỉ cần 1 dòng changelog (mục 3).
  - Người thử tự bấm qua link Render → **lệch định nghĩa**: changelog phải ghi rõ và báo cáo kết quả kèm lưu ý này.
- [x] **Thứ tự câu gốc** (Long chốt: đủ 6 câu Q1–Q6, làm tiếp được sau một vòng; metric tính vòng đầu): `web.py` đang dùng `ROOT_ORDER = ["Q1", "Q4", "Q5", "Q6"]` theo `quy-trinh.md` (Huy) — tức **bỏ Q2, Q3**. Đúng ý nhóm không? Nếu muốn dùng cả 6 câu: sửa danh sách đó.
- [x] `quy-trinh.md` dòng "đề + 3 lựa chọn A/B/C" — **Q5 có 4 lựa chọn** (A–D); sửa chữ cho khớp (giao diện web đã hiện đủ 4).
- [ ] Bảng hẹn ở `validation/log.md`: điền **U2, U3** (vai, nguồn, giờ, ai cầm máy / ghi). Cần **4–5 người** để chắc ≥ 3 người vào vòng — U4, U5 chưa hẹn.

## 3. Trước CP4 14:30 — changelog `spec.md` §10 (bảng "CP2 → CP4")

Ba dòng còn thiếu. Bản nháp để dán, Long sửa chữ nếu cần:

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
| 27/11 ~22:36 | `data/question_bank.json`: thêm 2 ý Q2 (`llm_api_token_usage`) và Q3 (`chatbot_history_window`) viết lại từ hướng dẫn Lab 01 của khoá, kèm lượt sai mẫu (sau đó Q2 đổi sang T14–T15) | Ngân hàng chỉ có 1 câu gốc → người thử dễ làm đúng và không vào vòng, metric `hieu_lai_tren_nguoi_thu` không đo được. Không đụng câu thử, metric hay ngưỡng |
| 28/11 ~00:26–00:43 | Thêm `codebase/web.py`: giao diện web cho buổi người dùng thử — gọi đúng `answer()` với cùng định dạng input, tự bấm giờ, lưu phiên ở `validation/phien-thu/`; bản chạy Render bắt buộc mã vào trang, giới hạn 20 lượt / phút | Buổi thử online: giảm lỗi gõ tay và đo thời gian một vòng chính xác cho metric 5. Không đổi hành vi agent, metric hay ngưỡng |
| 28/11 [giờ] | Buổi người dùng thử chạy bằng `web.py` thay cho gõ vào `python run.py`; [người trong nhóm bấm theo lựa chọn người thử đọc ra / người thử tự bấm qua link]; model `gpt-5.4-nano` | `metric_spec.yaml` ghi chạy bằng `run.py`; `web.py` gọi cùng `answer()` nên hành vi agent giống hệt. [Nếu người thử tự bấm: ghi rõ đây là lệch so với định nghĩa] |

## 4. Trước CP4 — `docs/ai-usage.md` (hiện còn trống hoàn toàn)

Luật đề: khai thiếu không bị trừ, giấu mới bị. Phần của Khoa — bản nháp để Long gộp vào bảng:

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Khảo sát | Claude Code | Soạn bộ câu hỏi (`evidence/survey/questions.md`) và script tạo form (`create_form.gs`); tham khảo form nhóm khác chỉ về cách trình bày; tải Sheet và xuất `results.csv` đã bỏ email, liên hệ, giờ | Khoa duyệt câu hỏi, sửa câu 1 trên form, gửi form, xác nhận người trả lời ngoài nhóm | Khoa |
| Viết câu thử (B11–B16) | Claude Code | Đề xuất 6 câu có nguồn từ khảo sát / phỏng vấn | Khoa thêm vào bộ câu thử; Đạt sửa lại câu chữ và nguồn | Khoa, Đạt |
| Chấm thử người thứ hai | Claude Code | Soạn bảng chấm; **sau khi Khoa tự chấm**, rà lại theo chữ định nghĩa (14/20 ô đổi, bản đầu giữ ở mục 1a) | Khoa tự chấm trước; Đạt so sánh | Khoa |
| Chấm mù run-1 | Claude Code | Tạo bảng đọc 21 câu và script chép điểm vào cột `pass` (không chấm) | Khoa tự chấm cả 21 câu | Khoa |
| Ngân hàng câu Q2, Q3 | Claude Code | Viết lại 2 ý từ hướng dẫn Lab 01 của khoá thành đoạn bài, câu gốc, câu tương tự, ghi chú hiểu sai | Khoa chạy kiểm thử; Long sửa nội dung (00:45) | Khoa, Long |
| Giao diện buổi thử | Claude Code | Viết `codebase/web.py`, nhánh Gemini trong `codebase/ai.py`, chạy thử trên trình duyệt | Khoa chạy thử và duyệt | Khoa |
| Slide | Claude (Design) | Soạn nội dung từ `evidence/summary.md`, `spec.md` và dựng deck 5 trang + ghi chú người nói | Khoa duyệt chữ và số | Khoa |

## 5. Sau lượt 2 — số cho slide trang 4

- [ ] Gửi Khoa: kết quả lượt 2 (x/21, run ID), 1 lỗi chính lượt 1 + đã sửa gì, kết quả buổi thử (x/N với lý do không yếu, trung vị phút), chi phí / task thành công (từ Huy).
- [ ] Chốt **2 câu demo** (đang đề xuất B01 thường + B12 hoặc B02 khó) và **ai nói trang nào**.

## 6. Không gấp

- [ ] Nhánh `origin/khoa` và `origin/grade-khoa` đã gộp / đã dùng xong — xoá hay giữ tuỳ Long.
- [ ] Nhắc Huy: `cost/personas.yaml` vẫn là số "(ví dụ)" của Gemini; thêm giá `gpt-5.4-nano` có nguồn rồi chạy `python run.py simulate`.

## 7. Prompt mẫu cho coding agent của Long

Dán nguyên khối dưới vào Claude Code / Codex đang mở repo (sau `git pull`):

```
Đọc HANDS-OFF.md ở thư mục gốc repo (Khoa bàn giao). Làm các việc trong repo mà không cần bí mật nào:

1. spec.md §10, bảng "CP2 → CP4": thêm 3 dòng theo bản nháp ở mục 3 của HANDS-OFF.md. Dòng thứ 3 có chỗ [ ] — hỏi tôi chọn "người trong nhóm bấm" hay "người thử tự bấm" và giờ chạy trước khi điền; không tự đoán.
2. docs/ai-usage.md: gộp bảng ở mục 4 vào bảng sẵn có (giữ tiêu đề cột của file), rồi hỏi tôi điền nốt các dòng phần của Long, Đạt, Huy — không tự bịa ai dùng công cụ gì.
3. validation/quy-trinh.md: sửa câu "đề + 3 lựa chọn A/B/C" cho đúng (Q5 có 4 lựa chọn A–D). Hỏi tôi có giữ ROOT_ORDER = ["Q1","Q4","Q5","Q6"] trong codebase/web.py không; nếu đổi thì sửa cả web.py và quy-trinh.md cho khớp.
4. Chạy `python run.py check` và `python codebase/test_tools.py`; báo kết quả.

Luật: không sửa eval/metric_spec.yaml, chuẩn "đạt" ở spec.md §7, câu thử hay kết quả các lượt đã chạy (AGENTS.md). Không đọc, in hay ghi API key; không đụng .env. Không commit hay push khi tôi chưa đồng ý. Đánh [x] các mục đã xong trong HANDS-OFF.md.
```
