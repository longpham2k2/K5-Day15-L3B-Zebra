# Script thuyết trình CP4 — 1 người nói, ~5 phút 30

> Deck: 5 trang (bìa · vấn đề · giải pháp · demo · kết quả). Số lấy từ `evidence/summary.md`, `spec.md` §2, `eval/report.md`, `validation/log.md`, `cost/cost-estimate.md` trên `main` lúc 28/11 (commit `f97b4bd` — đã có U3, U4).
> Chữ **đậm** = nhấn giọng. `[…]` = thao tác, không đọc. Tổng ~5:30, chừa 30 giây trễ.
> *(Bản nháp do coding agent soạn; người nói đọc thành tiếng 1 lần, sửa cho quen miệng.)*

## Chuẩn bị trước khi lên (≤ 1 giờ trước)

- [ ] `.env` = OpenAI `gpt-5.4-nano` → `python run.py` → góc trên phải ghi **model gpt-5.4-nano**.
- [ ] Chạy thử 1 vòng (gọi model thật), rồi bấm **Phiên mới**, nhập mã `DEMO`, dừng ở Q1 — chưa chọn.
- [ ] Mở sẵn 2 cửa sổ: deck (trang bìa) và trang demo. Video dự phòng mở sẵn ở tab thứ ba.
- [ ] Chép sẵn lý do để dán: `Mình nghĩ hai embedding gần nhau thì mã lỗi phải trùng từng ký tự`

---

## Trang 1 · Bìa — 0:00 → 0:20

> Chào thầy cô, bọn mình là nhóm Zebra, lớp L3B, track A4 — Lớp học kiểu mới. Nhóm có bốn người: Long, Đạt, Khoa, Huy.
> Đề tài của bọn mình: khi học viên vừa trả lời **sai** một câu, làm sao để họ **biết chắc** mình đã hiểu lại — thay vì tự tra rồi đoán là hiểu.

## Trang 2 · Vấn đề — 0:20 → 1:20

> Bọn mình khảo sát **25 học viên khoá 5** ngoài nhóm, phỏng vấn 4 bạn, và đào data pre-class.
>
> Điều đầu tiên: học viên **không lười**. Sau khi sai, gần như ai cũng làm gì đó — **70%** hỏi ChatGPT, nhiều bạn mở lại slide.
> Vấn đề là việc đó **tốn thời gian** — **83%** nói vậy. Và nó kết thúc bằng cảm giác "chắc là hiểu rồi": **30%** bị chính ý đó quay lại làm vướng, phần lớn mất 16 đến 30 phút.
>
> Trong app cũng không có cách kiểm: mỗi ý kiến thức chỉ có **một** câu ôn tập — trong 424 câu sai, chỉ **2** câu được làm lại.
>
> Cộng lại khoảng **99 giờ một tháng** cho một khoá — đây là con số tự ước tính, và là mức thấp vì chưa tính thời gian tự tra.

*Nếu bị hỏi về phỏng vấn:* 4 học viên khoá 5, chỉ 1 bạn gặp pain một phần; 3 bạn tự xoay xở được. Người có thời gian thì tự kiểm được — người ít thời gian thì không, đó là người dùng của bọn mình.

## Trang 3 · Giải pháp — 1:20 → 2:20

> Giải pháp là **một vòng ngắn ngay sau câu sai**, năm bước.
>
> Học viên trả lời sai. Trợ lý Zebra hỏi ngay: **vì sao bạn chọn vậy?** — lý do lấy sẵn từ ghi chú hiểu sai của chính đáp án bạn chọn, nên chủ yếu là bấm.
> **AI chỉ quyết định ở bước 3**: gợi ý gì, và gợi ý **bắt buộc có mã đoạn bài** của khoá. Rồi học viên làm một câu cùng ý — và **code chấm** theo đáp án, không phải AI. AI không thấy đáp án, nên không thể nói "bạn đúng rồi" khi bạn sai.
> Đúng rồi thì bạn học An hỏi lại, học viên giải thích một câu — học bằng cách dạy lại.
>
> Khác ChatGPT ở ba chỗ: bắt đầu từ **đúng đáp án bạn đã chọn**, chỉ nói trong **bài của khoá**, và kết thúc bằng **một câu kiểm có chấm**.
> Và nếu lý do là "Mình đoán", hệ thống không gọi AI, đúng cũng **không khen** là đã hiểu.

## Trang 4 · Demo — 2:20 → 4:05

`[Chuyển sang cửa sổ demo]`

> Bọn mình chạy thật, model gpt-5.4-nano.

`[Chọn C ở Q1 → Gửi câu trả lời]`

> Câu hỏi về tìm tài liệu có mã lỗi E417. Mình cố tình chọn **C** — dùng embedding, tưởng hai vectơ gần nhau thì trùng từng ký tự. Sai.

`[Zebra hỏi lý do → dán lý do → Gửi]`

> Zebra hỏi ngay vì sao. Mình gõ đúng điều mình nghĩ.

`[Chờ ~6 giây — trong lúc chờ nói:]`

> Lúc này là lần gọi model duy nhất trong cả vòng.

`[Gợi ý hiện ra — chỉ vào nút "Xem đoạn bài D08-P1"]`

> Gợi ý chỉ ra embedding xếp theo **nghĩa**, BM25 xếp theo **khớp từ** — và có **nguồn**: đoạn D08-P1 trong bài.

`[Câu kiểm lại: chọn A → Kiểm lại]`

> Câu cùng ý nhưng tình huống khác. Chọn A — đúng, và chấm bằng code.

`[Bấm tab Bạn học An → gõ: "Embedding so gần nghĩa, tìm đúng mã thì dùng BM25" → Gửi]`

> Bạn An cũng từng chọn C và hỏi vì sao chưa đúng. Mình giải thích một câu.

`[Màn hình kết quả]`

> Cả vòng khoảng **nửa phút**.

`[Nếu còn ≥ 20 giây: Kết thúc — sang nhận xét → kéo xuống → mở "Chi tiết kỹ thuật"]`

> Ở đây thấy từng bước: đúng **một** lần gọi model, có số token. Nếu học viên bấm "Mình đoán", số lần gọi model là **không** — và lát nữa các bạn sẽ thấy nút này quan trọng thế nào.

*Mạng hỏng / model lỗi:* "Bọn mình có video quay sẵn" → mở video, nói lại đúng các câu trên.

## Trang 5 · Kết quả & kết luận — 4:05 → 5:20

`[Quay lại deck, trang 5]`

> Bộ câu thử 21 câu. **Lượt 1 đạt 17/21** — trượt một câu bắt buộc: học viên hỏi chuyện lab, model lại "sửa" một ý sai mà học viên **không hề nói**. Đau nhất với người dùng là bị gán lời như vậy.
> Bọn mình sửa **luật chọn bước**: chỉ sửa lỗi khi học viên tự nêu niềm tin sai, ngoài phạm vi ghi cụ thể, và code tự ghép lời nhắn. **Lượt 2 đạt 21/21**, hai người chấm mù khớp nhau. Lưu ý: mới **một lượt**, chưa đo độ ổn định.
>
> Nhưng metric quan trọng nhất là **học viên có hiểu lại thật không** — và chỗ này bọn mình **chưa đạt**. Trưa nay **3 học viên khoá 5** dùng thử, tự bấm. Cả 3 đều đúng câu cùng ý, trung vị **1 phút** một vòng — nhưng cả 3 đều bấm **"Mình đoán"** chỉ sau 5 đến 9 giây. Theo đúng chuẩn bọn mình chốt từ trước, đoán thì **không tính** là hiểu lại → **0/3**.
>
> Bài học: chính cái nút "Mình đoán" bọn mình làm để không khen nhầm đã thành **lối tắt** — người dùng bấm để đi nhanh, nên bước hỏi lý do chưa lấy được suy nghĩ thật.
>
> Chi phí không phải vấn đề: khoảng **$0,0004** mỗi lần hỏi lại thành công, **dưới $2 một tháng** cho 436 học viên.
>
> Nên kết luận của bọn mình là **làm tiếp, chưa mở rộng**. Nếu có thêm một tuần: hỏi lý do bằng câu mở trước để "Mình đoán" không còn là lối tắt, rồi đo lại trên ít nhất 3 học viên; và cho bạn An **phản hồi đúng sai có căn cứ** — vì một người thử thấy An đồng ý cả lời giải thích sai.

## Kết — 5:20 → 5:30

> Cảm ơn thầy cô, bọn mình xin nghe góp ý.

---

## Câu hỏi có thể gặp

| Hỏi | Trả lời ngắn | Nguồn |
|---|---|---|
| 21/21 có phải học thuộc câu thử không? | Không — sửa luật chung, không so khớp câu chữ câu thử nào; nhưng mới chạy 1 lượt, model có dao động (thử trước lượt 2 có lúc trượt B12, B18, B20) | `eval/report.md` §3 |
| Sao không tính người thử ngoài khoá? | Định nghĩa metric chốt trước: học viên khoá 5. U1 ngoài khoá → bonus, không tính N | `validation/log.md` |
| Đúng 3/3 mà sao lại 0/3? | Chuẩn chốt trước 19:30 thứ Sáu: chỉ tính người đúng **với lý do không yếu**; cả 3 bấm "Mình đoán" nên đúng có thể là đoán. Không đổi chuẩn sau khi có kết quả | `spec.md` §7 |
| Người thử có thích không? | Cả 3 học viên khoá 5 trả lời "hơi tiếc" nếu mai không được dùng. Ở các vòng làm thêm (không tính metric), 2/3 vòng có lý do thật thì đúng | `validation/log.md` |
| Người thử có xem được đoạn bài trước câu kiểm lại không? | Có — U4 nói "tài liệu đang được ra quá sớm"; nhóm ghi rủi ro câu kiểm lại đo đọc chứ không đo hiểu | `eval/report.md` §4 |
| Buổi thử có đúng như định nghĩa metric không? | Lệch: người thử tự bấm trên web, không phải nhóm gõ vào `run.py`; agent, model, input giữ nguyên; ghi ở `spec.md` §10 | `validation/log.md` |
| Sao chọn bài này mà không làm "bạn học AI được đáp lại nhiều hơn"? | 98,9% lời xen vào bị bỏ qua, nhưng người có đáp lại chỉ đúng lần đầu hơn 2,7 điểm (85,1% vs 82,4%) | `spec.md` §2 |
| Gợi ý có lộ đáp án câu kiểm lại không? | Đạt metric `khong_lo_dap_an` theo định nghĩa, nhưng nhóm tự ghi rủi ro: câu kiểm lại có thể đo nhớ gợi ý hơn là hiểu → viết câu kiểm lại theo góc khác | `eval/report.md` §4 |
| Chi phí tháng tính thế nào? | 50 phiên mô phỏng, token thật từ API; 3 persona từ khảo sát câu 7; ước tính dè dặt vì mô phỏng gọi model nhiều hơn một vòng thật | `cost/cost-estimate.md` |
