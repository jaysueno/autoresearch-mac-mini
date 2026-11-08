# Autoresearch: Qwen 3.5 27B on M4 Pro 64GB

> Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch).
> The human iterates on the prompt (this file).
> The AI agent iterates on the config (config.py).
> The goal: find the optimal Ollama inference config for Qwen 3.5 27B.

## Hardware

- Apple Mac Mini M4 Pro, 64GB unified memory, 273 GB/s bandwidth
- macOS, Ollama 0.18.2
- Model: qwen3.5:27b (Q4_K_M, 17GB weights)

## The Loop

Run this loop FOREVER until manually stopped:

1. Read the current config.py and results.tsv
2. Plan an experiment: change ONE thing in config.py
3. Git commit the change with a descriptive message
4. Run: .venv/bin/python3 evaluate.py 2>&1
5. Read the RESULT line from the output
6. If no RESULT line = crash. Read the error. Try to fix.
7. Compare composite score to the best score so far
8. If composite_score IMPROVED (higher is better): keep the commit
9. If composite_score is EQUAL or WORSE: git reset --hard HEAD~1
10. Push to GitHub: git push origin main
11. Go to step 1

## Constraints (DO NOT CHANGE THESE)

- NUM_CTX must stay at 32768. Real-world use cases (OpenClaw agent, document analysis, multi-turn conversations) require large context windows.
- THINK_MODE for "code" and "reasoning" must stay True. Deep thinking is the whole point of this model. The eval rewards thinking and penalizes skipping it.
- Do NOT change MODEL_BASE. We are optimizing config, not swapping models.
- Do NOT modify evaluate.py. It is the locked evaluation harness.

## What You CAN Change in config.py

- NUM_BATCH (batch size for prompt eval)
- NUM_THREAD (CPU threads)
- NUM_PREDICT (max output tokens)
- TEMPERATURE
- REPEAT_PENALTY
- TOP_P, TOP_K, MIN_P
- SYSTEM_PROMPT (the system prompt text)
- THINK_MODE for "short" and "creative" (can toggle these)

## Rules

- Do NOT pause to ask the human. Work indefinitely.
- ONLY modify config.py -- that is your playground.
- Each experiment has a 5-minute wall clock budget (enforced by evaluate.py).
- Change ONE thing at a time so you know what helped.
- If stuck, read results.tsv history for patterns.
- After each keep or revert, push to GitHub.

## Scoring (v3)

Composite = (quality * 0.65) + (avg_tps * 0.20) + (mem_eff * 0.15)

- quality: 0-100. Code is executed and verified. Reasoning checks for correct answers. Thinking mode gives a +15 bonus on hard problems, and a penalty if skipped.
- avg_tps: generation tokens/second (higher = better, max ~18 on M4 Pro)
- mem_eff: 100 * (1 - vram_gb / 64) -- less memory = better

## Simplicity Rule

- A tiny score improvement that adds complexity? Probably not worth it.
- Equal score but simpler config? Keep it.
- The best config is the one that works well AND is easy to understand.

## Starting Point

The baseline config in config.py has thinking ON for code and reasoning. Beat the baseline score by optimizing sampling parameters, system prompt, batch size, and thread count.
