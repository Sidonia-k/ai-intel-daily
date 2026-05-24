from datetime import date
from pathlib import Path

import ai_intel_daily
import ai_intel_daily.main as main_module
from ai_intel_daily.main import (
    generate_ai_daily_report,
    generate_reports,
    generate_stock_research_report,
)


TEST_OUTPUT_DIR = Path("data/test-output")


def _test_output_dir(name: str) -> Path:
    path = TEST_OUTPUT_DIR / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_package_imports():
    assert ai_intel_daily.__version__ == "0.0.0"


def test_generate_ai_daily_report_writes_markdown_without_network(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "collect_from_config",
        lambda config_path: [
            {
                "title": "OpenAI ships a model update",
                "url": "https://example.com/openai-model",
                "source": "OpenAI News",
                "published_at": "2026-05-22T08:00:00+00:00",
                "summary": "A model update for developers.",
                "category": "model",
            }
        ],
    )

    output_dir = _test_output_dir("ai-report")
    ai_path = generate_ai_daily_report(output_dir=output_dir, report_date=date(2026, 5, 22))

    assert ai_path == output_dir / "ai" / "2026-05-22-ai-daily-report.md"
    report = ai_path.read_text(encoding="utf-8")
    assert "# AI 圈日报" in report
    assert "日期：2026-05-22" in report
    assert "## 来源列表" in report
    assert "OpenAI ships a model update" in report


def test_generate_ai_daily_report_handles_empty_items(monkeypatch):
    monkeypatch.setattr(main_module, "collect_from_config", lambda config_path: [])

    ai_path = generate_ai_daily_report(
        output_dir=_test_output_dir("empty-ai-report"),
        report_date=date(2026, 5, 22),
    )

    report = ai_path.read_text(encoding="utf-8")
    assert "暂无有效数据" in report
    assert "## 来源列表" in report


def test_generate_reports_keeps_default_two_report_contract(monkeypatch):
    monkeypatch.setattr(main_module, "collect_from_config", lambda config_path: [])

    output_dir = _test_output_dir("all-reports")
    ai_path, stock_path = generate_reports(output_dir=output_dir, report_date=date(2026, 5, 22))

    assert ai_path == output_dir / "ai" / "2026-05-22-ai-daily-report.md"
    assert stock_path == output_dir / "stocks" / "2026-05-22-ai-stock-report.md"
    assert ai_path.exists()
    assert stock_path.exists()


def test_main_uses_default_all_report_logic_when_report_is_not_provided(monkeypatch):
    calls = []

    def fake_generate_reports(output_dir=None, report_date=None):
        calls.append((output_dir, report_date))
        return Path("ai-report.md"), Path("stock-report.md")

    monkeypatch.setattr(main_module, "generate_reports", fake_generate_reports)

    main_module.main([])

    assert calls == [(None, None)]


def test_main_passes_cli_date_to_default_generate_reports(monkeypatch):
    calls = []

    def fake_generate_reports(output_dir=None, report_date=None):
        calls.append((output_dir, report_date))
        return Path("ai-report.md"), Path("stock-report.md")

    monkeypatch.setattr(main_module, "generate_reports", fake_generate_reports)

    main_module.main(["--date", "2026-05-22"])

    assert calls == [(None, date(2026, 5, 22))]


def test_main_report_ai_generates_only_ai_report(monkeypatch):
    ai_calls = []
    stock_calls = []

    def fake_generate_ai_daily_report(output_dir=None, report_date=None, sources_config_path=None):
        ai_calls.append((output_dir, report_date, sources_config_path))
        return Path("ai-report.md")

    def fake_generate_stock_research_report(output_dir=None, report_date=None):
        stock_calls.append((output_dir, report_date))
        return Path("stock-report.md")

    monkeypatch.setattr(main_module, "generate_ai_daily_report", fake_generate_ai_daily_report)
    monkeypatch.setattr(main_module, "generate_stock_research_report", fake_generate_stock_research_report)

    main_module.main(["--report", "ai", "--date", "2026-05-22"])

    assert ai_calls == [(None, date(2026, 5, 22), None)]
    assert stock_calls == []


def test_ai_report_contains_required_sections(monkeypatch):
    monkeypatch.setattr(main_module, "collect_from_config", lambda config_path: [])

    ai_path = generate_ai_daily_report(
        output_dir=_test_output_dir("ai-sections"),
        report_date=date(2026, 5, 22),
    )
    ai_report = ai_path.read_text(encoding="utf-8")

    required_sections = [
        "今日最值得关注的 3～5 件事",
        "大模型发布与更新",
        "AI 产品更新",
        "Agent / MCP / Workflow / Skills 生态",
        "开源项目与开发者工具",
        "重要论文 / 技术趋势",
        "对我学习 Codex、agent、AI 应用的启发",
        "来源列表",
    ]
    for section in required_sections:
        assert section in ai_report


def test_stock_report_contains_required_sections_and_disclaimer():
    stock_path = generate_stock_research_report(
        output_dir=_test_output_dir("stock-sections"),
        report_date=date(2026, 5, 22),
    )
    stock_report = stock_path.read_text(encoding="utf-8")

    required_sections = [
        "安全声明",
        "事实区",
        "合理推断区",
        "不确定性区",
        "风险点",
        "后续关注指标",
    ]
    for section in required_sections:
        assert section in stock_report
    assert "不构成投资建议" in stock_report
    assert "不提供买入、卖出或持有建议" in stock_report


def test_stock_report_avoids_deterministic_investment_advice():
    stock_path = generate_stock_research_report(
        output_dir=_test_output_dir("stock-safety"),
        report_date=date(2026, 5, 22),
    )
    stock_report = stock_path.read_text(encoding="utf-8")

    banned_phrases = [
        "建议买入",
        "可以买入",
        "强烈买入",
        "应该买入",
        "建议卖出",
        "应该卖出",
        "建议持有",
        "可以重仓",
        "保证盈利",
        "保证赚钱",
        "稳赚不赔",
        "一定上涨",
        "必然上涨",
    ]
    for phrase in banned_phrases:
        assert phrase not in stock_report
