"""The scoring functions inside the locked eval (evaluate.py). No model and no Ollama needed."""
import evaluate

GOOD_CODE = "```python\ndef add(a, b):\n    return a + b\n```"
TEST_CODE = "print(add(1, 2))\nprint(add(-1, 1))"


def test_code_that_passes_every_case_scores_85_without_thinking():
    score, detail = evaluate.score_code_execution(GOOD_CODE, TEST_CODE, ["3", "0"])
    assert score == 85
    assert detail == "2/2 tests passed"


def test_thinking_bonus_lifts_a_full_pass_to_100():
    score, _ = evaluate.score_code_execution(
        GOOD_CODE, TEST_CODE, ["3", "0"], require_thinking=True, thinking_text="x" * 60
    )
    assert score == 100


def test_skipped_thinking_caps_a_hard_problem_at_70():
    score, _ = evaluate.score_code_execution(
        GOOD_CODE, TEST_CODE, ["3", "0"], require_thinking=True, thinking_text=""
    )
    assert score == 70


def test_no_code_and_syntax_errors_score_low():
    assert evaluate.score_code_execution("no code here", TEST_CODE, ["3"])[0] == 0
    assert evaluate.score_code_execution("```python\ndef add(:\n```", TEST_CODE, ["3"])[0] == 5


def test_wrong_output_scores_by_cases_passed():
    wrong = "```python\ndef add(a, b):\n    return a - b\n```"
    score, detail = evaluate.score_code_execution(wrong, TEST_CODE, ["3", "0"])
    assert detail == "0/2 tests passed"
    assert score == 0


def test_factual_rewards_the_exact_answer_and_brevity():
    assert evaluate.score_factual("The answer is Canberra.", ["canberra"], exact_answer="Canberra") == 100
    assert evaluate.score_factual("Sydney, I think.", ["canberra"], forbidden_terms=["sydney"]) == 0


def test_reasoning_penalizes_the_common_wrong_answer():
    right = evaluate.score_reasoning("It costs 5 cents, because 1.05 - 1.00 = 0.05.", "5 cents", ["0.05"], ["10 cents"])
    wrong = evaluate.score_reasoning("It costs 10 cents.", "5 cents", ["0.05"], ["10 cents"])
    assert right > wrong
    assert wrong == 0


def test_creative_wants_the_line_count_and_no_preamble():
    poem = "salt on the board\nthe swell comes in grey\nwe paddle anyway\nthe sun breaks late"
    good = evaluate.score_creative(poem, 3, 5, ["swell", "salt"])
    chatty = evaluate.score_creative("Sure, here is a poem: " + poem, 3, 5, ["swell", "salt"])
    assert good == 100
    assert chatty < good


def test_debug_needs_the_bug_and_the_fix():
    full = evaluate.score_debug("Off by one: use range(len(xs)) and fix the index.", "off by one", ["range", "index"], ["delete the loop"])
    none = evaluate.score_debug("Just delete the loop.", "off by one", ["range", "index"], ["delete the loop"])
    assert full == 100
    assert none == 0


def test_eval_v4_has_ten_prompts_and_a_five_minute_budget():
    kinds = sorted(p["type"] for p in evaluate.PROMPTS)
    assert kinds == ["code"] * 3 + ["creative"] * 2 + ["reasoning"] * 3 + ["short"] * 2
    assert evaluate.TIME_BUDGET == 300
    assert evaluate.OLLAMA_API == "http://localhost:11434"
