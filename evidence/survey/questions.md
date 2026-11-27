# Khảo sát — hiểu sai rồi có sửa được không (A4)

> *(Bản nháp do coding agent soạn từ `TEMPLATE.md`, `../interviews/SCRIPT.md` và `../data-mining.md`; bản 2 chỉnh cách trình bày sau khi tham khảo form của một nhóm khác — chỉ học cách trình bày, không chép câu hỏi. Nhóm đã duyệt và gửi form lúc 12:42 27/11; file này ghi lại **đúng bộ câu đã hỏi** (khác bản nháp ở câu 1, xem ghi chú dưới câu đó). Ghi vào `docs/ai-usage.md` dòng "Rà câu hỏi phỏng vấn / khảo sát".)*
>
> **Vai trò:** khảo sát dùng để **đếm** (bao nhiêu người gặp, mấy lần, mất gì), còn phỏng vấn dùng để hiểu **vì sao**. Hai nguồn kiểm chéo nhau, không thay nhau.
> **Ngưỡng R1:** ≥20 người **ngoài nhóm**, đúng người dùng (học viên khoá 5). Không gửi cho 4 thành viên nhóm. Câu 1 khác "học viên" thì không tính vào mẫu số chính.

## Log gửi (điền khi gửi)

| | |
|---|---|
| Link form | https://docs.google.com/forms/d/e/1FAIpQLSe74TZJOAm8vjt7Zzya2L0NWm2RjgIUR2uNMz0nedayr1g_GA/viewform |
| Bản lưu giữa chừng | 27/11 · 12 phản hồi (mới nhất 16:34) → `results.csv` — chưa chốt |
| Bản lưu 2 | 27/11 · 22 phản hồi (mới nhất 17:21), 22/22 học viên L3A / L3B → ghi đè `results.csv`; R01–R12 giữ nguyên mã và nội dung, R13–R22 nối thêm theo giờ gửi · đạt ngưỡng ≥20 · form vẫn mở |
| Bản lưu 3 | 27/11 · 24 phản hồi (mới nhất 17:24), 24/24 học viên L3A / L3B → ghi đè `results.csv`; R01–R22 giữ nguyên, R23–R24 nối thêm · form vẫn mở |
| Bản chốt | 27/11 · 25 phản hồi → ghi đè `results.csv` lần cuối (xem dòng "Số phản hồi lúc chốt"). Câu 3–6 không đổi so với bản lưu 3 vì R25 chọn "Không nhớ / chưa gặp" ở câu 2 |
| Kênh đã gửi | Discord server của cohort "[L34] AI20K Build Phase", nhóm kênh CỘNG ĐỒNG, kênh `#chung` (trao đổi chung toàn cohort L3–L4) · một tin, do TV Khoa đăng |
| Giờ mở | 27/11/2026 12:42 (giờ đăng tin) · phản hồi đầu tiên 12:44 |
| Tin nhắn thật đã gửi | *"Hi mọi người, nhóm mình đang làm một khảo sát nhỏ về cách mọi người học và ôn bài trong khoá ạ. Mọi người dành giúp tụi em khoảng 3 phút làm form nhé, ẩn danh hoàn toàn nha. Cảm ơn mọi người nhiều ạ 🙏"* + link form (Discord tự hiện tiêu đề và lời mở đầu form bên dưới) |
| Giờ chốt | 27/11/2026 ~21:05 (Khoa tắt "Chấp nhận câu trả lời" trên form) · phản hồi cuối lúc 19:30 |
| Số phản hồi lúc chốt | **25** · trong đó học viên ngoài nhóm: **25/25** (16 L3A · 9 L3B · 0 "Khác"; R01–R24 nhóm xác nhận 27/11, R25 Khoa xác nhận 27/11 ~21:10 — không thành viên nào trả lời) → `results.csv` bản chốt, R01–R24 giữ nguyên, R25 nối thêm |

## Cài đặt Google Form

- **Tạo nhanh:** chạy [`create_form.gs`](create_form.gs) trên script.google.com. Script tạo đủ câu hỏi, nhánh, tắt thu email và nối sẵn một Sheet phản hồi. Cách chạy ghi ở đầu file.
- **Số câu trong form = số câu trong file này** ("Câu 1." … "Câu 11."). Câu có nhánh thì đi theo hướng ghi bên dưới, người làm có thể không thấy một số câu, nhưng số không bao giờ chạy lùi.
- Script không bật được "trộn thứ tự lựa chọn". Sau khi tạo, vào câu 3 → ⋮ → **Trộn thứ tự tuỳ chọn** để bật tay (riêng "Khác" luôn ở cuối). *Bản đã gửi: __ (chưa xác nhận đã bật hay chưa — nếu chưa thì thứ tự lựa chọn câu 3 cố định như danh sách bên dưới).*
- **Thu thập email: Tắt.** Không bật "Giới hạn 1 phản hồi" vì việc đó bắt đăng nhập.
  - *Thực tế:* form tạo ra lúc đầu có ô Email bắt buộc; nhóm đã tắt trước phản hồi đầu tiên (12:44). Sheet phản hồi vẫn còn cột "Địa chỉ email" nhưng **trống ở cả 24/24 dòng** (kiểm 27/11 17:29) → không thu email của ai. Cột này cùng cột câu 11 bị bỏ khi xuất `results.csv`.
- Không có câu hỏi về tên, mã học viên, SĐT, tuổi hay điểm số.

## Tiêu đề và lời mở đầu form

**Tiêu đề:** KHẢO SÁT ẨN DANH: CÁCH HỌC VÀ ÔN TRONG KHOÁ AI20K

**Mô tả:**

> Xin chào! Nhóm mình là học viên AI20K khoá 5, đang tìm hiểu **chuyện gì xảy ra sau khi mình trả lời sai hoặc hiểu sai một ý trong khoá**: mình làm gì tiếp, có kiểm lại không, và nó tốn của mình những gì.
>
> - Khoảng **3 phút**, 11 câu, phần lớn là chọn đáp án.
> - Câu hỏi đều về **lần gần nhất đã xảy ra**. Không có đúng / sai, không nhớ thì cứ chọn "Không nhớ".
> - **Ẩn danh:** không hỏi tên, email hay điểm. Kết quả chỉ dùng cho bài hackathon và chỉ báo cáo dạng tổng hợp (vd "12/25 người"), không công khai từng câu trả lời.
>
> Cảm ơn bạn đã dành thời gian!

**Lời cảm ơn khi gửi xong:** Cảm ơn bạn! Nếu bạn để lại liên hệ ở câu cuối, nhóm sẽ nhắn hẹn trong 1–2 ngày tới.

## Tin nhắn gửi kèm link

Bản đã gửi thật: xem dòng "Tin nhắn thật đã gửi" ở bảng Log. Tin nhắn không nhắc tới sản phẩm hay AI, để không dẫn dắt câu trả lời.

---

## Câu hỏi

### Phần 1 — Về bạn

**Câu 1. Bạn đang là:** *(chọn một, bắt buộc)*
- Học viên lớp L3A
- Học viên lớp L3B
- Khác

> Bản nháp (và `create_form.gs`) có 5 lựa chọn: thêm "Học viên lớp khác của khoá 5" và "Lab coach / TA / giảng viên". Form đã gửi chỉ có 3 lựa chọn trên (nhóm sửa tay trên form trước khi gửi; kiểm trên form đang chạy, 27/11). "Khác" có thể lẫn cả lab coach lẫn học viên lớp khác → không tính vào mẫu số chính. Bản lưu 3: 0/24 chọn "Khác".

### Phần 2 — Lần hiểu sai gần nhất *(kiểm D2, phần chính)*

**Câu 2. Lần gần nhất bạn trả lời sai, hoặc nhận ra mình hiểu sai một ý trong khoá, là khi nào?** *(ở bất kỳ đâu: câu hỏi trên lớp, quiz, câu ôn tập, lab, bài nhóm…; chọn một, bắt buộc)*
- Hôm nay
- 1–3 ngày trước
- 4–7 ngày trước
- Hơn 1 tuần trước
- Không nhớ / chưa gặp lần nào → **chuyển tới Phần 4 (câu 7)**

### Phần 3 — Sau lần hiểu sai đó *(bối cảnh: "nghĩ về đúng lần ở câu 2")*

**Câu 3. Ngay sau khi biết mình sai, bạn đã làm gì?** *(chọn nhiều)*
- Đọc đáp án / lời giải rồi học tiếp
- Xem lại slide / video / tài liệu
- Hỏi trợ giảng AI trong trang học của khoá
- Hỏi ChatGPT hoặc một AI khác bên ngoài
- Hỏi bạn học / lab coach / giảng viên
- Làm thêm một câu hoặc bài tương tự
- Bỏ qua, chưa làm gì
- Khác: ___

**Câu 4. Sau đó, bạn đã kiểm lại xem mình hiểu ý đó chưa?** *(ví dụ làm một câu khác cùng ý, giải thích lại cho ai đó, dùng lại trong lab; chọn một)*
- Có, ngay trong ngày
- Có, vài ngày sau
- Chưa kiểm lại
- Không nhớ

**Câu 5. Lần hiểu sai đó đã khiến bạn mất gì?** *(chọn nhiều)*
- Không mất gì đáng kể
- Mất thời gian tìm lại tài liệu hoặc hỏi lại
- Làm lab / bài tập sai, phải sửa lại
- Bị hỏi trên lớp mà không trả lời được
- Làm bài nhóm chậm hoặc sai, ảnh hưởng tới bạn cùng nhóm
- Khác: ___

**Câu 6. Sau đó, ý đó có quay lại làm bạn vướng không?** *(buổi sau, lab, bài nhóm…; chọn một, bắt buộc)*
- Có, và mình lại vướng → **sang câu 6b**
- Có, nhưng lúc đó mình đã nắm
- Chưa gặp lại
- Không nhớ

**Câu 6b. *(chỉ hiện khi câu 6 = "lại vướng")* Lần vướng lại đó bạn mất thêm khoảng bao lâu?** *(chọn một)*
- Dưới 5 phút
- 5–15 phút
- 16–30 phút
- Trên 30 phút
- Không nhớ

### Phần 4 — Trong 7 ngày gần đây *(dùng cho impact ở `spec.md` §2)*

**Câu 7. Trong 7 ngày gần đây, khoảng mấy lần bạn sai / hiểu sai một ý mà không chắc sau đó mình đã hiểu lại?** *(chọn một, bắt buộc)*
- 0 lần
- 1 lần
- 2–3 lần
- 4–6 lần
- 7 lần trở lên
- Không nhớ

> Hỏi **7 ngày** chứ không hỏi 1 tháng: khoá mới chạy khoảng 3 tuần (data từ 05/11), và khoảng ngắn thì người làm nhớ chính xác hơn.

**Câu 8. Ở lần hiểu sai gần nhất, điều gì khiến bạn khó chịu hoặc tốn công nhất?** *(đoạn văn, không bắt buộc)*

### Phần 5 — Trang pre-class *(kiểm D1)*

**Câu 9. Từ đầu khoá tới giờ, bạn đã học trên trang pre-class khoảng bao nhiêu ngày?** *(chọn một, bắt buộc)*
- Chưa bao giờ → **chuyển tới Phần 6 (câu 11)**
- 1–2 ngày → **chuyển tới Phần 6**
- 3–5 ngày → **sang câu 10**
- Trên 5 ngày → **sang câu 10**
- Không nhớ → **chuyển tới Phần 6**

**Câu 10. *(chỉ hiện khi câu 9 ≥ 3 ngày)* Lần gần nhất một "bạn học AI" tự nói chen vào lúc bạn đang học trên trang pre-class, bạn đã làm gì?** *(chọn một, bắt buộc)*
- Không để ý / không thấy nó nói gì
- Đọc nhưng không trả lời
- Lướt qua rồi xem tiếp
- Trả lời lại nó
- Không nhớ

**Câu 10b. *(chỉ hiện khi câu 10 = "Đọc nhưng không trả lời" hoặc "Lướt qua rồi xem tiếp")* Lúc đó điều gì khiến bạn không trả lời?** *(đoạn văn, không bắt buộc)*
> Để ô trống, **không** đưa sẵn lựa chọn lý do (cùng luật với câu 14 của kịch bản phỏng vấn: không gợi ý lý do).

### Phần 6 — Kết thúc

**Câu 11. *(không bắt buộc)* Bạn có sẵn lòng cho nhóm hỏi thêm 10–15 phút về lần học gần nhất không?** Nếu có, để lại Discord hoặc Zalo bạn muốn được liên hệ; không thì bỏ trống.

> Câu 11 là chỗ duy nhất có thể có thông tin liên hệ. **Xoá cột này trước khi xuất `results.csv`**. Người đồng ý thì chuyển sang danh sách hẹn phỏng vấn, chỉ ghi vai và giờ vào `evidence/summary.md` (mục "Lịch hẹn").

---

## Cố ý KHÔNG hỏi

Form tham khảo có các câu kiểu *"Nếu có ứng dụng AI làm X, bạn có muốn dùng thử không?"*, *"Bạn mong muốn sản phẩm có tính năng gì?"*, *"Bạn có hứng thú khi sản phẩm ra mắt không?"*. Phiếu này **không** có loại câu đó, vì:
- Đó là câu giả định. Người làm gần như luôn trả lời "có", nên số thu được không phải bằng chứng pain (Mom Test, và `TEMPLATE.md` ghi rõ "không hỏi có thích không").
- Giới thiệu giải pháp ngay trong form sẽ dẫn dắt các câu trả lời sau.
- Muốn thử phản ứng với ý tưởng thì làm ở `validation/log.md` (người dùng thử), không làm ở khảo sát pain.

Cũng không hỏi tuổi hay nghề: không câu nào trong phân tích dùng tới, và hỏi thêm chỉ làm form dài hơn.

## Câu nào đo cái gì → đổ vào đâu

| Câu | Đo gì | Kiểm chéo với | Dùng ở |
|---|---|---|---|
| 1 | Lọc đúng người dùng | — | Mẫu số chính = học viên (3 lựa chọn đầu) |
| 2 | Bao nhiêu người gặp hiểu sai gần đây | — | `spec.md` §2 cột "Bao nhiêu người gặp" |
| 3 | Đang xoay xở bằng gì | data: 74/399 (18,5%) nhắn AI trong 30 phút sau khi sai | `summary.md` §2 cột "Đang xoay xở bằng" · `spec.md` §1 |
| 4 | **D2: có kiểm lại không** | data: **1/399 (0,3%)** làm lại câu cùng ý | `summary.md` §2, §4 — số chính |
| 5 | **Hậu quả** (pain có đủ đau không) | phỏng vấn câu 10 | `spec.md` §1 "hậu quả gì" · §2 cột "Mỗi lần tốn gì" |
| 6, 6b | Hiểu sai có quay lại không + phút mất thêm | phỏng vấn câu 9–10 | `spec.md` §2 cột "Mỗi lần tốn gì" |
| 7 | Số lần / tuần | phỏng vấn câu 19 | `spec.md` §2 · `cost/personas.yaml` (`uses_per_month`) |
| 8, 10b | Trích dẫn nguyên văn | — | `summary.md` §3 (≥3 câu) |
| 9 | Độ phủ pre-class | data: 220/721 (30,5%) dùng ≥3 ngày | `summary.md` §4 (khớp / lệch) · chia nhóm khi đếm |
| 10 | **D1: phản ứng với lời bạn học AI xen vào** | data: 7.903/7.992 (98,9%) không đáp lại | `summary.md` §4 · chọn giải pháp ở `spec.md` §4 |

**Khi đếm:**
- Báo `x/n` kèm mẫu số rõ ràng, ví dụ câu 4 thì mẫu số = học viên không chọn "Không nhớ / chưa gặp" ở câu 2. Dưới khoảng 10 người thì chỉ ghi `x/n`, không ghi %.
- Đếm riêng hai nhóm theo câu 9 (dùng pre-class ≥3 ngày và còn lại), không cộng chung (cùng luật với `summary.md` §2).
- Câu 6b và câu 7 là **khoảng**. Muốn nhân ra impact thì lấy điểm giữa khoảng (câu 7: 1 → 1 · 2–3 → 2,5 · 4–6 → 5 · 7+ → 8; câu 6b: 5–15' → 10' …), đổi tuần sang tháng bằng × 30/7, và ghi rõ *(điểm giữa khoảng, quy đổi tuần → tháng — tự ước tính)*.
- Câu 3 và 5 chọn nhiều: tổng có thể vượt 100%, ghi rõ. Câu 5 tách riêng số người chỉ chọn "Không mất gì đáng kể", vì đó là phản chứng cho pain.

## Lưu kết quả

- `evidence/survey/results.csv`: bản xuất từ Google Sheets, **đã xoá** cột câu 11. Bản gốc có thông tin liên hệ thì **không** commit.
- Số chính + ≥3 câu trả lời nguyên văn (câu 8, 10b) → chép vào `evidence/summary.md` §2, §3.
