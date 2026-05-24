"""Markdown rendering for the AI daily report."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
import html


MAX_REPORT_ITEMS = 50
MAX_TOP_ITEMS = 5
MAX_SECTION_ITEMS = 10
WINDOW_HOURS = 36

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


@dataclass(frozen=True)
class FilterStats:
    collected: int
    in_window: int
    shown: int
    filtered_by_date: int
    filtered_unknown_date: int


def render_ai_daily_report(items: list[dict[str, str]], report_date: str) -> str:
    """Render a Markdown AI daily report from normalized source items."""
    target_date = date.fromisoformat(report_date)
    filtered_items, stats = _filter_items_for_date(items, target_date)
    top_items, section_map, displayed_items = _select_display_items(filtered_items)
    stats = FilterStats(
        collected=stats.collected,
        in_window=stats.in_window,
        shown=len(displayed_items),
        filtered_by_date=stats.filtered_by_date,
        filtered_unknown_date=stats.filtered_unknown_date,
    )

    lines = [
        "# AI 圈日报",
        "",
        f"日期：{report_date}",
        "",
        "> 本报告基于配置的 RSS/公开信息源生成，仅做研究辅助；所有条目均来自来源列表，不编造来源。",
        "> 本报告仅展示目标日期附近的 RSS 条目，已过滤历史内容。",
        "",
        _render_filter_summary(stats),
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
            _render_learning_notes(displayed_items),
            "",
            "## 来源列表",
            "",
            _render_sources(displayed_items),
            "",
        ]
    )
    return "\n".join(lines)


def _filter_items_for_date(
    items: list[dict[str, str]],
    target_date: date,
) -> tuple[list[dict[str, str]], FilterStats]:
    window_start = datetime.combine(target_date, time(hour=12)) - timedelta(hours=WINDOW_HOURS)
    window_end = datetime.combine(target_date, time(hour=12)) + timedelta(hours=WINDOW_HOURS)
    filtered: list[dict[str, str]] = []
    filtered_by_date = 0
    filtered_unknown_date = 0

    for item in items:
        published_at = _parse_published_at(item.get("published_at", ""))
        if published_at is None:
            filtered_unknown_date += 1
            continue
        if not window_start <= published_at <= window_end:
            filtered_by_date += 1
            continue
        filtered.append(item)

    filtered.sort(key=_sort_key, reverse=True)
    limited = filtered[:MAX_REPORT_ITEMS]
    return limited, FilterStats(
        collected=len(items),
        in_window=len(filtered),
        shown=len(limited),
        filtered_by_date=filtered_by_date + max(0, len(filtered) - MAX_REPORT_ITEMS),
        filtered_unknown_date=filtered_unknown_date,
    )


def _select_display_items(
    items: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]], list[dict[str, str]]]:
    top_items = items[:MAX_TOP_ITEMS]
    top_keys = {_item_key(item) for item in top_items}
    section_map = {title: [] for title in SECTION_TITLES}
    category_to_section = {category: title for category, title in CATEGORY_SECTIONS}
    remaining_slots = max(0, MAX_REPORT_ITEMS - len(top_items))
    section_count = 0

    for item in items:
        if _item_key(item) in top_keys:
            continue
        if section_count >= remaining_slots:
            break
        section_title = category_to_section.get(item.get("category", ""), "AI 产品更新")
        section_items = section_map.setdefault(section_title, [])
        if len(section_items) >= MAX_SECTION_ITEMS:
            continue
        section_items.append(item)
        section_count += 1

    displayed_items = top_items[:]
    for title in SECTION_TITLES:
        displayed_items.extend(section_map.get(title, []))

    return top_items, section_map, displayed_items


def _render_filter_summary(stats: FilterStats) -> str:
    return (
        f"> 采集 {stats.collected} 条；目标日期窗口内 {stats.in_window} 条；"
        f"本报告展示 {stats.shown} 条；"
        f"过滤历史或超出数量上限 {stats.filtered_by_date} 条；"
        f"过滤无法解析日期 {stats.filtered_unknown_date} 条。"
    )


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
    return _parse_published_at(item.get("published_at", "")) or datetime.min


def _parse_published_at(value: str) -> datetime | None:
    text = value.strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is not None:
        return parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _item_key(item: dict[str, str]) -> tuple[str, str, str]:
    return (
        item.get("url", "").strip(),
        item.get("title", "").strip(),
        item.get("published_at", "").strip(),
    )
