#!/usr/bin/env python3
"""
Autoresearch Runner -- Executes the experiment loop
====================================================
Usage:
  python3 run.py              # Run one experiment (for testing)
  python3 run.py --loop       # Run forever (autonomous mode)
  python3 run.py --baseline   # Run baseline and record it

This script is the harness. It:
1. Runs evaluate.py
2. Parses the RESULT line
3. Compares to best known score
4. Keeps or reverts the commit
5. Logs to results.tsv
"""

import subprocess
import sys
import os
import time
from datetime import datetime

RESULTS_FILE = "results.tsv"
TSV_HEADER = "timestamp\tcommit\tcomposite\tavg_tps\tquality\tmem_eff\tvram_gb\ttime_s\tavg_ttft_ms\tstatus\tdescription"


def get_commit_hash():
    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip()


def get_commit_msg():
    return subprocess.run(
        ["git", "log", "-1", "--pretty=%s"],
        capture_output=True, text=True
    ).stdout.strip()


def get_best_score():
    if not os.path.exists(RESULTS_FILE):
        return 0.0
    best = 0.0
    with open(RESULTS_FILE) as f:
        for line in f:
            if line.startswith("timestamp") or line.strip() == "":
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 3 and parts[9] == "keep":
                try:
                    score = float(parts[2])
                    best = max(best, score)
                except ValueError:
                    pass
    return best


def run_evaluate():
    """Run evaluate.py and return the RESULT line."""
    print("Running evaluation...")
    result = subprocess.run(
        [sys.executable, "evaluate.py"],
        capture_output=True, text=True, timeout=600
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[:500])

    # Find RESULT line
    for line in result.stdout.split("\n"):
        if line.startswith("RESULT:"):
            return line[7:]  # strip "RESULT:" prefix
    return None


def log_result(commit, result_parts, status, description):
    """Append to results.tsv."""
    write_header = not os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, "a") as f:
        if write_header:
            f.write(TSV_HEADER + "\n")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{ts}\t{commit}\t{result_parts}\t{status}\t{description}\n")


def run_one():
    """Run a single experiment."""
    commit = get_commit_hash()
    description = get_commit_msg()
    best_score = get_best_score()

    print(f"\n{'='*60}")
    print(f"EXPERIMENT: {commit} -- {description}")
    print(f"Best score so far: {best_score:.2f}")
    print(f"{'='*60}\n")

    result_line = run_evaluate()

    if result_line is None or result_line.startswith("crash"):
        print("\nEXPERIMENT CRASHED")
        log_result(commit, result_line or "0\t0\t0\t0\t0\t0\t0", "crash", description)
        return "crash", 0.0

    parts = result_line.split("\t")
    composite = float(parts[0])

    print(f"\nComposite score: {composite:.2f} (best: {best_score:.2f})")

    if composite > best_score:
        print(f"NEW BEST! +{composite - best_score:.2f} improvement")
        log_result(commit, result_line, "keep", description)
        return "keep", composite
    else:
        print(f"No improvement ({composite:.2f} <= {best_score:.2f}). Reverting.")
        log_result(commit, result_line, "discard", description)
        return "discard", composite


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if "--baseline" in sys.argv:
        print("RECORDING BASELINE")
        print("This will not revert -- it sets the score to beat.\n")
        status, score = run_one()
        print(f"\nBaseline recorded: {score:.2f}")
        return

    if "--loop" in sys.argv:
        print("AUTONOMOUS MODE -- Running until manually stopped (Ctrl+C)")
        experiment_num = 0
        while True:
            experiment_num += 1
            print(f"\n\n{'#'*60}")
            print(f"EXPERIMENT #{experiment_num}")
            print(f"{'#'*60}")
            status, score = run_one()
            print(f"\nStatus: {status} | Score: {score:.2f}")
            print("Cooling down for 10 seconds...")
            time.sleep(10)
    else:
        status, score = run_one()
        print(f"\nFinal: {status} | Score: {score:.2f}")


if __name__ == "__main__":
    main()
