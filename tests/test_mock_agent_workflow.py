from datetime import date
from pathlib import Path
import socket

from ai_intel_daily.agents import mock_workflow
from ai_intel_daily.agents.mock_workflow import CHINESE_FINANCIAL_DISCLAIMER
from ai_intel_daily.agents.agent_specs import (
    CYBER_COMMITTEE_AGENT,
    EDITOR_AGENT,
    FACT_CHECK_AGENT,
    FINANCIAL_SAFETY_AGENT,
    MARKET_AGENT,
    NEWS_AGENT,
)
from ai_intel_daily.agents.guardrails import (
    PROHIBITED_INVESTMENT_ADVICE_PHRASES,
)
from ai_intel_daily.main import generate_mock_agent_daily_report
from ai_intel_daily.reports.agent_daily_report import (
    render_agent_daily_report,
    write_agent_daily_report,
)


EXPECTED_AGENT_NAMES = [
    NEWS_AGENT,
    MARKET_AGENT,
    CYBER_COMMITTEE_AGENT,
    FACT_CHECK_AGENT,
    FINANCIAL_SAFETY_AGENT,
    EDITOR_AGENT,
]
EXPECTED_CYBER_ROLES = [
    "Cyber Buffett",
    "Cyber Munger",
    "Cyber Graham",
    "Cyber Damodaran",
    "Cyber Wood",
    "Cyber Lynch",
    "Cyber Taleb",
    "Cyber Huang",
]
TEST_OUTPUT_DIR = Path("data/test-output/stage7b-agent-report")


def test_run_mock_daily_agent_workflow_returns_structured_result():
    result = mock_workflow.run_mock_daily_agent_workflow(date(2026, 6, 8))

    assert result["report_date"] == "2026-06-08"
    assert result["mock"] is True
    assert result["steps"]
    assert result["markdown"]

    for step in result["steps"]:
        assert set(step) == {"agent_name", "input_summary", "output", "warnings"}
        assert step["agent_name"]
        assert step["input_summary"]
        assert isinstance(step["output"], dict)
        assert isinstance(step["warnings"], list)


def test_mock_workflow_contains_six_expected_agent_steps():
    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    agent_names = [step["agent_name"] for step in result["steps"]]

    assert len(result["steps"]) == 6
    assert agent_names == EXPECTED_AGENT_NAMES


def test_financial_safety_agent_runs_guardrails(monkeypatch):
    calls = []
    original_check = mock_workflow.guardrails.check_financial_safety_text

    def tracking_check(text):
        calls.append(text)
        return original_check(text)

    monkeypatch.setattr(
        mock_workflow.guardrails,
        "check_financial_safety_text",
        tracking_check,
    )

    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    safety_step = _step(result, FINANCIAL_SAFETY_AGENT)

    assert calls
    assert safety_step["output"]["passed"] is True
    assert safety_step["output"]["missing_disclaimer"] is False
    assert safety_step["output"]["blocked_phrases"] == []


def test_rendered_markdown_contains_disclaimer():
    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    markdown = render_agent_daily_report(result)

    assert CHINESE_FINANCIAL_DISCLAIMER in markdown
    assert "## 免责声明" in markdown
    assert "阶段 7B 本地 mock 模拟运行" in markdown


def test_rendered_markdown_uses_chinese_report_content():
    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    markdown = render_agent_daily_report(result)

    assert "# 阶段 7B 本地 Mock Agent 日报" in markdown
    assert "## 本地 Mock 说明" in markdown
    assert "## Editor Agent 汇总" in markdown
    assert "模拟模型发布说明强调更低推理资源占用" in markdown
    assert "Stage 7B Mock Agent Daily Report" not in markdown
    assert "Local Mock Notice" not in markdown
    assert "Disclaimer" not in markdown


def test_rendered_markdown_contains_all_cyber_committee_roles():
    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    markdown = render_agent_daily_report(result)

    for role in EXPECTED_CYBER_ROLES:
        assert role in markdown


def test_rendered_markdown_uses_readable_status_labels_and_clean_joining():
    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    markdown = render_agent_daily_report(result)

    assert "）-" not in markdown
    assert "。 （来源" not in markdown
    assert "）。摘要：" in markdown
    assert "来源字段：已包含" in markdown
    assert "事实、推断和不确定性标签：已区分" in markdown
    assert "检查结果：通过" in markdown
    assert "免责声明状态：已包含" in markdown
    assert "禁止性投资建议表达：未发现" in markdown
    assert "：True" not in markdown
    assert "：False" not in markdown


def test_rendered_markdown_avoids_deterministic_investment_advice():
    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    markdown = render_agent_daily_report(result).lower()

    for phrase in PROHIBITED_INVESTMENT_ADVICE_PHRASES:
        assert phrase.lower() not in markdown


def test_mock_workflow_does_not_access_network(monkeypatch):
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed in Stage 7B mock workflow")

    monkeypatch.setattr(socket, "socket", fail_socket)

    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")

    assert result["mock"] is True
    assert len(result["steps"]) == 6


def test_write_agent_daily_report_uses_expected_path():
    result = mock_workflow.run_mock_daily_agent_workflow("2026-06-08")
    output_dir = TEST_OUTPUT_DIR / "direct-write"

    report_path = write_agent_daily_report(result, output_dir=output_dir)

    assert report_path == output_dir / "agent" / "2026-06-08-agent-daily-report.md"
    assert report_path.exists()
    assert CHINESE_FINANCIAL_DISCLAIMER in report_path.read_text(encoding="utf-8")


def test_generate_mock_agent_daily_report_uses_expected_path():
    output_dir = TEST_OUTPUT_DIR / "main-entrypoint"

    report_path = generate_mock_agent_daily_report(
        output_dir=output_dir,
        report_date=date(2026, 6, 8),
    )

    assert report_path == output_dir / "agent" / "2026-06-08-agent-daily-report.md"
    assert report_path.exists()


def _step(result, agent_name):
    return next(step for step in result["steps"] if step["agent_name"] == agent_name)
