"""Stage 0 report generation entrypoint."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "data" / "reports"

FINANCIAL_DISCLAIMER = "本报告仅用于信息整理和研究辅助，不构成投资建议，不提供买入、卖出或持有建议，不承诺收益。"


def _bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _render_template(template_name: str, values: dict[str, str]) -> str:
    template = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        template = template.replace("{{ " + key + " }}", value)
    return template


def _write_report(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def generate_reports(output_dir: str | Path | None = None, report_date: date | None = None) -> tuple[Path, Path]:
    """Generate the two Stage 0 fake-data Markdown reports."""
    target_date = report_date or date.today()
    date_text = target_date.isoformat()
    reports_dir = Path(output_dir) if output_dir is not None else DEFAULT_REPORTS_DIR

    ai_report = _render_template(
        "ai_daily_report.md",
        {
            "title": "AI 圈值得关注的变化报告",
            "date": date_text,
            "top_three": _bullet_list(
                [
                    "假数据：一家模型公司发布新的多模态演示，适合观察产品化节奏。",
                    "假数据：一个开源推理优化项目获得开发者关注，可能降低本地实验门槛。",
                    "假数据：企业 AI 工具继续向工作流集成方向发展。",
                ]
            ),
            "product_updates": _bullet_list(
                [
                    "假数据：写作助手新增团队知识库草稿能力。",
                    "假数据：会议总结工具优化了行动项提取体验。",
                ]
            ),
            "developer_tools": _bullet_list(
                [
                    "假数据：命令行代码助手加入更清晰的变更预览。",
                    "假数据：本地评测脚本模板开始支持多模型对比。",
                ]
            ),
            "learning_notes": _bullet_list(
                [
                    "假数据：学习 AI 应用时，应优先把输入、输出和失败边界写清楚。",
                    "假数据：使用 Codex 时，小步提交需求和测试条件能减少返工。",
                ]
            ),
            "follow_up_questions": _bullet_list(
                [
                    "假数据：哪些 AI 产品更新真正改善了日常工作流？",
                    "假数据：哪些开发者工具值得进入下一阶段的真实数据观察清单？",
                ]
            ),
        },
    )

    stock_report = _render_template(
        "ai_stock_report.md",
        {
            "title": "AI 相关股市信息研究报告",
            "date": date_text,
            "disclaimer": FINANCIAL_DISCLAIMER,
            "sector_overview": _bullet_list(
                [
                    "假数据：AI 芯片、云基础设施和应用软件板块均与算力需求叙事相关。",
                    "假数据：阶段 0 只展示报告结构，不引用真实行情、估值或财报数据。",
                ]
            ),
            "facts": _bullet_list(
                [
                    "假数据：某芯片公司强调数据中心需求是管理层关注重点。",
                    "假数据：某云服务公司持续讨论 AI 基础设施资本开支。",
                    "假数据：某软件公司将 AI 功能作为产品升级方向。",
                ]
            ),
            "reasoned_inferences": _bullet_list(
                [
                    "假数据：如果企业 AI 采用率提升，相关云资源和工具链需求可能更受关注。",
                    "假数据：如果资本开支继续增加，研究时需要同时观察收入转化和现金流压力。",
                ]
            ),
            "uncertainties": _bullet_list(
                [
                    "假数据：AI 需求增长速度、客户预算和竞争格局都仍不确定。",
                    "假数据：不同公司对 AI 收入的披露口径可能不可直接比较。",
                ]
            ),
            "risks": _bullet_list(
                [
                    "假数据：估值波动、供应链限制和监管变化都可能影响研究结论。",
                    "假数据：市场叙事可能先于基本面兑现，需避免过度外推。",
                ]
            ),
            "follow_up_metrics": _bullet_list(
                [
                    "假数据：后续关注 AI 相关收入占比、毛利率、资本开支和自由现金流。",
                    "假数据：后续关注客户续费率、产品使用率和管理层对需求持续性的描述。",
                ]
            ),
        },
    )

    ai_path = _write_report(reports_dir / "ai" / f"{date_text}-ai-daily-report.md", ai_report)
    stock_path = _write_report(reports_dir / "stocks" / f"{date_text}-ai-stock-report.md", stock_report)
    return ai_path, stock_path


def _parse_report_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected date in YYYY-MM-DD format") from exc


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate local AI intelligence Markdown reports.")
    parser.add_argument("--date", type=_parse_report_date, help="Report date in YYYY-MM-DD format.")
    args = parser.parse_args(argv)

    ai_path, stock_path = generate_reports(report_date=args.date)
    print(f"Generated AI report: {ai_path}")
    print(f"Generated stock research report: {stock_path}")


if __name__ == "__main__":
    main()
