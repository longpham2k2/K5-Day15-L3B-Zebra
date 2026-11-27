"""Tự kiểm bốn công cụ tra cứu bằng dữ liệu mẫu của repo."""

import json

from tools import DATA_DIR, check_answer, get_passage, get_similar_question, learner_state


def main() -> None:
    kc_code = "rag_bm25_vs_embedding"
    missing_id = "__khong_ton_tai__"

    with (DATA_DIR / "question_bank.json").open(encoding="utf-8-sig") as source:
        bank = json.load(source)
    concept = next(item for item in bank["concepts"] if item["kc_code"] == kc_code)
    questions = {item["id"]: item for item in concept["questions"]}

    assert learner_state("T01") == {
        "kc_code": kc_code,
        "question_id": "Q1",
        "chosen": "C",
        "times_wrong": 1,
    }, "learner_state: sai dữ liệu lượt T01"
    assert learner_state(missing_id) == {}, "learner_state: thiếu lượt phải trả {}"

    passages = [{"code": item["code"], "text": item["text"]} for item in concept["passages"]]
    assert passages and get_passage(kc_code) == passages, "get_passage: sai đoạn bài"
    assert get_passage(missing_id) == [], "get_passage: thiếu ý kiến thức phải trả []"

    for exclude_id, expected_id in (("Q1", "Q1-S1"), ("Q1-S1", "Q1-S2")):
        expected = {key: questions[expected_id][key] for key in ("id", "stem", "options")}
        assert get_similar_question(kc_code, exclude_id) == expected, (
            f"get_similar_question: phải trả đúng dữ liệu công khai của {expected_id}"
        )
    assert get_similar_question(missing_id, "Q1") is None, (
        "get_similar_question: thiếu ý kiến thức phải trả None"
    )

    original = questions["Q1"]
    for chosen, correct in (("B", True), ("C", False)):
        assert check_answer("Q1", chosen) == {
            "correct": correct,
            "answer": original["answer"],
            "explanation": original["explanation"],
        }, f"check_answer: sai kết quả cho lựa chọn {chosen}"
    assert check_answer(missing_id, "B") == {"correct": False, "error": "không có câu"}, (
        "check_answer: thiếu câu hỏi phải trả lỗi tra cứu"
    )

    print("OK - all 4 tools passed, including not-found cases.")


if __name__ == "__main__":
    main()
