"""The numbers the README quotes, checked against RESULTS.md so the two cannot drift apart."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rows():
    out = []
    for line in (ROOT / "RESULTS.md").read_text().splitlines():
        if re.match(r"^\| \d+ \|", line):
            out.append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def test_119_experiments():
    assert "**119 experiments**" in (ROOT / "RESULTS.md").read_text()
    assert len(rows()) == 119


def test_the_eval_saturates():
    v3 = [r for r in rows() if r[5] == "qwen3.5-27b" and r[6] == "v3"]
    tied = [r for r in v3 if float(r[2]) >= 76.19]
    assert len(v3) == 82
    assert len(tied) == 45
    assert {r[3] for r in tied} == {"100"}  # quality pinned at the ceiling
    assert {r[4] for r in tied} <= {"9.5", "9.6"}  # speed inside the noise
    assert max(float(r[2]) for r in rows()) == 76.2


def test_the_jump_came_from_the_system_prompt():
    by_n = {int(r[0]): r for r in rows()}
    best_before = max(float(by_n[n][2]) for n in range(1, 9))
    assert best_before == 58.85
    assert float(by_n[9][2]) == 76.19 and by_n[9][3] == "100"
    assert "system prompt" in by_n[9][13]
    assert float(by_n[20][2]) == 76.19 and "empty system prompt" in by_n[20][13]


def test_results_tsv_keeps_every_run():
    lines = (ROOT / "results.tsv").read_text().splitlines()[1:]
    runs = [line.split("\t") for line in lines if line.strip()]
    assert len(runs) == 215
    distilled = [r for r in runs if r[9] == "opus-distilled"]
    assert len(runs) - len(distilled) == 83
    assert max(float(r[2]) for r in distilled) == 63.7
    full = (ROOT / "results_full.tsv").read_text().splitlines()[1:]
    assert len([line for line in full if line.strip()]) == 119


def test_the_smaller_numbers_the_readme_quotes():
    by_n = {int(r[0]): r for r in rows()}
    assert float(by_n[3][2]) == 58.85 and by_n[3][3] == "73"  # best before run 9, quality 73
    assert float(by_n[8][2]) == 23.02 and by_n[8][3] == "18"
    assert "Think briefly, then answer" in by_n[8][13]
    assert float(by_n[10][2]) == 23.01 and by_n[10][3] == "18"
    assert "Be concise." in by_n[10][13]


def test_83_qwen_runs_then_96_after_the_table():
    lines = (ROOT / "results.tsv").read_text().splitlines()[1:]
    runs = [line.split("\t") for line in lines if line.strip()]
    qwen = [r for r in runs if r[9] == "qwen3.5-27b"]
    assert len(qwen) == 83
    assert [r[10] for r in qwen].count("v2") == 1 and [r[10] for r in qwen].count("v3") == 82
    full = [line.split("\t") for line in (ROOT / "results_full.tsv").read_text().splitlines()[1:] if line.strip()]
    last_tabled = full[-1][0]
    later = [r for r in runs if r[0] > last_tabled]
    assert len(later) == 96
    assert {r[9] for r in later} == {"opus-distilled"}
    assert max(float(r[2]) for r in later) <= 63.7
