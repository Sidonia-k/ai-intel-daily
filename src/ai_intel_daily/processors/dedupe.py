"""Deduplication helpers for collected AI intelligence items."""

from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit


_TITLE_PUNCTUATION = re.compile(r"[\s\.,;:!\?\-_\(\)\[\]\{\}'\"`~，。！？、；：《》“”‘’（）【】]+")


def dedupe_items(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """Deduplicate items by URL first, then normalized title when URL is absent."""
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[dict[str, str]] = []

    for item in items:
        normalized_url = normalize_url(item.get("url", ""))
        if normalized_url:
            if normalized_url in seen_urls:
                continue
            seen_urls.add(normalized_url)
            unique.append(item)
            continue

        normalized_title = normalize_title(item.get("title", ""))
        if normalized_title and normalized_title in seen_titles:
            continue
        if normalized_title:
            seen_titles.add(normalized_title)
        unique.append(item)

    return unique


def normalize_url(url: str) -> str:
    """Normalize URLs enough for first-pass duplicate detection."""
    value = url.strip()
    if not value:
        return ""
    parts = urlsplit(value)
    path = parts.path.rstrip("/") or parts.path
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def normalize_title(title: str) -> str:
    """Normalize a title by removing spaces and common punctuation."""
    return _TITLE_PUNCTUATION.sub("", title.lower()).strip()
