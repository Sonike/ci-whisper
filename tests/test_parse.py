"""Tests for ci_whisper.parse."""

from pathlib import Path

from ci_whisper.parse import clean_lines, diagnose, suggest_fix

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_pytest_failure_finds_assertion_not_exit_code():
    diagnosis = diagnose(load("pytest_fail.log"))
    assert diagnosis.root_cause is not None
    assert diagnosis.root_cause.kind == "test-failure"
    assert "test_render_header" in diagnosis.root_cause.text
    assert "test_render_header" in diagnosis.fix


def test_npm_failure_reports_eresolve_and_ignores_deprecation():
    diagnosis = diagnose(load("npm_fail.log"))
    assert diagnosis.root_cause is not None
    assert diagnosis.root_cause.kind == "npm-error"
    assert "ERESOLVE" in diagnosis.root_cause.text
    assert "Peer dependency" in diagnosis.fix


def test_traceback_uses_module_not_found_rule():
    diagnosis = diagnose(load("traceback.log"))
    assert diagnosis.root_cause is not None
    assert "No module named 'yaml'" in diagnosis.root_cause.text
    assert "pip install yaml" in diagnosis.fix


def test_noise_only_log_reports_no_error():
    diagnosis = diagnose(load("noise_only.log"))
    assert diagnosis.root_cause is None
    assert "No error signal found" in diagnosis.fix


def test_line_numbers_point_at_the_source_line():
    raw = load("pytest_fail.log")
    diagnosis = diagnose(raw)
    lines = clean_lines(raw)
    root = diagnosis.root_cause
    assert root is not None
    assert lines[root.line_no - 1].strip() == root.text


def test_chain_is_ordered_and_unique():
    diagnosis = diagnose(load("pytest_fail.log"))
    numbers = [hit.line_no for hit in diagnosis.chain]
    assert numbers == sorted(numbers)
    assert len(numbers) == len(set(numbers))
    assert diagnosis.chain[0].line_no == diagnosis.root_cause.line_no


def test_suggest_fix_handles_none():
    assert suggest_fix(None).startswith("No error signal found")


def test_exit_code_only_log_falls_back_to_exit_signal():
    diagnosis = diagnose("##[error]Process completed with exit code 1.")
    assert diagnosis.root_cause is not None
    assert diagnosis.root_cause.kind == "github-error"
