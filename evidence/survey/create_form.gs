/**
 * Tạo Google Form khảo sát A4 — nội dung và số câu khớp evidence/survey/questions.md (bản 2).
 *
 * Cách chạy:
 *   1. Mở https://script.google.com bằng tài khoản Google sẽ sở hữu form → "Dự án mới".
 *   2. Xoá code mẫu, dán toàn bộ file này, bấm Lưu.
 *   3. Chọn hàm taoFormKhaoSat → Chạy → tự cấp quyền cho script (Forms, Sheets).
 *   4. Mở "Nhật ký thực thi": có link gửi người làm, link sửa form, link Sheet phản hồi.
 *   Chạy lại sẽ tạo thêm một form MỚI (không sửa form cũ) — xoá form thừa trong Drive nếu có.
 *
 * Trang và nhánh (số câu không bao giờ chạy lùi):
 *   Phần 1 câu 1 → Phần 2 câu 2 → Phần 3 câu 3–6 → [câu 6b] → Phần 4 câu 7–8 → Phần 5 câu 9 → [câu 10] → [câu 10b] → Phần 6 câu 11
 *   câu 2  = "Không nhớ / chưa gặp"                  → bỏ Phần 3 và 6b, sang Phần 4
 *   câu 6  = "Có, và mình lại vướng"                  → câu 6b, còn lại → Phần 4
 *   câu 9  = "3–5 ngày" / "Trên 5 ngày"               → câu 10, còn lại → Phần 6
 *   câu 10 = "Đọc nhưng không trả lời" / "Lướt qua…"  → câu 10b, còn lại → Phần 6
 *
 * Không thu email, không bắt đăng nhập. Nếu giao diện Forms có nút "Xuất bản" thì bấm để form nhận phản hồi.
 * Làm tay sau khi tạo: câu 3 → ⋮ → "Trộn thứ tự tuỳ chọn".
 */
function taoFormKhaoSat() {
  var form = FormApp.create('KHẢO SÁT ẨN DANH: CÁCH HỌC VÀ ÔN TRONG KHOÁ AI20K');
  form.setDescription([
    'Xin chào! Nhóm mình là học viên AI20K khoá 5, đang tìm hiểu chuyện gì xảy ra sau khi mình trả lời sai ' +
      'hoặc hiểu sai một ý trong khoá: mình làm gì tiếp, có kiểm lại không, và nó tốn của mình những gì.',
    '',
    '• Khoảng 3 phút, 11 câu, phần lớn là chọn đáp án.',
    '• Câu hỏi đều về lần gần nhất đã xảy ra. Không có đúng / sai, không nhớ thì cứ chọn "Không nhớ".',
    '• Ẩn danh: không hỏi tên, email hay điểm. Kết quả chỉ dùng cho bài hackathon và chỉ báo cáo dạng tổng hợp ' +
      '(vd "12/25 người"), không công khai từng câu trả lời.',
    '',
    'Cảm ơn bạn đã dành thời gian!'
  ].join('\n'));
  try { form.setCollectEmail(false); } catch (e) { Logger.log('Không tắt được thu email: ' + e); }
  try { form.setRequireLogin(false); } catch (e) { /* chỉ có ở tài khoản Workspace */ }
  form.setLimitOneResponsePerUser(false);   // bật cái này sẽ bắt đăng nhập
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setProgressBar(true);
  form.setConfirmationMessage('Cảm ơn bạn! Nếu bạn để lại liên hệ ở câu cuối, nhóm sẽ nhắn hẹn trong 1–2 ngày tới.');

  var CONTINUE = FormApp.PageNavigationType.CONTINUE;

  // ---------- Phần 1 · Về bạn ----------
  form.addMultipleChoiceItem()
    .setTitle('Câu 1. Bạn đang là:')
    .setRequired(true)
    .setChoiceValues([
      'Học viên lớp L3A',
      'Học viên lớp L3B',
      'Học viên lớp khác của khoá 5',
      'Lab coach / TA / giảng viên',
      'Khác'
    ]);

  // ---------- Phần 2 · Lần hiểu sai gần nhất ----------
  form.addPageBreakItem()
    .setTitle('Phần 2 · Lần hiểu sai gần nhất')
    .setHelpText('Ở bất kỳ đâu trong khoá: câu hỏi trên lớp, quiz, câu ôn tập, lab, bài nhóm…');
  var q2 = form.addMultipleChoiceItem()
    .setTitle('Câu 2. Lần gần nhất bạn trả lời sai, hoặc nhận ra mình hiểu sai một ý trong khoá, là khi nào?')
    .setRequired(true);

  // ---------- Phần 3 · Sau lần hiểu sai đó ----------
  form.addPageBreakItem()
    .setTitle('Phần 3 · Sau lần hiểu sai đó')
    .setHelpText('Các câu dưới đây hỏi về đúng lần bạn vừa nghĩ tới ở câu 2.');
  form.addCheckboxItem()
    .setTitle('Câu 3. Ngay sau khi biết mình sai, bạn đã làm gì?')
    .setHelpText('Chọn tất cả những gì bạn đã làm.')
    .setChoiceValues([
      'Đọc đáp án / lời giải rồi học tiếp',
      'Xem lại slide / video / tài liệu',
      'Hỏi trợ giảng AI trong trang học của khoá',
      'Hỏi ChatGPT hoặc một AI khác bên ngoài',
      'Hỏi bạn học / lab coach / giảng viên',
      'Làm thêm một câu hoặc bài tương tự',
      'Bỏ qua, chưa làm gì'
    ])
    .showOtherOption(true);
  form.addMultipleChoiceItem()
    .setTitle('Câu 4. Sau đó, bạn đã kiểm lại xem mình hiểu ý đó chưa?')
    .setHelpText('Ví dụ: làm một câu khác cùng ý, giải thích lại cho ai đó, dùng lại trong lab.')
    .setChoiceValues(['Có, ngay trong ngày', 'Có, vài ngày sau', 'Chưa kiểm lại', 'Không nhớ']);
  form.addCheckboxItem()
    .setTitle('Câu 5. Lần hiểu sai đó đã khiến bạn mất gì?')
    .setHelpText('Chọn tất cả những gì đúng với bạn.')
    .setChoiceValues([
      'Không mất gì đáng kể',
      'Mất thời gian tìm lại tài liệu hoặc hỏi lại',
      'Làm lab / bài tập sai, phải sửa lại',
      'Bị hỏi trên lớp mà không trả lời được',
      'Làm bài nhóm chậm hoặc sai, ảnh hưởng tới bạn cùng nhóm'
    ])
    .showOtherOption(true);
  var q6 = form.addMultipleChoiceItem()
    .setTitle('Câu 6. Sau đó, ý đó có quay lại làm bạn vướng không?')
    .setHelpText('Buổi sau, lab, bài nhóm…')
    .setRequired(true);

  // ---------- Câu 6b ----------
  var p6b = form.addPageBreakItem().setTitle('Phần 3 · Lần vướng lại');
  form.addMultipleChoiceItem()
    .setTitle('Câu 6b. Lần vướng lại đó bạn mất thêm khoảng bao lâu?')
    .setChoiceValues(['Dưới 5 phút', '5–15 phút', '16–30 phút', 'Trên 30 phút', 'Không nhớ']);

  // ---------- Phần 4 · Trong 7 ngày gần đây ----------
  var p4 = form.addPageBreakItem().setTitle('Phần 4 · Trong 7 ngày gần đây');
  form.addMultipleChoiceItem()
    .setTitle('Câu 7. Trong 7 ngày gần đây, khoảng mấy lần bạn sai / hiểu sai một ý mà không chắc sau đó mình đã hiểu lại?')
    .setRequired(true)
    .setChoiceValues(['0 lần', '1 lần', '2–3 lần', '4–6 lần', '7 lần trở lên', 'Không nhớ']);
  form.addParagraphTextItem()
    .setTitle('Câu 8. Ở lần hiểu sai gần nhất, điều gì khiến bạn khó chịu hoặc tốn công nhất?')
    .setHelpText('Không bắt buộc.');

  // ---------- Phần 5 · Trang pre-class ----------
  form.addPageBreakItem().setTitle('Phần 5 · Trang pre-class');
  var q9 = form.addMultipleChoiceItem()
    .setTitle('Câu 9. Từ đầu khoá tới giờ, bạn đã học trên trang pre-class khoảng bao nhiêu ngày?')
    .setRequired(true);

  // ---------- Câu 10 ----------
  var p10 = form.addPageBreakItem().setTitle('Phần 5 · Bạn học AI trên trang pre-class');
  var q10 = form.addMultipleChoiceItem()
    .setTitle('Câu 10. Lần gần nhất một "bạn học AI" tự nói chen vào lúc bạn đang học trên trang pre-class, bạn đã làm gì?')
    .setRequired(true);

  // ---------- Câu 10b ----------
  var p10b = form.addPageBreakItem().setTitle('Phần 5 · Lần đó');
  form.addParagraphTextItem()
    .setTitle('Câu 10b. Lúc đó điều gì khiến bạn không trả lời?')
    .setHelpText('Không bắt buộc.');

  // ---------- Phần 6 · Kết thúc ----------
  var p6 = form.addPageBreakItem().setTitle('Phần 6 · Kết thúc');
  form.addTextItem()
    .setTitle('Câu 11. Bạn có sẵn lòng cho nhóm hỏi thêm 10–15 phút về lần học gần nhất không?')
    .setHelpText('Không bắt buộc. Nếu có, để lại Discord hoặc Zalo bạn muốn được liên hệ; không thì bỏ trống.');

  // ---------- Chia nhánh (đặt sau khi đã có đủ trang) ----------
  q2.setChoices([
    q2.createChoice('Hôm nay', CONTINUE),
    q2.createChoice('1–3 ngày trước', CONTINUE),
    q2.createChoice('4–7 ngày trước', CONTINUE),
    q2.createChoice('Hơn 1 tuần trước', CONTINUE),
    q2.createChoice('Không nhớ / chưa gặp lần nào', p4)
  ]);
  q6.setChoices([
    q6.createChoice('Có, và mình lại vướng', p6b),
    q6.createChoice('Có, nhưng lúc đó mình đã nắm', p4),
    q6.createChoice('Chưa gặp lại', p4),
    q6.createChoice('Không nhớ', p4)
  ]);
  q9.setChoices([
    q9.createChoice('Chưa bao giờ', p6),
    q9.createChoice('1–2 ngày', p6),
    q9.createChoice('3–5 ngày', p10),
    q9.createChoice('Trên 5 ngày', p10),
    q9.createChoice('Không nhớ', p6)
  ]);
  q10.setChoices([
    q10.createChoice('Không để ý / không thấy nó nói gì', p6),
    q10.createChoice('Đọc nhưng không trả lời', p10b),
    q10.createChoice('Lướt qua rồi xem tiếp', p10b),
    q10.createChoice('Trả lời lại nó', p6),
    q10.createChoice('Không nhớ', p6)
  ]);

  // ---------- Sheet nhận phản hồi ----------
  var ss = SpreadsheetApp.create('Khảo sát A4 — phản hồi (bản gốc, KHÔNG commit)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('Link gửi người làm: ' + form.getPublishedUrl());
  Logger.log('Link sửa form:      ' + form.getEditUrl());
  Logger.log('Sheet phản hồi:     ' + ss.getUrl());
}
