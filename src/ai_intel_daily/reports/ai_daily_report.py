"""Markdown rendering for the AI daily report."""

from __future__ import annotations

from datetime import datetime
import html


CATEGORY_SECTIONS = [
    ("model", "大模型发布与更新"),
    ("product", "AI 产品更新"),
    ("agent", "Agent / MCP / Workflow / Skills 生态"),
    ("tool", "开源项目与开发者工具"),
    ("open_source", "开源项目与开发者工具"),
    ("research", "重要论文 / 技术趋势"),
    ("company", "AI 产品更新"),
]

SECTION_TITLES = [
    "大模型发布与更新",
    "AI 产品更新",
    "Agent / MCP / Workflow / Skills 生态",
    "开源项目与开发者工具",
    "重要论文 / 技术趋势",
]


def render_ai_daily_report(items: list[dict[str, str]], report_date: str) -> str:
    """Render a Markdown AI daily report from normalized source items."""
    sorted_items = sorted(items, key=_sort_key, reverse=True)
    top_items = sorted_items[:5]
    section_map = _group_items(sorted_items)

    lines = [
        "# AI 圈日报",
        "",
        f"日期：{report_date}",
        "",
        "> 本报告基于配置的 RSS/公开信息源生成，仅做研究辅助；所有条目均来自来源列表，不编造来源。",
        "",
        "## 今日最值得关注的 3～5 件事",
        "",
        _render_items(top_items),
        "",
    ]

    for title in SECTION_TITLES:
        lines.extend([f"## {title}", "", _render_items(section_map.get(title, [])), ""])

    lines.extend(
        [
            "## 对我学习 Codex、agent、AI 应用的启发",
            "",
            _render_learning_notes(sorted_items),
            "",
            "## 来源列表",
            "",
            _render_sources(sorted_items),
            "",
        ]
    )
    return "\n".join(lines)


def _group_items(items: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    section_map = {title: [] for title in SECTION_TITLES}
    category_to_section = {category: title for category, title in CATEGORY_SECTIONS}

    for item in items:
        category = item.get("category", "")
        title = category_to_section.get(category, "AI 产品更新")
        section_map.setdefault(title, []).append(item)

    return section_map


def _render_items(items: list[dict[str, str]]) -> str:
    if not items:
        return "- 暂无有效数据。"

    lines = []
    for item in items:
        title = _clean_markdown(item.get("title", "Untitled"))
        source = _clean_markdown(item.get("source", "Unknown source"))
        url = item.get("url", "").strip()
        summary = _clean_markdown(_short_summary(item.get("summary", "")))
        published_at = _clean_markdown(item.get("published_at", ""))
        suffix = f"（{source}"
        if published_at:
            suffix += f"，{published_at}"
        suffix += "）"
        if url:
            line = f"- [{title}]({url}) {suffix}"
        else:
            line = f"- {title} {suffix}"
        if summary:
            line += f"：{summary}"
        lines.append(line)
    return "\n".join(lines)


def _render_learning_notes(items: list[dict[str, str]]) -> str:
    if not items:
        return "- 暂无有效数据。"

    notes = [
        "- 优先记录来源、标题、发布时间和链接，能让后续用 Codex 做复盘时快速回到原文。",
        "- 第一版只做可追溯整理，不做自动判断；等来源稳定后再考虑摘要、标签和优先级评分。",
    ]
    if any(item.get("category") in {"agent", "tool", "open_source"} for item in items):
        notes.append("- Agent、MCP、Workflow 和开发者工具类条目适合沉淀成后续实验清单。")
    return "\n".join(notes)


def _render_sources(items: list[dict[str, str]]) -> str:
    if not items:
        return "- 暂无有效数据。"

    seen: set[tuple[str, str]] = set()
    lines: list[str] = []
    for item in items:
        source = _clean_markdown(item.get("source", "Unknown source"))
        url = item.get("url", "").strip()
        key = (source, url)
        if key in seen:
            continue
        seen.add(key)
        if url:
            lines.append(f"- {source}: {url}")
        else:
            lines.append(f"- {source}")
    return "\n".join(lines)


def _short_summary(summary: str, limit: int = 180) -> str:
    value = " ".join(html.unescape(summary).split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def _clean_markdown(value: str) -> str:
    return " ".join(html.unescape(value).split())


def _sort_key(item: dict[str, str]) -> datetime:
    value = item.get("published_at", "").strip()
    if not value:
        return datetime.min
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return datetime.min
