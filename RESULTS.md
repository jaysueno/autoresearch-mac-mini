# Autoresearch Results (Full History)

**119 experiments** across 2 models and 3 eval versions

| # | time | score | qual | tps | model | eval | temp | top_p | top_k | min_p | miro | batch | experiment |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 22:10:15 | 49.69 | 74 | 9.7 | qwen3.5-27b | v2 | 0.7 | 0.9 | 40 | 0.0 |  | 512 | feat: streaming eval v2 -- live thinking display, 8 prompts, |
| 2 | 23:46:17 | 52.59 | 64 | 9.7 | qwen3.5-27b | v3 | 0.5 | 0.9 | 40 | 0.0 |  | 512 | feat: eval v3 -- quality-heavy scoring, harder prompts, thin |
| 3 | 02:01:29 | 58.85 | 73 | 9.5 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: REPEAT_PENALTY 1.1 -> 1.0 (retry, previous run crashed) |
| 4 | 02:19:57 | 41.52 | 47 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.1 |  | 512 | exp: MIN_P 0.0 -> 0.1 (aggressive low-prob filtering with TE |
| 5 | 02:29:08 | 41.51 | 47 | 9.5 | qwen3.5-27b | v3 | 0.3 | 0.95 | 40 | 0.0 |  | 512 | exp: TOP_P 0.9 -> 0.95 (wider nucleus may help exit thinking |
| 6 | 02:37:43 | 58.56 | 73 | 9.5 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: NUM_THREAD 10 -> 12 (use 2 efficiency cores for CPU-sid |
| 7 | 02:46:44 | 41.52 | 47 | 9.5 | qwen3.5-27b | v3 | 0.25 | 0.9 | 40 | 0.0 |  | 512 | exp: TEMPERATURE 0.3 -> 0.25 (fine-tune between 0.2 and 0.3) |
| 8 | 02:55:20 | 23.02 | 18 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: system prompt -> "Think briefly, then answer" |
| 9 | 03:01:27 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: minimal system prompt "You are a helpful assistant." |
| 10 | 03:10:04 | 23.01 | 18 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: add "Be concise." to minimal system prompt |
| 11 | 03:16:47 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.85 | 40 | 0.0 |  | 512 | exp: TOP_P 0.9 -> 0.85 (tighter nucleus with minimal system  |
| 12 | 03:24:02 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 1024 | exp: NUM_BATCH 512 -> 1024 (faster prompt eval, M4 Pro shoul |
| 13 | 03:30:22 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.25 | 0.9 | 40 | 0.0 |  | 512 | exp: TEMPERATURE 0.3 -> 0.25 (re-test with minimal system pr |
| 14 | 03:36:45 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: NUM_PREDICT 2048 -> 1024 (trim verbose responses, save  |
| 15 | 03:42:47 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: REPEAT_PENALTY 1.1 -> 1.05 (lighter penalty with minima |
| 16 | 03:49:33 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.15 | 0.9 | 40 | 0.0 |  | 512 | exp: TEMPERATURE 0.3 -> 0.15 (very deterministic with minima |
| 17 | 03:56:37 | 76.19 | 100 | 9.5 | qwen3.5-27b | v3 | 0.5 | 0.9 | 40 | 0.0 |  | 512 | exp: TEMPERATURE 0.3 -> 0.5 (re-test with minimal system pro |
| 18 | 04:05:21 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.7 | 0.9 | 40 | 0.0 |  | 512 | exp: TEMPERATURE 0.3 -> 0.7 (test higher creativity with min |
| 19 | 04:11:11 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 60 | 0.0 |  | 512 | exp: TOP_K 40 -> 60 (wider token pool with minimal prompt) |
| 20 | 04:17:23 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: empty system prompt (remove all system instructions) |
| 21 | 04:23:41 | 41.37 | 46 | 9.5 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: NUM_PREDICT 2048 -> 512 (force shorter responses, fit m |
| 22 | 04:29:33 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | exp: NUM_THREAD 10 -> 12 (re-test with minimal system prompt |
| 23 | 04:36:28 | 9.77 | 0 | 0.0 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 256 | exp: NUM_BATCH 512 -> 256 (smaller batch, test prompt eval i |
| 24 | 04:43:21 | 9.77 | 0 | 0.0 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 |  | 512 | exp: TEMPERATURE 0.3 -> 1.0 (extreme high, test quality impa |
| 25 | 09:42:56 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 0.3 | 0.9 | 40 | 0.0 |  | 512 | revert: TEMPERATURE back to 0.3 (1.0 crashed with 404) |
| 26 | 09:48:42 | 76.20 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 |  | 512 | exp: TEMPERATURE 0.3 -> 1.0 (retry after Ollama fix) |
| 27 | 09:54:52 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 |  | 256 | exp: NUM_BATCH 512 -> 256 (retry after Ollama fix, with TEMP |
| 28 | 10:01:12 | 70.36 | 91 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.8 | 40 | 0.0 |  | 512 | exp: TOP_P 0.9 -> 0.8 (tighter nucleus with TEMP=1.0) |
| 29 | 10:49:03 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIROSTAT_ETA 0.1     # Mirostat learning rate (only whe |
| 30 | 10:54:31 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.08 (explore search space) |
| 31 | 10:59:55 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.8 (explore search space) |
| 32 | 11:05:47 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 1.1 (explore search space) |
| 33 | 11:11:19 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.02 (explore search space) |
| 34 | 11:17:51 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIROSTAT_TAU 5.0     # Mirostat target entropy (only wh |
| 35 | 11:23:29 | 64.41 | 82 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 1.2 (explore search space) |
| 36 | 11:29:40 | 70.37 | 91 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.1 -> 1.12 (explore search space) |
| 37 | 11:36:12 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIROSTAT 0           # 0=disabled, 1=mirostat v1, 2=mir |
| 38 | 11:46:50 | 76.18 | 100 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.9 (interaction search around curre |
| 39 | 11:52:16 | 76.20 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10        # CPU threads (M4 Pro: 10 perf + 4 |
| 40 | 11:58:00 | 74.03 | 97 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.15 -> 1.08 (exploit search around curr |
| 41 | 12:03:33 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIROSTAT_TAU 5.0     # Mirostat target entropy (only wh |
| 42 | 12:09:45 | 70.37 | 91 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: THINK_MODE["creative"] False -> True (exploit search ar |
| 43 | 12:14:54 | 73.26 | 95 | 9.7 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.15 -> 1.08 (interaction search around  |
| 44 | 12:20:42 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.15 -> 1.1 (exploit search around curre |
| 45 | 12:26:51 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 30 (exploit search around current best) |
| 46 | 12:32:31 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.01 (exploit search around current best) |
| 47 | 12:40:00 | 58.86 | 73 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.15 -> 1.18 (exploit search around curr |
| 48 | 12:45:18 | 46.67 | 55 | 9.7 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 1.1 (interaction search around curre |
| 49 | 12:52:12 | 71.56 | 93 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.15 -> 1.08 (interaction search around  |
| 50 | 12:57:58 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: NUM_BATCH 512        # Batch size for prompt processing |
| 51 | 13:03:27 | 46.67 | 55 | 9.7 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10        # CPU threads (M4 Pro: 10 perf + 4 |
| 52 | 13:09:19 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 1.05 (exploit search around current  |
| 53 | 13:16:58 | 58.86 | 73 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.95 (explore search around current  |
| 54 | 13:22:08 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: NUM_BATCH 512        # Batch size for prompt processing |
| 55 | 13:28:17 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.85 (exploit search around current  |
| 56 | 13:34:49 | 55.61 | 68 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 1.15 (exploit search around current  |
| 57 | 13:40:14 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.03 (exploit search around current best) |
| 58 | 13:45:41 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.9 -> 0.88 (interaction search around current be |
| 59 | 13:51:33 | 72.42 | 94 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.95 (exploit search around current  |
| 60 | 13:57:17 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 50 (exploit search around current best) |
| 61 | 14:02:57 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.9 (exploit search around current b |
| 62 | 14:14:00 | 76.19 | 100 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 50 (exploit from clean 76.20 baseline) |
| 63 | 14:19:59 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.9 -> 0.92 (exploit from clean 76.20 baseline) |
| 64 | 14:25:47 | 38.28 | 42 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: NUM_PREDICT 2048 -> 1024 (exploit from clean 76.20 base |
| 65 | 14:31:06 | 46.67 | 55 | 9.7 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 50 (exploit from clean 76.20 baseline) |
| 66 | 14:36:30 | 72.42 | 94 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.9 -> 0.95 (exploit from clean 76.20 baseline) |
| 67 | 14:42:36 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.02 (exploit from clean 76.20 baseline) |
| 68 | 14:47:51 | 76.20 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.9 (exploit from clean 76.20 baseli |
| 69 | 14:54:03 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10 -> 11 (exploit from clean 76.20 baseline) |
| 70 | 14:59:22 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 30 (interaction from clean 76.20 baseline) |
| 71 | 15:05:18 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 30 (interaction from clean 76.20 baseline) |
| 72 | 15:12:56 | 72.42 | 94 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 50 (exploit from clean 76.20 baseline) |
| 73 | 15:19:53 | 46.59 | 55 | 9.3 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: THINK_MODE["short"] False -> True (explore from clean 7 |
| 74 | 15:26:04 | 74.03 | 97 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.95 (interaction from clean 76.20 b |
| 75 | 15:32:15 | 70.37 | 91 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: NUM_BATCH 512 -> 256 (exploit from clean 76.20 baseline |
| 76 | 15:37:41 | 72.42 | 94 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 1.05 (exploit from clean 76.20 basel |
| 77 | 15:43:33 | 76.14 | 100 | 9.3 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: THINK_MODE["short"] False -> True (exploit from clean 7 |
| 78 | 15:49:55 | 70.37 | 91 | 9.5 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.1 -> 1.15 (exploit from clean 76.20 ba |
| 79 | 15:55:31 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 30 (exploit from clean 76.20 baseline) |
| 80 | 16:00:40 | 46.67 | 55 | 9.7 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 20 (exploit from clean 76.20 baseline) |
| 81 | 16:06:26 | 46.67 | 55 | 9.7 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.1 -> 1.08 (interaction from clean 76.2 |
| 82 | 16:11:50 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 0.95 (interaction from clean 76.20 b |
| 83 | 16:17:04 | 76.19 | 100 | 9.6 | qwen3.5-27b | v3 | 1.0 | 0.9 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.0 -> 1.05 (exploit from clean 76.20 basel |
| 84 | 13:08:34 | 15.21 | 8 | 1.0 | opus-distilled | v4 | 0.7 | 0.9 | 40 | 0.0 | 0 | 512 | feat: eval v4 (shuffled prompts) + Opus-distilled model |
| 85 | 13:16:23 | 53.95 | 65 | 9.1 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.9 -> 0.98 (explore distilled-model search space |
| 86 | 13:21:44 | 19.73 | 15 | 1.7 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 0.7 -> 0.0 (explore distilled-model search  |
| 87 | 13:27:25 | 17.33 | 11 | 1.5 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10 -> 5 (explore distilled-model search spac |
| 88 | 13:35:46 | 22.44 | 19 | 2.1 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 0.7 -> 1.2 (explore distilled-model search  |
| 89 | 13:41:14 | 20.68 | 16 | 2.0 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10 -> 1 (explore distilled-model search spac |
| 90 | 13:48:58 | 15.68 | 9 | 1.1 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: MIROSTAT_TAU 5.0 -> 10.0 (explore distilled-model searc |
| 91 | 13:54:51 | 17.80 | 12 | 1.7 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: THINK_MODE["short"] False -> True (prompt-type thinking |
| 92 | 14:00:20 | 28.10 | 27 | 3.5 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.98 -> 1.0 (explore distilled-model search space |
| 93 | 14:08:27 | 29.27 | 28 | 4.6 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10 -> 2 (explore distilled-model search spac |
| 94 | 14:15:05 | 22.86 | 19 | 2.5 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.1 -> 0.5 (explore distilled-model sear |
| 95 | 14:23:57 | 20.69 | 16 | 2.1 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 0.7 -> 0.5 (explore distilled-model search  |
| 96 | 14:30:31 | 25.12 | 22 | 3.0 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: MIROSTAT_TAU 5.0 -> 0.5 (explore distilled-model search |
| 97 | 14:36:04 | 19.64 | 14 | 1.8 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.1 -> 0.5 (explore distilled-model sear |
| 98 | 14:39:03 | 19.07 | 14 | 1.8 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.1 (explore distilled-model search space) |
| 99 | 14:45:07 | 20.05 | 15 | 1.8 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.1 (explore distilled-model search space) |
| 100 | 14:52:54 | 23.49 | 20 | 3.0 | opus-distilled | v4 | 0.7 | 0.98 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.08 (explore distilled-model search space |
| 101 | 14:59:16 | 63.70 | 80 | 9.1 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 0.7 -> 1.2 (explore distilled-model search  |
| 102 | 15:07:06 | 25.11 | 22 | 3.0 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: REPEAT_PENALTY 1.1 -> 0.95 (explore distilled-model sea |
| 103 | 15:12:25 | 24.57 | 22 | 3.0 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10 -> 13 (explore distilled-model search spa |
| 104 | 15:19:27 | 56.12 | 68 | 9.1 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 60 (explore distilled-model search space) |
| 105 | 15:25:07 | 18.55 | 13 | 1.7 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.2 -> 1.4 (explore distilled-model search  |
| 106 | 15:31:58 | 20.07 | 15 | 2.0 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 80 (explore distilled-model search space) |
| 107 | 15:37:43 | 24.58 | 22 | 3.0 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: NUM_THREAD 10 -> 8 (explore distilled-model search spac |
| 108 | 15:43:43 | 19.13 | 14 | 1.8 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.2 -> 1.6 (explore distilled-model search  |
| 109 | 15:50:58 | 55.03 | 67 | 9.0 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.98 -> 0.85 (explore distilled-model search spac |
| 110 | 15:56:09 | 19.81 | 15 | 1.8 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TEMPERATURE 1.2 -> 1.4 (explore distilled-model search  |
| 111 | 16:01:07 | 18.56 | 13 | 1.8 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.98 -> 0.3 (explore distilled-model search space |
| 112 | 16:08:57 | 18.40 | 13 | 1.8 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_P 0.98 -> 0.88 (explore distilled-model search spac |
| 113 | 16:17:22 | 16.50 | 10 | 1.4 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: MIN_P 0.0 -> 0.05 (explore distilled-model search space |
| 114 | 16:23:41 | 20.65 | 16 | 1.8 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: TOP_K 40 -> 60 (explore distilled-model search space) |
| 115 | 16:29:15 | 27.87 | 27 | 3.0 | opus-distilled | v4 | 1.2 | 0.98 | 40 | 0.0 | 0 | 512 | exp: MIROSTAT 0 -> 2 (distilled model may benefit from miros |
| 116 | 13:21:47 | 40.41 | 44 | 8.9 | opus-distilled | v4 | 0.7 | 0.9 | 40 | 0.0 | 0 | 128 | exp: NUM_BATCH 512 -> 128 (hypothesis) |
| 117 | 13:30:45 | 39.32 | 42 | 8.9 | opus-distilled | v4 | 0.7 | 0.9 | 40 | 0.0 | 0 | 128 | exp: NUM_BATCH 512 -> 128 (hypothesis) |
| 118 | 13:45:39 | 26.00 | 22 | 8.9 | opus-distilled | v4 | 0.7 | 0.8 | 40 | 0.0 | 0 | 128 | exp: TOP_P 0.9 -> 0.8 (hypothesis) |
| 119 | 13:56:52 | 37.70 | 40 | 8.9 | opus-distilled | v4 | 0.7 | 0.8 | 40 | 0.0 | 0 | 128 | exp: MIROSTAT_TAU 7.0 -> 2.0 (hypothesis) |
