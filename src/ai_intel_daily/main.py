"""Local Markdown report generation entrypoint."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from ai_intel_daily.collectors.rss_collector import collect_from_config
from ai_intel_daily.processors.dedupe import dedupe_items
from ai_intel_daily.reports.ai_daily_report import render_ai_daily_report


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_AI_SOURCES_CONFIG = CONFIG_DIR / "ai_sources.yaml"
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "data" / "reports"

FINANCIAL_DISCLAIMER = (
    "本报告仅用于信息整理和研究辅助，不构成投资建议，"
    "不提供买入、卖出或持有建议，不承诺收益。"
)


def _bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _write_report(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def generate_ai_daily_report(
    output_dir: str | Path | None = None,
    report_date: date | None = None,
    sources_config_path: str | Path | None = None,
) -> Path:
    """Collect RSS items and generate the Stage 4 AI daily report."""
    target_date = report_date or date.today()
    date_text = target_date.isoformat()
    reports_dir = Path(output_dir) if output_dir is not None else DEFAULT_REPORTS_DIR
    config_path = Path(sources_config_path) if sources_config_path else DEFAULT_AI_SOURCES_CONFIG

    items = dedupe_items(collect_from_config(config_path))
    content = render_ai_daily_report(items, date_text)
    return _write_report(reports_dir / "ai" / f"{date_text}-ai-daily-report.md", content)


def generate_stock_research_report(
    output_dir: str | Path | None = None,
    report_date: date | None = None,
) -> Path:
    """Generate the local stock research Markdown report."""
    target_date = report_date or date.today()
    date_text = target_date.isoformat()
    reports_dir = Path(output_dir) if output_dir is not None else DEFAULT_REPORTS_DIR

    content = "\n".join(
        [
            "# AI 相关股市信息研究报告",
            "",
            f"日期：{date_text}",
            "",
            "> 阶段 4 本地报告：以下内容仅用于验证 Markdown 生成流程，不接真实市场数据源。",
            "",
            "## 安全声明",
            "",
            FINANCIAL_DISCLAIMER,
            "",
            "## 今日 AI 相关板块概览",
            "",
            _bullet_list(
                [
                    "示例数据：AI 芯片、云基础设施和应用软件板块均与算力需求叙事相关。",
                    "示例数据：当前仅展示报告结构，不引用真实行情、估值或财报数据。",
                ]
            ),
            "",
            "## 事实区",
            "",
            _bullet_list(
                [
                    "示例数据：某芯片公司强调数据中心需求是管理层关注重点。",
                    "示例数据：某云服务公司持续讨论 AI 基础设施资本开支。",
                    "示例数据：某软件公司将 AI 功能作为产品升级方向。",
                ]
            ),
            "",
            "## 合理推断区",
            "",
            _bullet_list(
                [
                    "示例数据：如果企业 AI 采用率提升，相关云资源和工具链需求可能更受关注。",
                    "示例数据：如果资本开支继续增加，研究时需要同时观察收入转化和现金流压力。",
                ]
            ),
            "",
            "## 不确定性区",
            "",
            _bullet_list(
                [
                    "示例数据：AI 需求增长速度、客户预算和竞争格局都仍不确定。",
                    "示例数据：不同公司对 AI 收入的披露口径可能不可直接比较。",
                ]
            ),
            "",
            "## 风险点",
            "",
            _bullet_list(
                [
                    "示例数据：估值波动、供应链限制和监管变化都可能影响研究结论。",
                    "示例数据：市场叙事可能先于基本面兑现，需要避免过度外推。",
                ]
            ),
            "",
            "## 后续关注指标",
            "",
            _bullet_list(
                [
                    "示例数据：后续关注 AI 相关收入占比、毛利率、资本开支和自由现金流。",
                    "示例数据：后续关注客户续费率、产品使用率和管理层对需求持续性的描述。",
                ]
            ),
            "",
        ]
    )
    return _write_report(reports_dir / "stocks" / f"{date_text}-ai-stock-report.md", content)


def generate_reports(
    output_dir: str | Path | None = None,
    report_date: date | None = None,
) -> tuple[Path, Path]:
    """Generate both reports for backward-compatible default behavior."""
    ai_path = generate_ai_daily_report(output_dir=output_dir, report_date=report_date)
    stock_path = generate_stock_research_report(output_dir=output_dir, report_date=report_date)
    return ai_path, stock_path


def _parse_report_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected date in YYYY-MM-DD format") from exc


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate local AI intelligence Markdown reports.")
    parser.add_argument("--date", type=_parse_report_date, help="Report date in YYYY-MM-DD format.")
    parser.add_argument(
        "--report",
        choices=("all", "ai", "stocks"),
        default="all",
        help="Report to generate. Defaults to all for compatibility.",
    )
    args = parser.parse_args(argv)

    if args.report == "ai":
        ai_path = generate_ai_daily_report(report_date=args.date)
        print(f"Generated AI report: {ai_path}")
        return

    if args.report == "stocks":
        stock_path = generate_stock_research_report(report_date=args.date)
        print(f"Generated stock research report: {stock_path}")
        return

    ai_path, stock_path = generate_reports(report_date=args.date)
    print(f"Generated AI report: {ai_path}")
    print(f"Generated stock research report: {stock_path}")


if __name__ == "__main__":
    main()
