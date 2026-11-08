"""
Autoresearch Config -- THE AGENT EDITS THIS FILE
=================================================
This is the only file the agent modifies.
Each change = one experiment = one git commit.
"""

# Base model -- Opus-distilled Qwen 3.5 27B
MODEL_BASE = 'kwangsuklee/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF'

# === INFERENCE PARAMETERS ===
NUM_CTX = 32768
NUM_BATCH = 512
NUM_THREAD = 10
NUM_PREDICT = 2048

# === SAMPLING PARAMETERS ===
TEMPERATURE = 1.1
REPEAT_PENALTY = 1.1
TOP_P = 0.98
TOP_K = 40
MIN_P = 0.0
MIROSTAT = 0
MIROSTAT_ETA = 0.1
MIROSTAT_TAU = 5.0

# === THINKING MODE ===
THINK_MODE = {
    'short': False,
    'code': True,
    'reasoning': True,
    'creative': False,
}

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = 'You are a helpful assistant.'

# === MODELFILE TEMPLATE (generated from above) ===
def generate_modelfile():
    lines = [
        f"FROM {MODEL_BASE}",
        f"PARAMETER num_ctx {NUM_CTX}",
        f"PARAMETER num_batch {NUM_BATCH}",
        f"PARAMETER num_thread {NUM_THREAD}",
        f"PARAMETER num_predict {NUM_PREDICT}",
        f"PARAMETER temperature {TEMPERATURE}",
        f"PARAMETER repeat_penalty {REPEAT_PENALTY}",
        f"PARAMETER top_p {TOP_P}",
        f"PARAMETER top_k {TOP_K}",
        f"PARAMETER min_p {MIN_P}",
        f"PARAMETER mirostat {MIROSTAT}",
        f"PARAMETER mirostat_eta {MIROSTAT_ETA}",
        f"PARAMETER mirostat_tau {MIROSTAT_TAU}",
        f"SYSTEM {SYSTEM_PROMPT}",
    ]
    return "\n".join(lines) + "\n"
