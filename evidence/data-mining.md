# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Hướng: **A4 · Lớp học kiểu mới**. Giả thuyết viết trước: [hypothesis.md](hypothesis.md).
> Chạy lại: `python evidence/count.py <đường-dẫn>/data/preclass` — chỉ thư viện chuẩn, in ra mọi số dưới đây. Repo không chứa file data gốc.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** `data/preclass` của BTC — `events.csv`, `class_events.csv`, `answers.csv`, `chat.csv`, `rewards.csv`, `learners.csv`; 05/11/2026 → 25/11/2026 (Day01–Day13).
- **Đếm gì · trên tập nào · lọc gì:**
  1. *Lời bạn học AI xen vào có được đáp lại không.* Một **lượt tiếp xúc** = một cặp (`hv`, `intervention_id`) duy nhất từ `events.type = agent_message_shown` có `intervention_id` và `agent_id` bắt đầu bằng `classmate`. **Có đáp lại** = có dòng `chat.csv` hoặc `answers.csv` cùng `hv` + `intervention_id`. Bản chặt hơn: chỉ tính lượt hiện ra lúc tab đang hiện (`app_visibility_changed` gần nhất trước đó không phải `visible=false`).
  2. *Câu hỏi giữa video có bị bỏ qua không:* `quiz_item_dismissed` có `skipped_stop = true`.
  3. *Học từ lỗi:* câu ôn tập cuối ngày (`answers.nguon = pre_post_post`, `lan_thu = 1`) trả lời sai → sau đó học viên có làm câu khác cùng `kc_code`, hay nhắn AI trong 30 phút không.
  4. *Độ sâu khi viết:* điểm rubric của giám khảo AI trên chat đã chấm (`trang_thai_cham = da_cham`), độ dài câu nhắn.
  5. *So sánh (tương quan):* tỉ lệ đúng lần đầu của học viên từng đáp lại bạn học AI và học viên thấy nhưng không đáp lại.
- **Mẫu số là gì:** học viên → **436 người có hoạt động** (≥1 event `actor = learner`), không phải 721 tài khoản. Lời xen vào → số lượt tiếp xúc. Câu trả lời → câu có `was_correct` là True/False, `lan_thu = 1`.
- **Script:** [`evidence/count.py`](count.py)

## 2. Đọc trước, đếm sau

Đã đọc 3–4 dòng đầu mỗi file, mẫu từng loại event, `column_dictionary.csv` và `event_types.csv`. Các *kiểu* hành vi thấy được:
- Xem video, tua, câu hỏi bật lên giữa video rồi đóng (trả lời hoặc bỏ qua).
- Bộ điều phối quyết định từng đoạn bài: cho bạn học AI (note_taker, deep_thinker, inquisitive, clown) xen vào hay không, xen vào kiểu nào (`ask_check`, `summarize`…).
- Lời xen vào hiện ra cho học viên; học viên có thể đáp lại trong khung thảo luận dưới video.
- Học viên hỏi trợ giảng AI dưới video; câu hỏi được chấm rubric (bám bài, ý mới, đúng ngữ cảnh).
- Ôn tập cuối ngày (`pre_post_post`) có lời giải ngay; mini lab có câu dự đoán; tự giải thích; Sổ hiểu bài.

**Phát hiện khi kiểm data (không dùng các số này làm bằng chứng):**
- `answers.nguon = video_quiz` chỉ có 7 dòng, đều ngày 25/11 → câu giữa video mới bắt đầu ghi, **không đo được** tỉ lệ trả lời / đúng câu giữa video.
- `last_rate` luôn = 1, `crossed_stop` luôn = false → không đo được tua nhanh hay tua vượt câu hỏi.
- Mọi câu dự đoán (`du_doan = True`) đều ở mini lab và đều `was_correct = True` → không đo được "đoán đúng mà không hiểu" trên bộ này.
- `intervention_id` (`…:module-N:chunk-K:director`) không nối được với `class_events.ref_id` (`…@V1:K`) → không tách được tỉ lệ đáp lại theo kiểu xen vào, chỉ tách được theo bạn học.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Tài khoản dùng pre-class ≥3 ngày (giờ VN) | 220 / 721 | 30,5% | ≥1 ngày 436 (60,5%) · ≥5 ngày 108 (15,0%) · ≥8 ngày 43 (6,0%) · chưa từng 285 (39,5%) |
| Đoạn bài bộ điều phối cho bạn học AI xen vào | 385 / 761 | 50,6% | `ask_check` 212, `summarize` 155, `prompt_reflection` 16 |
| Học viên có hoạt động từng thấy lời xen vào | 273 / 436 | 62,6% | trung vị 12 lời / người, p90 = 77 |
| **Lượt tiếp xúc lời xen vào KHÔNG được đáp lại** | 7.903 / 7.992 | **98,9%** | chỉ tính lúc tab đang hiện: đáp lại 73/6.070 (1,2%) |
| — theo bạn học: inquisitive · deep_thinker · clown · note_taker | 46/2.379 · 41/2.533 · 2/410 · 0/2.670 | 1,9% · 1,6% · 0,5% · 0,0% | kể cả bạn hay hỏi (đặt câu hỏi kiểm tra) cũng gần như không ai đáp |
| Học viên thấy lời xen vào mà từng đáp lại ≥1 lần | 31 / 273 | 11,4% | = 31/436 (7,1%) học viên có hoạt động |
| Câu hỏi giữa video bị bấm bỏ qua | 21 / 2.099 | 1,0% | **ngược giả thuyết**: học viên gần như không bỏ qua |
| Câu ôn tập cuối ngày sai lần đầu | 399 / 1.968 | 20,3% | 100% số câu sai đều thấy lời giải ngay |
| **Sai câu ôn tập → sau đó làm câu khác cùng ý kiến thức** | 1 / 399 | **0,3%** | ⚠️ **mỗi `kc_code` chỉ có đúng 1 câu ôn tập** (156 ý · 156 câu) → app **không có câu thứ hai** để luyện lại; số này đo thiếu sót của app, không đo ý muốn của học viên |
| Câu chấm đúng / sai bị sai lần đầu → học viên làm lại **chính câu đó** | 2 / 424 | 0,5% | làm lại được (có 18 dòng `lan_thu = 2`) nhưng gần như không ai làm |
| Sai câu ôn tập → nhắn AI (câu bất kỳ) trong 30 phút | 74 / 399 | 18,5% | không biết có hỏi về đúng câu sai không |
| Chat đã chấm có `rubric_y_moi = 0` (chép / hỏi lại nguyên văn, không có ý riêng) | 909 / 1.223 | 74,3% | `= 2` (lý do, so sánh, phản biện): 226 (18,5%) |
| Chat có câu nhắn ≤15 ký tự | 150 / 1.260 | 11,9% | câu đáp lại lời xen vào: 25/144 (17,4%) |
| Học viên có hoạt động từng tự giải thích ≥1 lần | 18 / 436 | 4,1% | tổng 20 dòng, chỉ trên **5 mục** (đều là bước lab) → ô tự giải thích hiếm khi được hiện ra; 4% là "ít được mời", không phải "từ chối viết" |
| Học viên có hoạt động từng trả lời câu ôn tập cuối ngày | 77 / 436 | 17,7% | 69 người sai ≥1 câu → độ phủ của lát cắt nếu chỉ bắt đầu từ câu ôn tập |
| Học viên có hoạt động từng mở Sổ hiểu bài | 51 / 436 | 11,7% | |
| Đúng lần đầu: từng đáp lại bạn học AI vs thấy nhưng không đáp | 468/550 vs 1.575/1.911 | 85,1% vs 82,4% | chênh 2,7 điểm, **dưới ngưỡng 10 điểm**; tương quan, có thể do học viên chăm hơn |

**Đối chiếu giả thuyết:**
- ✅ ≥80% lời xen vào không được đáp lại → **98,9%**.
- ❌ ≥25% câu hỏi giữa video bị bỏ qua / tua qua → chỉ **1,0%** bỏ qua (không đo được tua qua).
- ❌ Chênh đúng lần đầu ≥10 điểm → chỉ **2,7 điểm**.
- ➕ Phát hiện thêm, ngoài giả thuyết: **sai xong gần như không ai luyện lại** — làm lại chính câu đó 2/424; và app không có câu thứ hai cùng ý để luyện (mỗi ý 1 câu).
- ➕ Bộ điều phối cho bạn học AI xen vào **chỉ trong lúc giảng** (`lesson_phase = content` ở 385/385 lượt), không lượt nào ngay sau khi học viên trả lời sai.

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

1. Lượt tiếp xúc không đáp lại: `L0006` · `program-day01:ai-llm-foundation:module-1:chunk-4:director` (bạn note_taker xen vào).
2. Lượt tiếp xúc không đáp lại: `L0007` · `program-day01:ai-llm-foundation:module-2:chunk-1:director`.
3. Lượt tiếp xúc không đáp lại: `L0008` · `program-day03:chatbot-to-agentic-agent:module-1:chunk-3:director`.
4. Câu ôn tập sai, đã thấy lời giải, không làm lại ý đó: `A00611` (`d01-on-chatbot-la-ung-dung`, ý `chatbot_is_app_around_model`), trả lời sau 32 giây.
5. Câu ôn tập sai, đã thấy lời giải: `A00288`, `A02467`, `A01030`, `A00887`.
6. Câu ôn tập sai nhiều nhất (n≥20): `d03-on-tong-5-diem` sai 12/20 (60%), `d04-on-cot-hai` 11/27 (41%), `d01-on-chatbot-la-ung-dung` 16/41 (39%).

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Thiếu / lệch:
- "Hiện ra" ≠ "đã đọc": một phần lời xen vào hiện ra khi học viên không nhìn (đã loại lượt tab ẩn, tỉ lệ vẫn 1,2%).
- Không có chữ học viên viết, chỉ có độ dài và điểm rubric do AI chấm (chưa kiểm lại bằng người).
- Không đo được câu giữa video (mới ghi từ 25/11), không đo được tốc độ xem.
- Học viên có thể đã sửa hiểu sai ngoài app (hỏi bạn, lên lớp) — data không thấy.
- So sánh nhóm đáp lại / không đáp là tương quan; nhóm đáp lại chỉ 31 người, tự chọn.
- Chưa biết UI có mời đáp lại rõ ràng không (nút trả lời ở đâu, lời xen vào có chặn video không).

- **Độ phủ thấp:** chỉ 220/721 (30,5%) dùng ≥3 ngày → số trên là hành vi của nhóm *có dùng*, lệch về phía người chăm hơn. Phần lớn học viên nhóm hỏi được chưa dùng trang này, nên phỏng vấn kiểm lại hành vi "sai → đọc đáp án → đi tiếp" ở mọi chỗ học trong khoá, nhánh pre-class chỉ hỏi người đã dùng ([interviews/SCRIPT.md](interviews/SCRIPT.md)).

→ **Kiểm lại bằng phỏng vấn ≥3 học viên cùng khoá:**
- Lần gần nhất bạn học AI xen vào giữa video, bạn làm gì? Vì sao không trả lời? (không thấy / không muốn ngắt mạch / câu hỏi không đáng / không biết trả lời ở đâu)
- Lần gần nhất sai câu ôn tập cuối ngày: đọc lời giải xong bạn làm gì? Có chắc mình đã hiểu chưa? Muốn được hỏi lại một câu tương tự không?
- Khi nào bạn thấy mình *thật sự* hiểu một ý trong pre-class?
