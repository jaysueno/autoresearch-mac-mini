# AGENTS.md

Instructions for an AI coding agent working in this repo. If you are the experiment agent running
the tuning loop, your instructions are `program.md`, not this file.

## Install, run, test

- Install: `python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`
- Run one experiment (needs Ollama on `localhost:11434` and the model in `config.py`):
  `.venv/bin/python3 run.py`. `run.py --baseline` records the score to beat; `run.py --loop`
  runs until stopped.
- Test: `.venv/bin/python -m pytest` (the same `pytest` run CI uses). No model or Ollama needed.
  It must pass before every commit.

## Where you may work

- `tests/`: add tests freely.
- `README.md`, `AGENTS.md`, `requirements-dev.txt`, `.github/`.
- `config.py`, but only during a tuning run, one knob per commit, as `program.md` says.

## What you must never do

- Never edit `evaluate.py`. It is the locked eval; changing it makes every earlier score
  meaningless.
- Never edit `results.tsv`, `results_full.tsv` or `RESULTS.md` by hand. They are the record of
  the run, and `tests/test_results_data.py` pins the numbers the README quotes.
- Never change `MODEL_BASE`, `NUM_CTX` (32768) or thinking mode for code and reasoning.
- Never commit `.venv/`, `last_run.log`, or `.claude/settings.local.json`.
- Never push or change repository settings unless your human asks.

## Before every commit

Run an identity and secret scan over the tree and the git history: no real names, addresses,
tokens, hosts or ids. The maintainer runs one outside this repo; if you have no scanner, at least
grep the diff for `@`, `token`, `key`, IP addresses and long hex strings, and read every hit.
