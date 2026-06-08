"""Local Markdown report generation entrypoint."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from ai_intel_daily.collectors.market_collector import collect_market_research_snapshot
from ai_intel_daily.collectors.rss_collector import collect_from_config
from ai_intel_daily.processors.dedupe import dedupe_items
from ai_intel_daily.reports.ai_daily_report import render_ai_daily_report
from ai_intel_daily.reports.ai_stock_report import render_ai_stock_report


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DEFAULT_AI_SOURCES_CONFIG = CONFIG_DIR / "ai_sources.yaml"
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "data" / "reports"


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

    snapshot = collect_market_research_snapshot(target_date)
    content = render_ai_stock_report(snapshot, date_text)
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
