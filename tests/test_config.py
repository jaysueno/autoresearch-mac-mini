"""config.py: the only file the experiment agent edits. These tests pin the rules in program.md."""
import config


def test_modelfile_has_every_knob():
    text = config.generate_modelfile()
    assert text.startswith(f"FROM {config.MODEL_BASE}\n")
    for name, value in [
        ("num_ctx", config.NUM_CTX),
        ("num_batch", config.NUM_BATCH),
        ("num_thread", config.NUM_THREAD),
        ("num_predict", config.NUM_PREDICT),
        ("temperature", config.TEMPERATURE),
        ("repeat_penalty", config.REPEAT_PENALTY),
        ("top_p", config.TOP_P),
        ("top_k", config.TOP_K),
        ("min_p", config.MIN_P),
        ("mirostat", config.MIROSTAT),
    ]:
        assert f"PARAMETER {name} {value}\n" in text
    assert text.endswith(f"SYSTEM {config.SYSTEM_PROMPT}\n")


def test_program_md_constraints_hold():
    # program.md: NUM_CTX stays at 32768, thinking stays on for code and reasoning.
    assert config.NUM_CTX == 32768
    assert config.THINK_MODE["code"] is True
    assert config.THINK_MODE["reasoning"] is True
    assert set(config.THINK_MODE) == {"short", "code", "reasoning", "creative"}


def test_model_base_names_a_qwen_3_5_27b():
    assert "Qwen3.5-27B" in config.MODEL_BASE
