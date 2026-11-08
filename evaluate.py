#!/usr/bin/env python3
"""
Autoresearch Evaluation Harness v4 -- SHUFFLED PROMPT ORDER
=============================================================
Designed to reward QUALITY and DEEP THINKING, not just speed.

Key design principles:
- Hard problems that REQUIRE thinking to solve correctly
- Code is executed and verified against test cases
- Multi-step reasoning with strict answer validation
- Quality-heavy weighting: 65% quality, 20% speed, 15% memory
- Thinking prompts get a BONUS for using thinking mode
- Token efficiency: penalize bloated answers, reward concise correct ones

Composite = (quality * 0.65) + (avg_tps * 0.20) + (mem_eff * 0.15)
"""

import json
import time
import subprocess
import sys
import os
import urllib.request
import tempfile
import textwrap
import re
import random

OLLAMA_API = "http://localhost:11434"
MODEL_NAME = "autoresearch-candidate"
TIME_BUDGET = 300  # 5 minutes max


# ============================================================
# QUALITY SCORING FUNCTIONS
# ============================================================

def score_code_execution(response, test_code, expected_outputs, require_thinking=False, thinking_text=""):
    """Extract code, execute it, verify outputs. Score 0-100."""
    code_match = re.search(r"```python\s*\n(.*?)```", response, re.DOTALL)
    if not code_match:
        code_match = re.search(r"(def \w+.*?)(?:\n\n|\Z)", response, re.DOTALL)
    if not code_match:
        return 0, "No code found"

    code = code_match.group(1).strip()

    try:
        compile(code, "<eval>", "exec")
    except SyntaxError as e:
        return 5, f"Syntax error: {e}"

    full_code = code + "\n" + test_code
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(full_code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True, text=True, timeout=15
        )
    except subprocess.TimeoutExpired:
        os.unlink(tmp_path)
        return 10, "Execution timeout"
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if result.returncode != 0:
        return 15, f"Runtime error: {result.stderr[:200]}"

    output = result.stdout.strip()
    lines = output.split("\n")
    passed = 0
    for i, expected in enumerate(expected_outputs):
        if i < len(lines) and lines[i].strip() == str(expected):
            passed += 1

    if not expected_outputs:
        return 20, "No test cases"

    base_score = (passed / len(expected_outputs)) * 85

    # Thinking bonus: if problem requires thinking and model used it, +15
    if require_thinking and len(thinking_text) > 50:
        base_score += 15
    # Penalty: if problem requires thinking and model skipped it, cap at 70
    elif require_thinking and len(thinking_text) < 10 and base_score > 70:
        base_score = min(base_score, 70)

    return min(100, base_score), f"{passed}/{len(expected_outputs)} tests passed"


def score_factual(response, required_terms, forbidden_terms=None, exact_answer=None):
    """Score factual accuracy 0-100."""
    score = 0
    r = response.lower()

    if exact_answer and exact_answer.lower() in r:
        score += 60
    term_score = sum(1 for t in required_terms if t.lower() in r)
    if required_terms:
        score += (term_score / len(required_terms)) * 30
    if forbidden_terms:
        for term in forbidden_terms:
            if term.lower() in r:
                score -= 15

    word_count = len(response.split())
    if score >= 60 and word_count < 50:
        score += 10
    elif score >= 60 and word_count > 200:
        score -= 10

    return max(0, min(100, score))


def score_reasoning(response, correct_answer, reasoning_keywords, common_mistakes,
                    require_thinking=False, thinking_text=""):
    """Score reasoning with thinking bonus/penalty."""
    score = 0
    r = response.lower()

    if correct_answer.lower() in r:
        score += 40
    reasoning_found = sum(1 for kw in reasoning_keywords if kw.lower() in r)
    if reasoning_keywords:
        score += (reasoning_found / len(reasoning_keywords)) * 25
    for mistake in common_mistakes:
        if mistake.lower() in r:
            score -= 15

    word_count = len(response.split())
    if word_count < 150:
        score += 10
    elif word_count < 300:
        score += 5

    # Thinking bonus/penalty
    if require_thinking and len(thinking_text) > 100:
        score += 15  # Rewarded for using thinking on hard problems
    elif require_thinking and len(thinking_text) < 10 and score > 0:
        score = min(score, 50)  # Capped if skipped thinking on hard problem

    return max(0, min(100, score))


def score_creative(response, min_lines, max_lines, required_theme_words):
    """Score creative writing 0-100."""
    score = 0
    lines = [l.strip() for l in response.strip().split("\n") if l.strip()]
    r = response.lower()

    if min_lines <= len(lines) <= max_lines:
        score += 40
    elif len(lines) > 0:
        score += 15

    theme_found = sum(1 for w in required_theme_words if w.lower() in r)
    if required_theme_words:
        score += (theme_found / len(required_theme_words)) * 30

    if len(response) > 30 and not response.startswith("1."):
        score += 20

    meta_phrases = ["here is", "here's a", "sure,", "certainly", "of course"]
    if not any(phrase in r for phrase in meta_phrases):
        score += 10

    return max(0, min(100, score))


def score_debug(response, bug_description, fix_keywords, wrong_fixes):
    """Score debugging ability. Must identify bug AND propose correct fix."""
    score = 0
    r = response.lower()

    # Identifies the bug (40 points)
    if bug_description.lower() in r:
        score += 40
    else:
        # Partial credit for related terms
        related = sum(1 for kw in fix_keywords[:3] if kw.lower() in r)
        score += related * 10

    # Proposes correct fix (40 points)
    fix_found = sum(1 for kw in fix_keywords if kw.lower() in r)
    if fix_keywords:
        score += (fix_found / len(fix_keywords)) * 40

    # Avoids wrong fixes (20 points)
    for wrong in wrong_fixes:
        if wrong.lower() in r:
            score -= 10

    # No penalty, just bonus for not suggesting wrong things
    if not any(w.lower() in r for w in wrong_fixes):
        score += 20

    return max(0, min(100, score))


# ============================================================
# TEST PROMPTS -- 10 prompts, quality-focused
# ============================================================
PROMPTS = [
    # --- FAST / FACTUAL (no thinking needed) ---
    {
        "type": "short",
        "prompt": "What is the capital of the Philippines? Answer in one sentence.",
        "scorer": lambda r, t: score_factual(r, ["manila", "philippines"], exact_answer="Manila"),
        "weight": 0.5,
    },
    {
        "type": "short",
        "prompt": "What is 17 * 24? Show only the number.",
        "scorer": lambda r, t: score_factual(
            r, ["408"], exact_answer="408",
            forbidden_terms=["let me think", "step by step"]
        ),
        "weight": 0.5,
    },

    # --- CODE: MEDIUM DIFFICULTY (thinking should help) ---
    {
        "type": "code",
        "prompt": "Write a Python function called `longest_palindrome(s)` that returns the longest palindromic substring in s. For example: longest_palindrome('babad') should return 'bab' or 'aba', longest_palindrome('cbbd') should return 'bb'.",
        "scorer": lambda r, t: score_code_execution(r,
            test_code=textwrap.dedent("""\
                r1 = longest_palindrome("babad")
                print("True" if r1 in ("bab", "aba") else "False")
                print("True" if longest_palindrome("cbbd") == "bb" else "False")
                print("True" if longest_palindrome("a") == "a" else "False")
                print("True" if longest_palindrome("ac") in ("a", "c") else "False")
                r5 = longest_palindrome("racecar")
                print("True" if r5 == "racecar" else "False")
                print("True" if longest_palindrome("") == "" else "False")
            """),
            expected_outputs=["True"] * 6,
            require_thinking=True, thinking_text=t
        ),
        "weight": 2.5,
    },
    {
        "type": "code",
        "prompt": "Write a Python function called `flatten_nested(lst)` that takes an arbitrarily nested list and returns a flat list. Example: flatten_nested([1, [2, [3, 4], 5], 6]) returns [1, 2, 3, 4, 5, 6]. Handle any depth of nesting.",
        "scorer": lambda r, t: score_code_execution(r,
            test_code=textwrap.dedent("""\
                print(flatten_nested([1, [2, [3, 4], 5], 6]))
                print(flatten_nested([]))
                print(flatten_nested([1, 2, 3]))
                print(flatten_nested([[[[1]]]]))
                print(flatten_nested([1, [2], [[3]], [[[4]]]]))
            """),
            expected_outputs=[
                "[1, 2, 3, 4, 5, 6]",
                "[]",
                "[1, 2, 3]",
                "[1]",
                "[1, 2, 3, 4]",
            ],
            require_thinking=True, thinking_text=t
        ),
        "weight": 2.0,
    },
    {
        "type": "code",
        "prompt": "Write a Python function called `group_anagrams(words)` that takes a list of strings and groups anagrams together. Return a list of lists. Example: group_anagrams(['eat','tea','tan','ate','nat','bat']) returns [['eat','tea','ate'],['tan','nat'],['bat']] (order within groups and order of groups doesn't matter).",
        "scorer": lambda r, t: score_code_execution(r,
            test_code=textwrap.dedent("""\
                result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
                # Sort each group and sort groups for comparison
                result = [sorted(g) for g in result]
                result.sort()
                print(result)
                result2 = group_anagrams([""])
                print(result2)
                result3 = group_anagrams(["a"])
                print(result3)
            """),
            expected_outputs=[
                "[['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]",
                "[['']]",
                "[['a']]",
            ],
            require_thinking=True, thinking_text=t
        ),
        "weight": 2.0,
    },

    # --- REASONING: HARD (thinking is essential) ---
    {
        "type": "reasoning",
        "prompt": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost? Show your algebraic work step by step.",
        "scorer": lambda r, t: score_reasoning(
            r, "$0.05",
            reasoning_keywords=["0.05", "5 cents", "2x", "x + 1"],
            common_mistakes=["$0.10", "10 cents", "the ball costs 10"],
            require_thinking=True, thinking_text=t
        ),
        "weight": 2.0,
    },
    {
        "type": "reasoning",
        "prompt": "In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how many days would it take for the patch to cover half of the lake? Explain your reasoning.",
        "scorer": lambda r, t: score_reasoning(
            r, "47",
            reasoning_keywords=["doubles", "half", "day before", "47 days", "one day before"],
            common_mistakes=["24 days", "24"],
            require_thinking=True, thinking_text=t
        ),
        "weight": 2.0,
    },

    # --- DEBUGGING (requires careful analysis) ---
    {
        "type": "reasoning",
        "prompt": textwrap.dedent("""\
            This Python function is supposed to remove duplicates from a list while preserving order, but it has a bug. Find the bug and fix it.

            ```python
            def remove_duplicates(lst):
                seen = set()
                result = []
                for item in lst:
                    if item not in result:
                        result.append(item)
                return result
            ```

            What is the bug and what is the performance issue? How would you fix it?"""),
        "scorer": lambda r, t: score_debug(
            r,
            bug_description="seen",
            fix_keywords=["seen", "set", "o(n)", "o(1)", "lookup", "not in result is o(n)", "quadratic"],
            wrong_fixes=["no bug", "works correctly", "nothing wrong"]
        ),
        "weight": 2.0,
    },

    # --- CREATIVE (should be fast, no thinking) ---
    {
        "type": "creative",
        "prompt": "Write a haiku about the ocean. Just the haiku, nothing else.",
        "scorer": lambda r, t: score_creative(
            r, min_lines=3, max_lines=3,
            required_theme_words=["wave", "sea", "ocean", "salt", "tide", "shore", "deep", "blue", "water", "sand", "surf", "foam"]
        ),
        "weight": 1.0,
    },
    {
        "type": "creative",
        "prompt": "Write a 4-line poem about a programmer debugging code at 3am. Just the poem, nothing else.",
        "scorer": lambda r, t: score_creative(
            r, min_lines=3, max_lines=6,
            required_theme_words=["bug", "code", "screen", "night", "debug", "error", "line", "fix", "coffee", "light", "dark", "glow", "sleep"]
        ),
        "weight": 1.0,
    },
]


def stream_generate(model, prompt, think, options):
    """Stream tokens to terminal in real time. Return full response + metrics."""
    payload = {
        "model": model,
        "prompt": prompt,
        "think": think,
        "stream": True,
        "options": options,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{OLLAMA_API}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    response_text = ""
    thinking_text = ""
    in_thinking = False
    total_duration = 0
    eval_duration = 0
    eval_count = 0
    prompt_eval_duration = 0
    load_duration = 0
    first_token = True

    try:
        with urllib.request.urlopen(req, timeout=TIME_BUDGET) as resp:
            for raw_line in resp:
                chunk = json.loads(raw_line.decode())

                if chunk.get("thinking"):
                    if not in_thinking:
                        sys.stdout.write("\033[90m")  # gray
                        sys.stdout.write("  [thinking] ")
                        in_thinking = True
                    thinking_text += chunk["thinking"]
                    sys.stdout.write(".")
                    sys.stdout.flush()

                if chunk.get("response"):
                    if in_thinking:
                        sys.stdout.write(f" ({len(thinking_text)} chars)\033[0m\n")
                        sys.stdout.write("  [answer] ")
                        in_thinking = False
                    elif first_token:
                        sys.stdout.write("  [answer] ")
                        first_token = False
                    response_text += chunk["response"]
                    sys.stdout.write(chunk["response"])
                    sys.stdout.flush()

                if chunk.get("done"):
                    if in_thinking:
                        sys.stdout.write(f" ({len(thinking_text)} chars)\033[0m\n")
                    total_duration = chunk.get("total_duration", 0)
                    eval_duration = chunk.get("eval_duration", 0)
                    eval_count = chunk.get("eval_count", 0)
                    prompt_eval_duration = chunk.get("prompt_eval_duration", 0)
                    load_duration = chunk.get("load_duration", 0)
                    break

    except Exception as e:
        sys.stdout.write(f"\n  ERROR: {e}\n")
        return None

    sys.stdout.write("\n")
    sys.stdout.flush()

    return {
        "response": response_text,
        "thinking": thinking_text,
        "total_duration": total_duration,
        "eval_duration": eval_duration,
        "eval_count": eval_count,
        "prompt_eval_duration": prompt_eval_duration,
        "load_duration": load_duration,
    }


def get_vram():
    try:
        data = json.loads(
            urllib.request.urlopen(f"{OLLAMA_API}/api/ps", timeout=5).read()
        )
        if data.get("models"):
            return data["models"][0].get("size_vram", 0) / 1e9
    except Exception:
        pass
    return -1


def build_model(modelfile_content):
    modelfile_path = "/tmp/autoresearch-modelfile"
    with open(modelfile_path, "w") as f:
        f.write(modelfile_content)
    try:
        result = subprocess.run(
            ["ollama", "create", MODEL_NAME, "-f", modelfile_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"BUILD FAILED: {result.stderr}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"BUILD FAILED: {e}", file=sys.stderr)
        return False


def cleanup():
    try:
        subprocess.run(["ollama", "rm", MODEL_NAME], capture_output=True, timeout=10)
    except Exception:
        pass


def main():
    start_time = time.time()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import config

    modelfile = config.generate_modelfile()
    print(f"\n{'='*60}")
    print(f"AUTORESEARCH EVAL v4 -- {time.strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    print(f"  ctx={config.NUM_CTX} batch={config.NUM_BATCH} threads={config.NUM_THREAD}")
    print(f"  temp={config.TEMPERATURE} repeat={config.REPEAT_PENALTY} top_p={config.TOP_P}")
    print(f"  predict={config.NUM_PREDICT}")
    print(f"  think={config.THINK_MODE}")
    print(f"  scoring: quality 65% | speed 20% | memory 15%")
    print(f"{'='*60}\n")

    if not build_model(modelfile):
        print("RESULT:crash\t0\t0\t0\t0\t0\tBuild failed")
        return

    print("Warming up model...")
    try:
        req = urllib.request.Request(
            f"{OLLAMA_API}/api/generate",
            data=json.dumps({
                "model": MODEL_NAME, "prompt": "hi", "stream": False,
                "think": False, "options": {"num_ctx": 4096}
            }).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=300)
        print("Model ready.\n")
    except Exception as e:
        print(f"RESULT:crash\t0\t0\t0\t0\t0\tWarmup failed: {e}")
        cleanup()
        return

    # Clear log
    with open("last_run.log", "w") as logf:
        logf.write(f"AUTORESEARCH EVAL v4 -- {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        logf.write(f"Config: ctx={config.NUM_CTX} batch={config.NUM_BATCH} threads={config.NUM_THREAD}\n")
        logf.write(f"Think: {config.THINK_MODE}\n")
        logf.write(f"Scoring: quality 65% | speed 20% | memory 15%\n\n")

    options = {
        "num_ctx": config.NUM_CTX,
        "num_batch": config.NUM_BATCH,
        "num_thread": config.NUM_THREAD,
        "num_predict": config.NUM_PREDICT,
        "temperature": config.TEMPERATURE,
        "repeat_penalty": config.REPEAT_PENALTY,
        "top_p": config.TOP_P,
        "top_k": config.TOP_K,
        "min_p": config.MIN_P,
    }

    # v4: shuffle prompt order to eliminate position bias
    prompts_with_idx = list(enumerate(PROMPTS))
    random.shuffle(prompts_with_idx)
    prompt_order = [f"P{idx}" for idx, _ in prompts_with_idx]
    print(f"  Prompt order: {prompt_order}")

    results = []
    prompts_completed = []
    for seq, (orig_idx, prompt_def) in enumerate(prompts_with_idx):
        elapsed = time.time() - start_time
        if elapsed > TIME_BUDGET:
            print(f"\nTIME BUDGET EXCEEDED at prompt {seq+1}/{len(PROMPTS)} ({len(prompts_completed)}/{len(PROMPTS)} completed)")
            break

        think = config.THINK_MODE.get(prompt_def["type"], False)
        remaining = int(TIME_BUDGET - elapsed)

        print(f"\n[{seq+1}/{len(PROMPTS)}] P{orig_idx} {prompt_def['type'].upper()} (w={prompt_def['weight']}) ({remaining}s left)")
        print(f"  Q: {prompt_def['prompt'][:80]}...")

        data = stream_generate(MODEL_NAME, prompt_def["prompt"], think, options)

        if data is None:
            results.append({"eval_tps": 0, "quality": 0, "gen_tokens": 0,
                           "weight": prompt_def["weight"], "ttft_ms": 0,
                           "total_s": 0, "load_s": 0})
            continue

        response = data["response"]
        thinking = data["thinking"]
        ev_dur = max(data["eval_duration"], 1)
        eval_tps = data["eval_count"] / ev_dur * 1e9
        gen_tokens = data["eval_count"]

        # Score quality (pass thinking text for bonus/penalty)
        scorer_result = prompt_def["scorer"](response, thinking)
        if isinstance(scorer_result, tuple):
            quality, detail = scorer_result
        else:
            quality, detail = scorer_result, ""

        # Token efficiency: penalize extreme bloat on correct answers
        if quality >= 70 and gen_tokens > 0:
            if gen_tokens > 1500:
                quality = max(0, quality - 10)

        quality = max(0, min(100, quality))
        total_s = data["total_duration"] / 1e9
        ttft_ms = data["prompt_eval_duration"] / 1e6

        print(f"  --> Q:{quality:.0f}/100 | {eval_tps:.1f} tok/s | {gen_tokens} tok | {total_s:.1f}s | {detail}")

        result = {
            "eval_tps": eval_tps, "quality": quality, "gen_tokens": gen_tokens,
            "weight": prompt_def["weight"], "ttft_ms": ttft_ms,
            "total_s": total_s, "load_s": data["load_duration"] / 1e9,
            "detail": detail, "response_preview": response[:300],
        }
        results.append(result)
        prompts_completed.append(f"P{orig_idx}")

        # Log
        with open("last_run.log", "a") as logf:
            logf.write("=" * 60 + "\n")
            logf.write(f"[{seq+1}/{len(PROMPTS)}] P{orig_idx} {prompt_def['type']} | Q:{quality:.0f}/100 | {eval_tps:.1f} tok/s | {gen_tokens} tok | {total_s:.1f}s\n")
            logf.write(f"PROMPT: {prompt_def['prompt'][:200]}\n")
            logf.write(f"DETAIL: {detail}\n")
            logf.write(f"THINKING: {len(thinking)} chars\n")
            logf.write(f"RESPONSE:\n{response}\n\n")

    if not results:
        print("RESULT:crash\t0\t0\t0\t0\t0\tNo results")
        cleanup()
        return

    total_weight = sum(r["weight"] for r in results)
    avg_tps = sum(r["eval_tps"] * r["weight"] for r in results) / total_weight
    quality = sum(r["quality"] * r["weight"] for r in results) / total_weight
    vram_gb = get_vram()
    mem_eff = max(0, 100 * (1 - vram_gb / 64)) if vram_gb > 0 else 50

    # Quality-heavy composite
    composite = (quality * 0.65) + (avg_tps * 0.20) + (mem_eff * 0.15)

    total_time = time.time() - start_time
    avg_ttft = sum(r.get("ttft_ms", 0) for r in results) / len(results)

    print(f"\n{'='*60}")
    print(f"EVAL COMPLETE in {total_time:.1f}s ({len(prompts_completed)}/{len(PROMPTS)} prompts)")
    print(f"  avg_tps:     {avg_tps:.1f}")
    print(f"  quality:     {quality:.1f}/100")
    print(f"  mem_eff:     {mem_eff:.1f}/100")
    print(f"  vram_gb:     {vram_gb:.1f}")
    print(f"  avg_ttft_ms: {avg_ttft:.0f}")
    print(f"  COMPOSITE:   {composite:.2f}")
    print(f"{'='*60}")
    print(f"RESULT:{composite:.2f}\t{avg_tps:.1f}\t{quality:.0f}\t{mem_eff:.0f}\t{vram_gb:.1f}\t{total_time:.0f}\t{avg_ttft:.0f}")

    # Log to results.tsv
    try:
        import subprocess as _sp
        _commit = _sp.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
        _msg = _sp.run(["git", "log", "-1", "--pretty=%s"], capture_output=True, text=True).stdout.strip()
        _tsv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.tsv")
        _header = not os.path.exists(_tsv)
        with open(_tsv, "a") as _f:
            if _header:
                _f.write("timestamp\tcommit\tcomposite\tavg_tps\tquality\tmem_eff\tvram_gb\ttime_s\tavg_ttft_ms\tdescription\n")
            _ts = time.strftime("%Y-%m-%d %H:%M:%S")
            _f.write(f"{_ts}\t{_commit}\t{composite:.2f}\t{avg_tps:.1f}\t{quality:.0f}\t{mem_eff:.0f}\t{vram_gb:.1f}\t{total_time:.0f}\t{avg_ttft:.0f}\t{_msg}\n")
            print(f"LOGGED to results.tsv: {_ts} | composite={composite:.2f} | {_msg}")
    except Exception as _e:
        print(f"LOGGING ERROR: {_e}")

    cleanup()


if __name__ == "__main__":
    main()
