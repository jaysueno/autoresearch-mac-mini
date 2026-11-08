"""run.py: the keep-or-revert bookkeeping, on a throwaway results.tsv in run.py's own format."""
import run


def test_best_score_reads_only_kept_rows(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rows = [
        run.TSV_HEADER,
        "2030-01-01 00:00:00\taaaaaaa\t50.00\t9.6\t70\t62\t24.4\t300\t900\tkeep\tbaseline",
        "2030-01-01 00:10:00\tbbbbbbb\t80.00\t9.6\t99\t62\t24.4\t300\t900\tdiscard\tlooked good, lost",
        "2030-01-01 00:20:00\tccccccc\t61.25\t9.6\t80\t62\t24.4\t300\t900\tkeep\tone knob",
        "2030-01-01 00:30:00\tddddddd\t0\t0\t0\t0\t0\t0\t0\tcrash\tbroke",
    ]
    (tmp_path / "results.tsv").write_text("\n".join(rows) + "\n")
    assert run.get_best_score() == 61.25


def test_best_score_is_zero_with_no_log(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert run.get_best_score() == 0.0


def test_log_result_writes_the_header_once(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run.log_result("aaaaaaa", "70.00\t9.6\t90\t62\t24.4\t300\t900", "keep", "first")
    run.log_result("bbbbbbb", "60.00\t9.6\t80\t62\t24.4\t300\t900", "discard", "second")
    lines = (tmp_path / "results.tsv").read_text().splitlines()
    assert lines[0] == run.TSV_HEADER
    assert len(lines) == 3
    assert lines[1].split("\t")[9] == "keep"
    assert run.get_best_score() == 70.0
