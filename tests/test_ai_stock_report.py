from datetime import date
from pathlib import Path

from ai_intel_daily.collectors.market_collector import (
    RISK_CATEGORIES,
    SECTOR_NAMES,
    collect_market_research_snapshot,
)
from ai_intel_daily.main import generate_stock_research_report
from ai_intel_daily.reports.ai_stock_report import (
    FINANCIAL_DISCLAIMER,
    SIMULATED_DATA_NOTICE,
    render_ai_stock_report,
)


TEST_OUTPUT_DIR = Path("data/test-output")


def _test_output_dir(name: str) -> Path:
    path = TEST_OUTPUT_DIR / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_ai_stock_report_file_can_be_generated():
    output_dir = _test_output_dir("stage5-stock-report")

    stock_path = generate_stock_research_report(output_dir=output_dir, report_date=date(2026, 5, 22))

    assert stock_path == output_dir / "stocks" / "2026-05-22-ai-stock-report.md"
    assert stock_path.exists()


def test_ai_stock_report_contains_disclaimer_and_simulated_data_notice():
    report = _render_sample_report()

    assert FINANCIAL_DISCLAIMER in report
    assert SIMULATED_DATA_NOTICE in report
    assert "不构成投资建议" in report
    assert "不提供买入、卖出或持有建议" in report


def test_ai_stock_report_separates_facts_inferences_and_uncertainties():
    report = _render_sample_report()

    assert "## 事实区" in report
    assert "## 合理推断区" in report
    assert "## 不确定性区" in report
    assert "只放模拟数据中的可验证事实，不做主观判断。" in report
    assert "当前信息不足以形成结论" in report


def test_ai_stock_report_contains_stable_sector_and_risk_categories():
    report = _render_sample_report()

    for sector_name in SECTOR_NAMES:
        assert f"### {sector_name}" in report

    for risk_category in RISK_CATEGORIES:
        assert risk_category in report


def test_ai_stock_report_avoids_dangerous_investment_advice_phrases():
    report = _render_sample_report()

    banned_phrases = [
        "建议买入",
        "建议卖出",
        "强烈买入",
        "强烈卖出",
        "必涨",
        "肯定上涨",
        "稳赚",
        "保证收益",
        "可以重仓",
        "梭哈",
        "无脑买入",
    ]
    for phrase in banned_phrases:
        assert phrase not in report


def _render_sample_report() -> str:
    snapshot = collect_market_research_snapshot(date(2026, 5, 22))
    return render_ai_stock_report(snapshot, "2026-05-22")
