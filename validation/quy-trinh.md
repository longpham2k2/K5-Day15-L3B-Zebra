# Quy trình buổi người dùng thử — 28/11, 10:30–12:30, online

> Dùng cho mọi người thử U1–U5 ở `validation/log.md`. Đo metric `hieu_lai_tren_nguoi_thu` (`eval/metric_spec.yaml`) và ghi quan sát cho phần bonus.
> ⚠️ **Không chia sẻ màn hình file này** — bảng mã lượt ở mục 2 để lộ đáp án câu gốc. Chỉ chia sẻ cửa sổ terminal chạy `python run.py`.
> *(Bản nháp do coding agent soạn từ `metric_spec.yaml`, `codebase/agent.py`, `data/`. Nhóm duyệt trước buổi.)*

## Cách chạy chính: giao diện web (`codebase/web.py`)

Thay cho việc gõ tay vào `python run.py` (mục 2–3 bên dưới giữ làm phương án dự phòng):

1. Ở thư mục repo: `python codebase/web.py` → mở **http://127.0.0.1:8765** trên máy người cầm máy. Dòng đầu trang ghi model đang dùng — phải đúng model nhóm chốt.
2. **Chia sẻ đúng cửa sổ trình duyệt này** (không phải cả màn hình — tránh lộ file có đáp án).
3. Điền mã người thử (U1…U5) → **Bắt đầu**. Trang tự hiện câu gốc theo thứ tự Q1 → Q4 → Q5 → Q6 (sửa `ROOT_ORDER` trong `web.py` nếu nhóm đổi); người thử đọc to lựa chọn, người cầm máy bấm.
4. Sai câu gốc → trang tự tra mã lượt, hỏi lý do (bấm lý do có sẵn / "Lý do khác" để gõ nguyên văn / "Bỏ qua bước này"), **tự bấm giờ**, đưa gợi ý và câu tương tự, chấm, rồi sang màn hình nhận xét. Đúng hết câu gốc → "không vào vòng", vẫn sang nhận xét.
5. Màn hình nhận xét: rất tiếc / hơi tiếc / không sao · chỗ khó hiểu nhất · gợi ý có giúp không · nhận xét khác (nguyên văn) · quan sát của người ghi → **Lưu phiên**.
6. Sau khi lưu: phiên ghi vào `validation/phien-thu/<mã>-<giờ>.json` (không tên; có lý do nguyên văn, nhóm lý do theo đúng quy tắc metric, số giây, tóm tắt trace) và trang hiện **sẵn một dòng** để dán vào bảng "Kết quả vòng hỏi lại" ở `validation/log.md`.

Trang gọi đúng `answer()` của agent với cùng định dạng input như bộ câu thử, nên kết quả giống `run.py`. Đáp án câu gốc không gửi xuống trình duyệt.

### Chạy trên Render (nếu cần mở bằng link)

Render → **New → Web Service** → nối repo GitHub của nhóm, nhánh `main`:

| Mục | Giá trị |
|---|---|
| Runtime | Python 3 · Region: Singapore · Instance: Free |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python codebase/web.py` |
| Health Check Path | `/` |
| Environment | `MODEL_PROVIDER=openai` · `MODEL_NAME=gpt-5.4-nano` · `API_KEY=<key OpenAI của nhóm>` · `APP_PASSCODE=<mã nhóm tự đặt>` · `PYTHON_VERSION=3.12` · (tuỳ chọn) `MAX_AGENT_CALLS_PER_MIN=20` |

- Thiếu `APP_PASSCODE` thì máy chủ **không khởi động** (tránh lộ key). Mã chỉ nhóm giữ, người cầm máy nhập ở màn hình đầu; không gửi mã cho người thử.
- Gói Free **ngủ sau 15 phút** không dùng, lần mở đầu mất ~50 giây → mở trang trước giờ hẹn mỗi người.
- **Ổ đĩa Render bị xoá khi khởi động lại / deploy lại** → sau mỗi người thử bấm **"Tải toàn bộ phiên (JSON)"**; cuối buổi tải lần nữa, tách thành file `validation/phien-thu/<mã>-<giờ>.json` rồi commit. Bản dự phòng: mỗi phiên in một dòng `[phien] …` trong Logs của Render.
- Máy chủ xử lý **một người một lúc** — chạy người thử lần lượt theo lịch.
- Đặt hạn mức chi tiêu cho key OpenAI trước khi chia link.

## 0. Vai trong nhóm (mỗi người thử cần 2 người)

| Vai | Làm gì |
|---|---|
| **Người cầm máy** | Đọc câu hỏi, gõ input vào `python run.py`, chia sẻ cửa sổ terminal |
| **Người ghi** | Bấm giờ, ghi bảng ở `validation/log.md`, chép nguyên văn lời người thử |

## 1. Chuẩn bị (trước 10:30, ~10 phút)

1. `git pull --rebase origin main` — để có ngân hàng câu mới (Q1–Q6, lượt T01–T15).
2. Kiểm `.env` trên máy cầm máy: có `MODEL_PROVIDER`, `MODEL_NAME`, `API_KEY`. **Model dùng: OpenAI `gpt-5.4-nano`** — cùng model với eval lượt 1 và lượt 2 (chốt 28/11 ~00:27): `.env` = `MODEL_PROVIDER=openai`, `MODEL_NAME=gpt-5.4-nano`, `API_KEY=<key OpenAI của nhóm>`. Mở giao diện web, dòng đầu trang phải ghi `model gpt-5.4-nano`.
3. Chạy thử 1 vòng không người: `python run.py` → gõ `attempt=T05` → phải thấy agent hỏi lý do. Gõ `Enter` 2 lần để thoát.
4. Mở sẵn: link họp online · `data/question_bank.json` (để đọc câu gốc) · `validation/log.md` (để ghi) · đồng hồ bấm giờ.
5. **`python run.py` không tự lưu trace** → sau mỗi người, **chép toàn bộ chữ trong terminal** vào một file tạm (vd `validation/raw-U1.txt`, KHÔNG có tên người thử) để làm bằng chứng.

## 2. Bảng tra mã lượt (KHÔNG chia sẻ màn hình)

Người thử chọn sai ở câu gốc nào, lựa chọn nào → gõ mã lượt tương ứng:

| Câu gốc | Chọn A | Chọn B | Chọn C | Chọn D | Câu tương tự agent sẽ đưa |
|---|---|---|---|---|---|
| Q1 (BM25 vs embedding) | `T02` | Đúng | `T01` | — | Q1-S1 |
| Q2 (token usage) | `T14` | Đúng | `T15` | — | Q2-S1 |
| Q3 (lịch sử chatbot) | `T07` | Đúng | `T08` | — | Q3-S1 |
| Q4 (ReAct) | `T05` | `T06` | Đúng | — | Q4-S1 |
| Q5 (precision và recall) | `T09` | `T10` | `T11` | Đúng | Q5-S1 |
| Q6 (chatbot và agent) | Đúng | `T12` | `T13` | — | Q6-S1 |

Ô **Đúng** → sang câu gốc tiếp theo.

## 3. Kịch bản cho một người thử (~10 phút)

### 3.1 Làm quen + bối cảnh (1 phút)
> "Cảm ơn bạn. Nhóm mình đang thử một công cụ giúp ôn lại sau khi trả lời sai. Mình **thử công cụ, không chấm bạn** — sai là bình thường, thậm chí giúp nhóm hơn. Không ghi tên, không quay. Bạn cứ nói to lựa chọn và nghĩ gì thì nói nấy nhé."

### 3.2 Câu gốc (người cầm máy đọc, chưa chạy agent)
1. Đọc **Q1**: đề + 3 lựa chọn A/B/C (lấy từ `data/question_bank.json`). Người thử chọn.
2. Tra bảng mục 2:
   - **Chọn đúng** → đọc tiếp **Q4**, **Q5**, rồi **Q6**.
   - **Chọn sai** → sang 3.3 ngay. **Chỉ chạy 1 vòng / người** (dừng ở câu sai đầu tiên).
   - **Đúng cả 4** → ghi **"không vào vòng"**, nhảy tới 3.5 (vẫn hỏi nhận xét).

### 3.3 Vòng hỏi lại (người cầm máy gõ — người ghi bấm giờ)

| Bước | Gõ vào `python run.py` | Agent trả | Người thử làm |
|---|---|---|---|
| a | `attempt=T0x` (mã từ bảng mục 2) → **bắt đầu bấm giờ** khi output hiện | `buoc: hoi_ly_do` + danh sách lý do | Chọn 1 lý do / tự nói lý do / bỏ qua |
| b | `attempt=T0x; ly_do=<đúng chữ người thử chọn hoặc nói>` — bỏ qua thì để trống: `attempt=T0x; ly_do=` | gợi ý (có mã đoạn) + câu tương tự | Chọn A/B/C cho câu tương tự |
| c | `attempt=T0x; ly_do=<giữ nguyên như bước b>; cau=<mã câu tương tự>; tra_loi=<A/B/C>` → **dừng bấm giờ** khi output hiện | `ket_qua_dung` hoặc `chuyen_lab_coach` | — |

Lưu ý khi gõ:
- **Bước c phải giữ nguyên `ly_do`** như bước b — agent dựa vào đó để nhận ra "đoán" và không nói "đã hiểu".
- Người thử chọn lý do có sẵn → gõ **đúng chữ** của lý do đó (vd `ly_do=Mình đoán`). Tự nói → gõ **nguyên văn** lời họ.
- Không giải thích thêm, không gợi ý đáp án. Người thử hỏi → "bạn cứ chọn theo ý bạn".
- Agent báo lỗi / mất mạng → ghi lại, chạy lại từ bước a với cùng mã lượt (bấm giờ lại từ đầu), ghi chú "chạy lại".

### 3.4 Quan sát trong lúc làm (người ghi)
- Người thử làm gì đầu tiên khi thấy output? Đọc gợi ý hay bỏ qua?
- Chỗ do dự (im lặng > 5 giây), chỗ hỏi lại, chỗ hiểu sai output.
- Chép **nguyên văn** câu họ nói.

### 3.5 Hỏi sau (2 phút)
1. "Nếu mai không được dùng nữa, bạn thấy: **rất tiếc / hơi tiếc / không sao**?"
2. "Chỗ nào làm bạn **khó hiểu nhất**?"
3. "Gợi ý vừa rồi có giúp bạn chọn câu tương tự không — vì sao?" *(hỏi về lần vừa xảy ra, không hỏi "bạn có muốn…")*

## 4. Ghi vào `validation/log.md` ngay sau mỗi người

**Xếp nhóm lý do** — đúng quy tắc của `tach_doan_voi_hieu`:

| Nhóm | Khi nào |
|---|---|
| **bỏ qua** | `ly_do` để trống |
| **yếu** | có chữ "đoán", hoặc là một trong: ok / oke / k / ko / không / k biết / ko biết / không biết / ? / . , hoặc dài ≤ 3 ký tự |
| **có lý do** | còn lại |

Mỗi người thử điền **một dòng** ở bảng "Kết quả vòng hỏi lại" và **một dòng** ở bảng quan sát.

## 5. Sau buổi — tổng kết metric 5

- **N** = số người **vào vòng** (không tính "không vào vòng"). Cần N ≥ 3.
- Báo riêng 3 số: đúng câu tương tự với nhóm **có lý do** · với nhóm **yếu** · với nhóm **bỏ qua**. **Chỉ số thứ nhất tính là hiểu lại.**
- **Đạt** khi: N ≥ 3 · (đúng + có lý do) / N ≥ 2/3 · trung vị thời gian một vòng ≤ 5 phút.
- Ghi một dòng tổng kết ở cuối bảng kết quả, rồi báo Long để đưa vào `spec.md` §7 và slide trang 5.
