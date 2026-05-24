"""RSS/Atom collection for AI daily reports."""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from pathlib import Path
from typing import Any, Callable, Iterable

import feedparser
import yaml


LOGGER = logging.getLogger(__name__)

FeedParser = Callable[[str], Any]


def load_sources(config_path: str | Path) -> list[dict[str, Any]]:
    """Load source definitions from a YAML config file."""
    path = Path(config_path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("expected 'sources' to be a list in AI sources config")
    return [source for source in sources if isinstance(source, dict)]


def collect_from_config(
    config_path: str | Path,
    parser: FeedParser = feedparser.parse,
) -> list[dict[str, str]]:
    """Collect RSS items from enabled RSS sources in a YAML config."""
    return collect_rss_items(load_sources(config_path), parser=parser)


def collect_rss_items(
    sources: Iterable[dict[str, Any]],
    parser: FeedParser = feedparser.parse,
) -> list[dict[str, str]]:
    """Collect normalized entries from enabled RSS/Atom sources.

    A single broken source is logged and skipped so report generation can
    continue with the remaining sources.
    """
    items: list[dict[str, str]] = []

    for source in sources:
        if not source.get("enabled", False) or source.get("type") != "rss":
            continue

        name = str(source.get("name", "")).strip() or "Unknown source"
        url = str(source.get("url", "")).strip()
        if not url:
            LOGGER.warning("Skipping RSS source %s because it has no URL.", name)
            continue

        try:
            feed = parser(url)
        except Exception as exc:  # pragma: no cover - defensive around parser/network
            LOGGER.warning("Failed to read RSS source %s: %s", name, exc)
            continue

        entries = getattr(feed, "entries", [])
        if getattr(feed, "bozo", False) and not _can_use_bozo_entries(feed, entries):
            LOGGER.warning(
                "Failed to parse RSS source %s: %s",
                name,
                getattr(feed, "bozo_exception", "unknown parse error"),
            )
            continue
        if getattr(feed, "bozo", False):
            LOGGER.warning(
                "RSS source %s had a parse warning but entries are available: %s",
                name,
                getattr(feed, "bozo_exception", "unknown parse error"),
            )

        for entry in entries:
            title = _text(entry.get("title"))
            if not title:
                continue
            items.append(
                {
                    "title": title,
                    "url": _entry_url(entry),
                    "source": name,
                    "published_at": _published_at(entry),
                    "summary": _text(entry.get("summary") or entry.get("description")),
                    "category": _text(source.get("category")),
                }
            )

    return items


def _can_use_bozo_entries(feed: Any, entries: list[Any]) -> bool:
    if not entries:
        return False
    message = str(getattr(feed, "bozo_exception", "")).lower()
    return "encoding" in message or "declared as" in message or "parsed as" in message


def _entry_url(entry: Any) -> str:
    for key in ("link", "id", "guid"):
        value = _text(entry.get(key))
        if value.startswith("http://") or value.startswith("https://"):
            return value
    return ""


def _published_at(entry: Any) -> str:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        parsed = entry.get(key)
        if parsed:
            return datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()
    return _text(entry.get("published") or entry.get("updated") or entry.get("created"))


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
