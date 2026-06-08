import re
import socket
from pathlib import Path

from ai_intel_daily.agent_runtime.deepseek_runtime import run_deepseek_agent_runtime
from ai_intel_daily.agent_runtime.mock_runtime import run_mock_agent_runtime
from ai_intel_daily.agent_runtime.runtime_types import AgentRuntimeResult
from ai_intel_daily.agents.guardrails import (
    REQUIRED_FINANCIAL_DISCLAIMER,
    check_financial_safety_text,
)


ROOT = Path(__file__).resolve().parents[1]


def test_mock_runtime_runs_offline(monkeypatch):
    def fail_socket(*args, **kwargs):
        raise AssertionError("mock agent runtime must not access the network")

    monkeypatch.setattr(socket, "socket", fail_socket)

    result = run_mock_agent_runtime("2026-06-08")

    assert isinstance(result, AgentRuntimeResult)
    assert result.provider == "mock"
    assert result.used_real_api is False
    assert result.final_markdown
    assert result.safety_passed is True


def test_mock_runtime_markdown_contains_disclaimer():
    result = run_mock_agent_runtime("2026-06-08")

    assert "不构成投资建议" in result.final_markdown
    assert "不提供买入、卖出或持有建议" in result.final_markdown


def test_deepseek_runtime_missing_key_returns_clear_result_without_network(monkeypatch):
    def fail_socket(*args, **kwargs):
        raise AssertionError("missing-key DeepSeek runtime must not access the network")

    monkeypatch.setattr(socket, "socket", fail_socket)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    result = run_deepseek_agent_runtime("2026-06-08")

    assert result.provider == "deepseek"
    assert result.model == "deepseek-v4-flash"
    assert result.workflow_name == "stage7d-deepseek-agent-runtime-smoke"
    assert result.final_markdown == ""
    assert result.safety_passed is False
    assert result.used_real_api is False
    assert result.warnings
    assert "DEEPSEEK_API_KEY is not set" in result.warnings[0]
    assert "Bearer" not in result.warnings[0]


def test_pytest_path_does_not_require_deepseek_api_key(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    result = run_mock_agent_runtime("2026-06-08")

    assert result.used_real_api is False
    assert result.final_markdown


def test_financial_safety_blocks_stage7d_required_phrases():
    for phrase in ("建议买入", "必涨", "稳赚", "满仓"):
        text = f"{phrase}\n\n{REQUIRED_FINANCIAL_DISCLAIMER}"
        safety_check = check_financial_safety_text(text)

        assert safety_check.passed is False
        assert phrase in safety_check.blocked_phrases


def test_new_stage7d_files_do_not_contain_hardcoded_api_keys():
    paths = [
        ROOT / "src" / "ai_intel_daily" / "agent_runtime" / "__init__.py",
        ROOT / "src" / "ai_intel_daily" / "agent_runtime" / "runtime_types.py",
        ROOT / "src" / "ai_intel_daily" / "agent_runtime" / "mock_runtime.py",
        ROOT / "src" / "ai_intel_daily" / "agent_runtime" / "deepseek_runtime.py",
        ROOT / "scripts" / "deepseek_agent_runtime_smoke.py",
        ROOT / "docs" / "deepseek_agent_runtime.md",
        ROOT / "README.md",
    ]
    secret_patterns = (
        re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
        re.compile(r"Bearer\s+[A-Za-z0-9._-]{8,}", re.IGNORECASE),
        re.compile(r"\bapi_key\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    )

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            for pattern in secret_patterns:
                assert not pattern.search(stripped)
