"""Công cụ tra cứu cục bộ cho vòng hỏi lại trong spec.md §4."""
from __future__ import annotations

import json
from pathlib import Path

from tracing import TOOLS, tool  # noqa: F401

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _read_data(filename: str):
    with (DATA_DIR / filename).open(encoding="utf-8-sig") as source:
        return json.load(source)


def _get_concept(kc_code: str) -> dict:
    concepts = _read_data("question_bank.json")["concepts"]
    return next((concept for concept in concepts if concept["kc_code"] == kc_code), {})


@tool
def learner_state(attempt_id: str) -> dict:
    """learner_state — tra lượt trả lời sai đã lưu.

    Input: mã lượt trả lời attempt_id.
    Output: kc_code, question_id, chosen, times_wrong, cộng stem (đề câu gốc) và
    misconception (ghi chú hiểu sai của đáp án đã chọn, "" nếu không có), hoặc {} nếu thiếu lượt.
    Không trả answer / explanation của câu gốc.
    Tác động ra ngoài: Không.
    """
    for attempt in _read_data("learner_states.json"):
        if attempt["attempt_id"] == attempt_id:
            state = {key: attempt[key] for key in ("kc_code", "question_id", "chosen", "times_wrong")}
            question = next((q for q in _get_concept(attempt["kc_code"]).get("questions", [])
                             if q["id"] == attempt["question_id"]), {})
            state["stem"] = question.get("stem", "")
            state["misconception"] = question.get("misconception", {}).get(attempt["chosen"], "")
            return state
    return {}


@tool
def get_passage(kc_code: str) -> list[dict]:
    """get_passage — tra đoạn bài theo ý kiến thức.

    Input: mã ý kiến thức kc_code.
    Output: danh sách đoạn gồm code và text, hoặc [] nếu thiếu căn cứ.
    Tác động ra ngoài: Không.
    """
    passages = _get_concept(kc_code).get("passages", [])
    return [{"code": passage["code"], "text": passage["text"]} for passage in passages]


@tool
def get_similar_question(kc_code: str, exclude_id: str) -> dict | None:
    """get_similar_question — lấy một câu tương tự từ ngân hàng.

    Input: mã ý kiến thức kc_code và mã câu gốc exclude_id.
    Output: chỉ id, stem và options của câu tương tự đầu tiên khác exclude_id,
    hoặc None nếu thiếu câu phù hợp.
    Nhóm duyệt nội dung trước khi thêm vào ngân hàng dưới role tuong_tu.
    Tác động ra ngoài: Không.
    """
    concept = _get_concept(kc_code)
    for question in concept.get("questions", []):
        if question["role"] == "tuong_tu" and question["id"] != exclude_id:
            return {key: question[key] for key in ("id", "stem", "options")}
    return None


@tool
def check_answer(question_id: str, chosen: str) -> dict:
    """check_answer — đối chiếu lựa chọn với đáp án đã lưu.

    Input: mã câu question_id và mã lựa chọn đã nộp chosen.
    Output: correct (bool), answer và explanation lấy từ JSON, hoặc
    {"correct": False, "error": "không có câu"} nếu thiếu câu.
    Chỉ luồng Python gọi sau khi nộp lựa chọn.
    Tác động ra ngoài: Không.
    """
    for concept in _read_data("question_bank.json")["concepts"]:
        for question in concept["questions"]:
            if question["id"] == question_id:
                return {
                    "correct": chosen == question["answer"],
                    "answer": question["answer"],
                    "explanation": question["explanation"],
                }
    return {"correct": False, "error": "không có câu"}
