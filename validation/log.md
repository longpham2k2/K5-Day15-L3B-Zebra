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
| U3 | Học viên L3A, khoá 5 | Khảo sát — tự để lại liên hệ ở câu 11 (= P6) | TV3 | 28/11, giờ cụ thể: __ | Online · chia sẻ màn hình, không quay; người thử để lại nhận xét bằng lời / chữ | __ / __ | Chưa |
| U4 | __ | __ | Long | __ | __ | __ / __ | Chưa |
| U5 | __ | __ | __ | __ | __ | __ / __ | Chưa hẹn |

Cách chạy từng người: [quy-trinh.md](quy-trinh.md).

## Kết quả vòng hỏi lại (metric `hieu_lai_tren_nguoi_thu`)

Model dùng: OpenAI `gpt-5.4-nano` (cùng model với eval lượt 1, lượt 2) · máy cầm: máy TV1 · chạy bằng `python run.py` (giao diện web `codebase/web.py`), mỗi phiên lưu ở `validation/phien-thu/`

| # | Câu gốc sai (lựa chọn) | Mã lượt | Lý do (nguyên văn) | Nhóm lý do (có lý do / yếu / bỏ qua) | Câu tương tự | Trả lời | Đúng? | Thời gian (phút) | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|
| U1 *(ngoài khoá — không tính N)* | Q2 (chọn A) | T14 | "Mình nghĩ prompt_token_count là số token model sinh ra." *(bấm lựa chọn có sẵn, 7,2 giây)* | có lý do | Q2-S1 | C | đúng | 0,8 | Agent chọn `sua_loi_ban`, 1 lần gọi model. Giải thích cho An (sau khi đúng): "boi vi dap an A la lay token vao" — có giải thích. File: `phien-thu/U1-20261128-131046.json` |
| U2 | Q1 (chọn C) | T01 | "Mình đoán" *(bấm lựa chọn có sẵn, 5,4 giây)* | **yếu** | Q1-S1 | A | đúng | 1,0 | **Vòng đầu — vòng tính metric:** đúng với nhóm yếu → không tính là hiểu lại. Agent nhắc "chưa dám nói bạn đã hiểu chắc". Giải thích cho An: bỏ qua. Người thử sai cả 4 câu gốc đã làm và chạy thêm 3 vòng (không tính metric, báo riêng): Q2 có lý do → **sai** (chuyển lab coach, 1,0 phút) · Q3 có lý do ("Mình nghĩ 3 lượt hội thoại là 3 tin nhắn.") → **đúng**, giải thích cho An đúng ý ("vi 3 luot hoi thoai tuong duong voi 6 tin nhan…"), 0,7 phút · Q4 "Mình đoán" → đúng, 1,1 phút. File: `phien-thu/U2-20261128-134509.json` |
| U3 | | | | | | | | | |
| U4 | | | | | | | | | |
| U5 | | | | | | | | | |

Người đúng cả 3 câu gốc: ghi "không vào vòng" ở cột "Câu gốc sai", để trống các cột còn lại.

**Tổng kết:** N (vào vòng) = __ · đúng với **có lý do** __/N · đúng với **yếu (đoán)** __ · đúng với **bỏ qua** __ · trung vị thời gian __ phút → **đạt / chưa đạt** (cần N ≥ 3, có lý do ≥ 2/3 N, trung vị ≤ 5 phút).

## Quan sát (bonus)

| Người thử (vai) | Việc giao (theo kết quả, không theo nút) | Quan sát (làm gì đầu tiên, chỗ do dự, chỗ hiểu sai) | Trích nguyên văn | Mức nghiêm trọng (cao / vừa / thấp) |
|---|---|---|---|---|
| U2 (L2, khoá 5) | Làm câu gốc đến khi sai, rồi theo vòng hỏi lại, rồi giải thích cho An; tự chọn làm tiếp các câu sau | Lúc đầu bỡ ngỡ với giao diện; **hiểu lầm rằng An sẽ chấm điểm lần nữa**; ở vòng đầu bỏ qua bước giải thích cho An, các vòng sau có giải thích | "An co ve chi tra loi 1 chieu nen giai thich du dung hay sai deu dong y, nen cai thien" · "Cac ly thuyet con kha moi nhung sau khi tra loi sai model tra loi kha ngan gon, nhung co ve kho giai thich lai cho nguoi khac chi sau 1 lan model tra loi" · gợi ý có giúp: "Phan lon giup toi chon duoc cau tuong tu. Vi toi da duoc giai thich nen van ghi nho duoc" | **cao** (An đồng ý cả lời giải thích sai — bước An không phản hồi đúng sai) · vừa (tưởng An chấm điểm) |
| U1 (ngoài khoá) | Làm câu gốc đến khi sai, rồi theo vòng hỏi lại, rồi giải thích cho An | Lúc đầu bỡ ngỡ khi chuyển giữa khung câu hỏi và khung trò chuyện; câu 1 làm đúng, sang câu 2 đã thao tác được. **Bất ngờ khi phải giải thích cho An, định bỏ qua, người ghi phải động viên** | "Chờ chuyển tab sang người dùng" (chỗ khó hiểu nhất) · "Kha thuan tien cho viec hoc, nhung can responsive lai phan textbox tin nhan input va output" · gợi ý có giúp: "Co. Boi vi cau hoi tuong tu co de cap den kien thuc cau sai" | vừa (bước An cần người nhắc) · thấp (ô nhập) |
| | | | | |
| | | | | |

Câu hỏi sau: *"Nếu mai không được dùng nữa, bạn thấy: rất tiếc / hơi tiếc / không sao?"* → U1 (ngoài khoá): không sao · U2: **hơi tiếc** / __

## Tổng hợp

- Chủ đề lặp nhiều nhất: __
- Sửa gì trước demo (ghi `spec.md` §10): __
- Giữ gì và vì sao: __
- Để dành sau: __
