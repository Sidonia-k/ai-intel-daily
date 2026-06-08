"""Markdown rendering for the AI stock research report."""

from __future__ import annotations

from typing import Any


FINANCIAL_DISCLAIMER = (
    "本报告仅用于信息整理和研究辅助，不构成投资建议，不提供买入、卖出或持有建议，"
    "不承诺收益。市场有风险，所有内容都需要结合更多数据独立判断。"
)

SIMULATED_DATA_NOTICE = "当前阶段使用本地模拟数据，不代表真实市场情况。"


def render_ai_stock_report(snapshot: dict[str, Any], report_date: str) -> str:
    """Render a Markdown AI stock research report from a local snapshot."""
    lines = [
        "# AI 相关股市信息研究报告",
        "",
        f"日期：{report_date}",
        "",
        "## 安全声明",
        "",
        "免责声明：",
        FINANCIAL_DISCLAIMER,
        "",
        SIMULATED_DATA_NOTICE,
        "",
        "## 今日概览",
        "",
        _render_list(snapshot.get("market_overview", [])),
        "",
        "## 事实区",
        "",
        "只放模拟数据中的可验证事实，不做主观判断。",
        "",
        _render_list(_facts(snapshot)),
        "",
        "## 合理推断区",
        "",
        "以下推断基于模拟事实做有限整理，并明确保留不确定性。",
        "",
        _render_list(_inferences(snapshot)),
        "",
        "## 不确定性区",
        "",
        _render_list(_uncertainties()),
        "",
        "## AI 产业链分类观察",
        "",
        _render_sectors(snapshot.get("sectors", [])),
        "",
        "## 重要公司新闻",
        "",
        _render_list(snapshot.get("company_news", [])),
        "",
        "## 风险点",
        "",
        _render_risks(snapshot.get("risks", [])),
        "",
        "## 后续关注指标",
        "",
        _render_list(snapshot.get("indicators_to_watch", [])),
        "",
    ]
    return "\n".join(lines)


def _facts(snapshot: dict[str, Any]) -> list[str]:
    facts: list[str] = []
    facts.extend(_as_strings(snapshot.get("company_news", [])))
    facts.extend(_as_strings(snapshot.get("earnings_events", [])))
    for sector in snapshot.get("sectors", []):
        if isinstance(sector, dict):
            facts.extend(_as_strings(sector.get("facts", [])))
    return facts


def _inferences(snapshot: dict[str, Any]) -> list[str]:
    inferences: list[str] = []
    for sector in snapshot.get("sectors", []):
        if not isinstance(sector, dict):
            continue
        name = str(sector.get("name", "")).strip()
        inference = str(sector.get("inference", "")).strip()
        if name and inference:
            inferences.append(f"{name}：{inference}")
    inferences.extend(_as_strings(snapshot.get("sentiment", [])))
    return inferences


def _uncertainties() -> list[str]:
    return [
        "当前信息不足以形成结论，需要进一步验证真实收入贡献和客户采用率。",
        "模拟数据没有包含真实行情、估值、成交量、财报数字或管理层原文。",
        "AI 需求、竞争格局、监管环境和宏观利率变化仍可能改变研究判断。",
    ]


def _render_sectors(sectors: Any) -> str:
    if not sectors:
        return "- 暂无有效数据。"

    lines: list[str] = []
    for sector in sectors:
        if not isinstance(sector, dict):
            continue
        name = str(sector.get("name", "")).strip()
        facts = _as_strings(sector.get("facts", []))
        inference = str(sector.get("inference", "")).strip()
        if not name:
            continue
        lines.append(f"### {name}")
        lines.append("")
        lines.append(_render_list(facts))
        if inference:
            lines.append("")
            lines.append(f"- 研究观察：{inference}")
        lines.append("")
    return "\n".join(lines).rstrip() or "- 暂无有效数据。"


def _render_risks(risks: Any) -> str:
    if not risks:
        return "- 暂无有效数据。"

    lines: list[str] = []
    for risk in risks:
        if isinstance(risk, dict):
            name = str(risk.get("name", "")).strip()
            detail = str(risk.get("detail", "")).strip()
            if name and detail:
                lines.append(f"- {name}：{detail}")
            elif name:
                lines.append(f"- {name}")
        elif str(risk).strip():
            lines.append(f"- {str(risk).strip()}")
    return "\n".join(lines) if lines else "- 暂无有效数据。"


def _render_list(items: Any) -> str:
    values = _as_strings(items)
    if not values:
        return "- 暂无有效数据。"
    return "\n".join(f"- {item}" for item in values)


def _as_strings(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    return [str(item).strip() for item in items if str(item).strip()]
