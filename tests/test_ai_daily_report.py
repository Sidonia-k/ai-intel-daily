import re

import feedparser

from ai_intel_daily.collectors.rss_collector import collect_rss_items
from ai_intel_daily.reports.ai_daily_report import render_ai_daily_report


SAMPLE_DAILY_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Sample AI Daily Feed</title>
    <item>
      <title>Target day model update</title>
      <link>https://example.com/target-day</link>
      <pubDate>Sat, 23 May 2026 08:00:00 GMT</pubDate>
      <description>Published on the target date.</description>
    </item>
    <item>
      <title>Nearby product update</title>
      <link>https://example.com/nearby</link>
      <pubDate>Fri, 22 May 2026 01:00:00 GMT</pubDate>
      <description>Within the 36 hour window.</description>
    </item>
    <item>
      <title>Very old historical update</title>
      <link>https://example.com/old</link>
      <pubDate>Thu, 01 Jan 2015 08:00:00 GMT</pubDate>
      <description>This should not appear in a daily report.</description>
    </item>
  </channel>
</rss>
"""


def test_report_filters_old_rss_history_from_sample_feed():
    sources = [
        {
            "name": "Sample Daily RSS",
            "url": "https://example.com/rss.xml",
            "type": "rss",
            "category": "model",
            "enabled": True,
        }
    ]
    items = collect_rss_items(sources, parser=lambda url: feedparser.parse(SAMPLE_DAILY_RSS))

    report = render_ai_daily_report(items, "2026-05-23")

    assert "本报告仅展示目标日期附近的 RSS 条目，已过滤历史内容。" in report
    assert "Target day model update" in report
    assert "Nearby product update" in report
    assert "Very old historical update" not in report
    assert "过滤历史或超出数量上限 1 条" in report


def test_report_total_displayed_items_does_not_exceed_50():
    items = []
    categories = ["model", "product", "agent", "open_source", "research"]
    for index in range(80):
        category = categories[index % len(categories)]
        items.append(
            {
                "title": f"Recent item {index:02d}",
                "url": f"https://example.com/recent-{index:02d}",
                "source": f"Source {index:02d}",
                "published_at": f"2026-05-23T08:{index % 60:02d}:00+00:00",
                "summary": "",
                "category": category,
            }
        )

    report = render_ai_daily_report(items, "2026-05-23")

    assert report.count("](") <= 50
    assert "Recent item 79" in report
    assert "过滤历史或超出数量上限 30 条" in report
    for title in [
        "大模型发布与更新",
        "AI 产品更新",
        "Agent / MCP / Workflow / Skills 生态",
        "开源项目与开发者工具",
        "重要论文 / 技术趋势",
    ]:
        section = _section(report, title)
        assert len(re.findall(r"^- \[Recent item", section, flags=re.MULTILINE)) <= 10


def test_report_caps_each_category_section_at_10_items():
    items = [
        {
            "title": f"Model item {index:02d}",
            "url": f"https://example.com/model-{index:02d}",
            "source": "Model Source",
            "published_at": f"2026-05-23T{index % 24:02d}:00:00+00:00",
            "summary": "",
            "category": "model",
        }
        for index in range(30)
    ]

    report = render_ai_daily_report(items, "2026-05-23")
    model_section = _section(report, "大模型发布与更新")

    assert len(re.findall(r"^- \[Model item", model_section, flags=re.MULTILINE)) <= 10


def test_report_sources_only_include_displayed_items():
    items = [
        {
            "title": "Displayed recent item",
            "url": "https://example.com/displayed",
            "source": "Displayed Source",
            "published_at": "2026-05-23T08:00:00+00:00",
            "summary": "",
            "category": "product",
        },
        {
            "title": "Hidden old item",
            "url": "https://example.com/hidden-old",
            "source": "Hidden Old Source",
            "published_at": "2024-01-01T08:00:00+00:00",
            "summary": "",
            "category": "product",
        },
        {
            "title": "Hidden unknown date item",
            "url": "https://example.com/hidden-unknown",
            "source": "Hidden Unknown Source",
            "published_at": "not-a-date",
            "summary": "",
            "category": "product",
        },
    ]

    report = render_ai_daily_report(items, "2026-05-23")
    sources_section = _section(report, "来源列表")

    assert "Displayed Source: https://example.com/displayed" in sources_section
    assert "Hidden Old Source" not in sources_section
    assert "Hidden Unknown Source" not in sources_section
    assert "Hidden old item" not in report
    assert "Hidden unknown date item" not in report
    assert "过滤无法解析日期 1 条" in report


def _section(report: str, title: str) -> str:
    marker = f"## {title}"
    start = report.index(marker)
    next_start = report.find("\n## ", start + len(marker))
    if next_start == -1:
        return report[start:]
    return report[start:next_start]
