# Người dùng thử *(bonus)*

> Điền ở guide bước 4.3 — 2–3 người ngoài nhóm, ~10 phút / người, theo 5 nhịp: làm quen · bối cảnh · giao việc · quan sát · hỏi sau. Ôn lại: ngày 5, ngày 13. Chấm ở rubric Bonus.
> Không ghi tên: ghi vai. Hành vi quan sát được nặng hơn lời nói; toàn lời khen = phiên chưa đạt, giao việc khó hơn.
> Người dùng thử **không thay được** bằng chứng pain ở `evidence/`.

## Lịch hẹn người dùng thử (chỉ ghi vai và giờ, không tên)

> Cũng là nơi đo metric `hieu_lai_tren_nguoi_thu` (`eval/metric_spec.yaml`): cần **≥ 3 học viên khoá 5 ngoài nhóm vào được vòng** hỏi lại (sai một câu gốc). Người làm đúng hết câu gốc ghi "không vào vòng", không tính vào N.
> **Khung giờ chung (Long chốt 27/11 ~22:25):** 28/11 **10:30–12:30**, sau CP3 10:00 — để còn kịp ghi kết quả và đưa vào slide trước CP4 14:30. Hẹn **4–5 người** để chắc có ≥ 3 người vào vòng.
> **Lệch so với định nghĩa metric (ghi `spec.md` §10):** buổi thực tế 28/11 chạy **trực tiếp**, **người thử tự bấm** trên giao diện web (`python run.py`) ở máy TV1; TV1 đứng sau quan sát và ghi, không hướng dẫn thêm (riêng U1 được động viên một lần ở bước giải thích cho An). Agent, model và định dạng input giữ nguyên.
> **Cách chạy online (dự kiến ban đầu):** người thử đọc to lựa chọn (câu gốc, lý do, câu tương tự); người trong nhóm gõ input vào `python run.py` và chia sẻ màn hình; không quay. Bấm giờ từ lúc agent hỏi lý do tới lúc có kết quả chấm câu tương tự.

| # | Vai | Từ đâu | Ai hẹn | Giờ hẹn | Hình thức | Ai cầm máy / ghi | Đã xong? |
|---|---|---|---|---|---|---|---|
| U1 | Học sinh / sinh viên **ngoài khoá AI20K** (= P3 phỏng vấn) — **không tính vào N** của metric (định nghĩa: học viên khoá 5) | Phỏng vấn P3, đồng ý dùng thử | TV1 | 28/11 ~13:00–13:10 | Trực tiếp · người thử tự thao tác trên máy TV1 | người thử tự bấm / TV1 đứng sau quan sát, ghi | ✅ (bonus, không tính N) |
| U2 | Học viên L2, khoá 5 (= P4 phỏng vấn) — **tính vào N** | Phỏng vấn P4, đồng ý dùng thử | TV1 | 28/11 ~13:35–13:45 | Trực tiếp · người thử tự thao tác trên máy TV1 | người thử tự bấm / TV1 đứng sau quan sát, ghi, không hướng dẫn thêm | ✅ |
| U3 | Học viên L3B, khoá 5 (cùng lớp TV1, ngoài nhóm) — **tính vào N** | Bạn cùng lớp, gặp trực tiếp ở trường | TV1 | 28/11 ~14:00–14:12 | Trực tiếp · người thử tự thao tác trên máy TV1 | người thử tự bấm / TV1 đứng sau quan sát, ghi lại lời nhận xét | ✅ |
| U4 | Học viên L3B, khoá 5 (cùng lớp TV1, ngoài nhóm) — **tính vào N** | Bạn cùng lớp, gặp trực tiếp ở trường | TV1 | 28/11 ~14:13–14:18 | Trực tiếp · người thử tự thao tác trên máy TV1 | người thử tự bấm / TV1 đứng sau quan sát, ghi lại lời nhận xét | ✅ |
| U5 | __ | __ | __ | __ | __ | __ / __ | Chưa hẹn |

Cách chạy từng người: [quy-trinh.md](quy-trinh.md).

## Kết quả vòng hỏi lại (metric `hieu_lai_tren_nguoi_thu`)

Model dùng: OpenAI `gpt-5.4-nano` (cùng model với eval lượt 1, lượt 2) · máy cầm: máy TV1 · chạy bằng `python run.py` (giao diện web `codebase/web.py`), mỗi phiên lưu ở `validation/phien-thu/`

| # | Câu gốc sai (lựa chọn) | Mã lượt | Lý do (nguyên văn) | Nhóm lý do (có lý do / yếu / bỏ qua) | Câu tương tự | Trả lời | Đúng? | Thời gian (phút) | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| U1 *(ngoài khoá — không tính N)* | Q2 (chọn A) | T14 | "Mình nghĩ prompt_token_count là số token model sinh ra." *(bấm lựa chọn có sẵn, 7,2 giây)* | có lý do | Q2-S1 | C | đúng | 0,8 | Agent chọn `sua_loi_ban`, 1 lần gọi model. Giải thích cho An (sau khi đúng): "boi vi dap an A la lay token vao" — có giải thích. File: `phien-thu/U1-20261128-131046.json` |
| U2 | Q1 (chọn C) | T01 | "Mình đoán" *(bấm lựa chọn có sẵn, 5,4 giây)* | **yếu** | Q1-S1 | A | đúng | 1,0 | **Vòng đầu — vòng tính metric:** đúng với nhóm yếu → không tính là hiểu lại. Agent nhắc "chưa dám nói bạn đã hiểu chắc". Giải thích cho An: bỏ qua. Người thử sai cả 4 câu gốc đã làm và chạy thêm 3 vòng (không tính metric, báo riêng): Q2 có lý do → **sai** (chuyển lab coach, 1,0 phút) · Q3 có lý do ("Mình nghĩ 3 lượt hội thoại là 3 tin nhắn.") → **đúng**, giải thích cho An đúng ý ("vi 3 luot hoi thoai tuong duong voi 6 tin nhan…"), 0,7 phút · Q4 "Mình đoán" → đúng, 1,1 phút. File: `phien-thu/U2-20261128-134509.json` |
| U3 | Q4 (chọn B) | T06 | "Mình đoán" *(bấm lựa chọn có sẵn, 5,9 giây)* | **yếu** | Q4-S1 | A | đúng | 1,0 | **Vòng đầu — vòng tính metric:** đúng với nhóm yếu → không tính là hiểu lại; agent nhắc "chưa dám nói bạn đã hiểu chắc". Giải thích cho An: bỏ qua. Đúng Q1–Q3, sai Q4–Q6 — **chọn B ở cả 6 câu gốc**. Thêm 2 vòng (báo riêng, không tính metric): Q5 "Mình đoán" → đúng, 0,8 phút · Q6 có lý do (bấm lựa chọn có sẵn) → **đúng**, 0,7 phút; cả 3 vòng đều bỏ qua bước giải thích cho An. File: `phien-thu/U3-20261128-141238.json` |
| U4 | Q3 (chọn C) | T08 | "Mình đoán" *(bấm lựa chọn có sẵn, 9,4 giây)* | **yếu** | Q3-S1 | B | đúng | 0,6 | **Vòng đầu — vòng tính metric:** đúng với nhóm yếu → không tính là hiểu lại. Giải thích cho An: bỏ qua (7 giây). Đúng Q1, Q2; dừng sau 1 vòng. File: `phien-thu/U4-20261128-141836.json` |
| U5 | | | | | | | | | |

Người đúng cả 3 câu gốc: ghi "không vào vòng" ở cột "Câu gốc sai", để trống các cột còn lại.

**Tổng kết (buổi 28/11, chỉ vòng đầu của mỗi người):** N (vào vòng) = **3** (U2, U3, U4; U1 ngoài khoá không tính) · đúng với **có lý do** **0/3** · đúng với **yếu (đoán)** **3** · đúng với **bỏ qua** 0 · trung vị thời gian **1,0 phút** (0,6 · 1,0 · 1,0) → **chưa đạt**: đủ N ≥ 3 và trung vị ≤ 5 phút, nhưng 0/3 < 2/3 — cả 3 người bấm "Mình đoán" ở vòng đầu nên theo định nghĩa đã khoá không ai **tính là** hiểu lại.

**Đọc kết quả cho đúng:** "Mình đoán" là lý do của **lần chọn sai đầu tiên**, không nói gì về câu kiểm lại. Định nghĩa đã khoá chỉ tính nhóm có lý do vì chỉ khi học viên nêu một ý sai thì mới thấy ý đó được sửa; với người đoán, một câu kiểm lại đúng không tách được hiểu với may (3 lựa chọn → 1/3). Vì vậy 0/3 nghĩa là **chưa chứng minh được** hiểu lại, không phải **đã chứng minh không** hiểu. Cả 3 người đều đúng câu kiểm lại sau gợi ý — nếu cả 3 chỉ đoán thì xác suất 3/3 đúng khoảng (1/3)³ ≈ 4% — nên có tác động thật; nhưng buổi thử không tách được đó là **hiểu** hay **đọc được đáp án từ gợi ý / đoạn bài** (U4: "tài liệu đang được ra quá sớm"). Cần câu kiểm lại không lặp câu chữ đoạn bài hoặc hỏi lại sau một khoảng thời gian (`eval/report.md` §4).

*Báo riêng — các vòng sau vòng đầu (không tính metric):* 5 vòng thêm của U2, U3 (U4 dừng sau 1 vòng): có lý do 3 vòng → đúng 2 (U2-Q3, U3-Q6), sai 1 (U2-Q2, chuyển lab coach); "Mình đoán" 2 vòng → đúng 2. Lý do ở cả 9 vòng (kể cả U1) đều là **bấm lựa chọn có sẵn**, chưa ai tự gõ lý do; "Mình đoán" được bấm sau ~5–9 giây. Ba người khoá 5 đều "hơi tiếc" nếu mai không được dùng.

## Quan sát (bonus)

| Người thử (vai) | Việc giao (theo kết quả, không theo nút) | Quan sát (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai) | Trích nguyên văn | Mức nghiêm trọng (cao / vừa / thấp) |
|---|---|---|---|---|
| U2 (L2, khoá 5) | Làm câu gốc đến khi sai, rồi theo vòng hỏi lại, rồi giải thích cho An; tự chọn làm tiếp các câu sau | Lúc đầu bỡ ngỡ với giao diện; **hiểu lầm rằng An sẽ chấm điểm lần nữa**; ở vòng đầu bỏ qua bước giải thích cho An, các vòng sau có giải thích | "An co ve chi tra loi 1 chieu nen giai thich du dung hay sai deu dong y, nen cai thien" · "Cac ly thuyet con kha moi nhung sau khi tra loi sai model tra loi kha ngan gon, nhung co ve kho giai thich lai cho nguoi khac chi sau 1 lan model tra loi" · gợi ý có giúp: "Phan lon giup toi chon duoc cau tuong tu. Vi toi da duoc giai thich nen van ghi nho duoc" | **cao** (An đồng ý cả lời giải thích sai — bước An không phản hồi đúng sai) · vừa (tưởng An chấm điểm) |
| U3 (khoá 5) | Làm câu gốc đến khi sai, rồi theo vòng hỏi lại; tự chọn làm tiếp các câu sau | **Chọn B ở cả 6 câu gốc**; 2/3 vòng bấm "Mình đoán" trong ~6 giây; **do dự vì không muốn trả lời An**, bỏ qua bước An cả 3 vòng | "Chỗ chuyển sang An, lúc đầu không hiểu An là gì và làm sao gặp" · gợi ý có giúp: "Có, vì mình trả lời lại đúng hết" *(TV1 ghi lại từ lời nói)* | **cao** (bấm "Mình đoán" để đi nhanh — lý do không phản ánh suy nghĩ thật) · vừa (không hiểu An là ai, không muốn trả lời An) |
| U4 (L3B, khoá 5) | Làm câu gốc đến khi sai, rồi theo vòng hỏi lại | Bấm "Mình đoán"; bỏ qua bước An; **hiểu sai rằng câu kiểm lại không cần đối chiếu đoạn bài đã trích** | "Có, nhưng mình cảm thấy tài liệu đang được ra quá sớm, mình bấm là đọc được ngay" (gợi ý có giúp không) · "Không, có hướng dẫn đầy đủ dễ dùng" (chỗ khó hiểu) *(TV1 ghi lại từ lời nói)* | **cao** (đoạn bài mở ngay trước câu kiểm lại → câu kiểm lại có thể đo đọc chứ không đo hiểu) |
| U1 (ngoài khoá) | Làm câu gốc đến khi sai, rồi theo vòng hỏi lại, rồi giải thích cho An | Lúc đầu bỡ ngỡ khi chuyển giữa khung câu hỏi và khung trò chuyện; câu 1 làm đúng, sang câu 2 đã thao tác được. **Bất ngờ khi phải giải thích cho An, định bỏ qua, người ghi phải động viên** | "Chờ chuyển tab sang người dùng" (chỗ khó hiểu nhất) · "Kha thuan tien cho viec hoc, nhung can responsive lai phan textbox tin nhan input va output" · gợi ý có giúp: "Co. Boi vi cau hoi tuong tu co de cap den kien thuc cau sai" | vừa (bước An cần người nhắc) · thấp (ô nhập) |
| | | | | |
| | | | | |

Câu hỏi sau: *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* → U1 (ngoài khoá): không sao · U2: **hơi tiếc** · U3: **hơi tiếc** · U4: **hơi tiếc**

## Tổng hợp

- Chủ đề lặp nhiều nhất: **bước lý do bị đi tắt** (cả 9 vòng dùng lựa chọn có sẵn; 3/3 người khoá 5 bấm "Mình đoán" ở vòng đầu) và **bước An chưa rõ, chưa có phản hồi** (U1, U3 không hiểu An là ai / làm sao gặp; U2: An đồng ý cả lời giải thích sai; bỏ qua bước An 5/9 vòng).
- Sửa gì trước demo (ghi `spec.md` §10): không sửa thêm agent hay giao diện sau buổi thử — kết quả buổi thử ghi nguyên, đưa vào slide và `eval/report.md` §4.
- Giữ gì và vì sao: trợ lý tự hỏi ngay khi sai (không cần bấm nút) và câu kiểm lại chấm bằng code — người thử vào vòng nhanh (trung vị 1,0 phút), 3/3 người khoá 5 "hơi tiếc" nếu không được dùng; agent không lỗi lần nào trong 9 vòng.
- Để dành sau: đổi bước lý do để "Mình đoán" không còn là lối tắt; An hỏi tiếp câu nhiều lựa chọn chấm bằng code; hỏi lại ý đã sai sau một khoảng thời gian; An hỏi cả khi đúng lần đầu (`eval/report.md` §4).
- **Góp ý giám khảo (Demo Zone 28/11, ghi sau buổi demo):** (1) vì sao An chỉ hỏi khi sai lần đầu rồi đúng lần hai — đề xuất hỏi cả khi đúng ngay lần đầu; (2) làm sao kiểm lời giải thích gửi An, vì học viên có thể quên ý sau khi qua câu kiểm lại và trả lời "Tôi không còn nhớ nữa".
