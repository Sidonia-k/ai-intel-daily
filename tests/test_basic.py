from datetime import date
from pathlib import Path

import ai_intel_daily
import ai_intel_daily.main as main_module
from ai_intel_daily.main import generate_reports


def test_package_imports():
    assert ai_intel_daily.__version__ == "0.0.0"


def test_generate_reports_creates_fake_markdown_reports(tmp_path):
    ai_path, stock_path = generate_reports(output_dir=tmp_path, report_date=date(2026, 5, 22))

    assert ai_path == tmp_path / "ai" / "2026-05-22-ai-daily-report.md"
    assert stock_path == tmp_path / "stocks" / "2026-05-22-ai-stock-report.md"
    assert ai_path.exists()
    assert stock_path.exists()

    ai_report = ai_path.read_text(encoding="utf-8")
    stock_report = stock_path.read_text(encoding="utf-8")

    assert "阶段 0" in ai_report
    assert "假数据" in ai_report
    assert "研究辅助" in stock_report
    assert "不构成投资建议" in stock_report
    assert "不提供买入、卖出或持有建议" in stock_report


def test_main_uses_default_date_logic_when_date_is_not_provided(monkeypatch):
    calls = []

    def fake_generate_reports(output_dir=None, report_date=None):
        calls.append((output_dir, report_date))
        return Path("ai-report.md"), Path("stock-report.md")

    monkeypatch.setattr(main_module, "generate_reports", fake_generate_reports)

    main_module.main([])

    assert calls == [(None, None)]


def test_main_passes_cli_date_to_generate_reports(monkeypatch):
    calls = []

    def fake_generate_reports(output_dir=None, report_date=None):
        calls.append((output_dir, report_date))
        return Path("ai-report.md"), Path("stock-report.md")

    monkeypatch.setattr(main_module, "generate_reports", fake_generate_reports)

    main_module.main(["--date", "2026-05-22"])

    assert calls == [(None, date(2026, 5, 22))]


def test_ai_report_contains_required_sections(tmp_path):
    ai_path, _ = generate_reports(output_dir=tmp_path, report_date=date(2026, 5, 22))
    ai_report = ai_path.read_text(encoding="utf-8")

    required_sections = [
        "今日最值得关注的 3 件事",
        "AI 产品更新",
        "开源项目 / 开发者工具",
        "对我学习 AI 应用和 Codex 的启发",
    ]
    for section in required_sections:
        assert section in ai_report


def test_stock_report_contains_required_sections_and_disclaimer(tmp_path):
    _, stock_path = generate_reports(output_dir=tmp_path, report_date=date(2026, 5, 22))
    stock_report = stock_path.read_text(encoding="utf-8")

    required_sections = [
        "事实区",
        "合理推断区",
        "不确定性区",
        "风险点",
        "后续关注指标",
    ]
    for section in required_sections:
        assert section in stock_report
    assert "本报告仅用于信息整理和研究辅助，不构成投资建议，不提供买入、卖出或持有建议，不承诺收益。" in stock_report


def test_stock_report_avoids_deterministic_investment_advice(tmp_path):
    _, stock_path = generate_reports(output_dir=tmp_path, report_date=date(2026, 5, 22))
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
