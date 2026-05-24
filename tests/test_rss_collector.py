import logging
from pathlib import Path

import feedparser

from ai_intel_daily.collectors.rss_collector import collect_from_config, collect_rss_items, load_sources


SAMPLE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Sample AI Feed</title>
    <item>
      <title>Sample model launch</title>
      <link>https://example.com/model-launch</link>
      <pubDate>Fri, 22 May 2026 08:00:00 GMT</pubDate>
      <description>A short model launch summary.</description>
    </item>
  </channel>
</rss>
"""


SAMPLE_ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Sample Atom Feed</title>
  <entry>
    <title>Sample product update</title>
    <link href="https://example.com/product-update" />
    <updated>2026-05-22T09:00:00Z</updated>
    <summary>A short product update summary.</summary>
  </entry>
</feed>
"""


SAMPLE_HF_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Hugging Face Blog</title>
    <item>
      <title>Open source model tools</title>
      <guid isPermaLink="true">https://huggingface.co/blog/open-source-model-tools</guid>
      <pubDate>Fri, 22 May 2026 10:00:00 GMT</pubDate>
      <description>Developer tooling update.</description>
    </item>
  </channel>
</rss>
"""


TEST_OUTPUT_DIR = Path("data/test-output")


def test_rss_collector_parses_rss_items_to_uniform_shape():
    sources = [
        {
            "name": "Sample RSS",
            "url": "https://example.com/rss.xml",
            "type": "rss",
            "category": "model",
            "enabled": True,
        }
    ]

    items = collect_rss_items(sources, parser=lambda url: feedparser.parse(SAMPLE_RSS))

    assert items == [
        {
            "title": "Sample model launch",
            "url": "https://example.com/model-launch",
            "source": "Sample RSS",
            "published_at": "2026-05-22T08:00:00+00:00",
            "summary": "A short model launch summary.",
            "category": "model",
        }
    ]


def test_rss_collector_parses_atom_items_to_uniform_shape():
    sources = [
        {
            "name": "Sample Atom",
            "url": "https://example.com/feed.atom",
            "type": "rss",
            "category": "product",
            "enabled": True,
        }
    ]

    items = collect_rss_items(sources, parser=lambda url: feedparser.parse(SAMPLE_ATOM))

    assert items[0]["title"] == "Sample product update"
    assert items[0]["url"] == "https://example.com/product-update"
    assert items[0]["source"] == "Sample Atom"
    assert items[0]["category"] == "product"


def test_rss_collector_continues_when_one_source_fails(caplog):
    sources = [
        {
            "name": "Broken RSS",
            "url": "https://example.com/broken.xml",
            "type": "rss",
            "category": "model",
            "enabled": True,
        },
        {
            "name": "Working RSS",
            "url": "https://example.com/working.xml",
            "type": "rss",
            "category": "model",
            "enabled": True,
        },
    ]

    def parser(url):
        if "broken" in url:
            raise RuntimeError("network failed")
        return feedparser.parse(SAMPLE_RSS)

    with caplog.at_level(logging.WARNING):
        items = collect_rss_items(sources, parser=parser)

    assert len(items) == 1
    assert items[0]["source"] == "Working RSS"
    assert "Failed to read RSS source Broken RSS" in caplog.text


def test_rss_collector_keeps_entries_for_encoding_bozo_warning(caplog):
    sources = [
        {
            "name": "Google DeepMind News",
            "url": "https://deepmind.google/blog/rss.xml",
            "type": "rss",
            "category": "research",
            "enabled": True,
        }
    ]

    def parser(url):
        feed = feedparser.parse(SAMPLE_RSS)
        feed.bozo = True
        feed.bozo_exception = Exception("document declared as us-ascii, but parsed as utf-8")
        return feed

    with caplog.at_level(logging.WARNING):
        items = collect_rss_items(sources, parser=parser)

    assert len(items) == 1
    assert items[0]["source"] == "Google DeepMind News"
    assert items[0]["title"] == "Sample model launch"
    assert "parse warning but entries are available" in caplog.text


def test_rss_collector_skips_bozo_feed_without_entries(caplog):
    sources = [
        {
            "name": "Empty Broken RSS",
            "url": "https://example.com/empty-broken.xml",
            "type": "rss",
            "category": "research",
            "enabled": True,
        }
    ]

    def parser(url):
        feed = feedparser.parse("")
        feed.bozo = True
        feed.bozo_exception = Exception("document declared as us-ascii, but parsed as utf-8")
        return feed

    with caplog.at_level(logging.WARNING):
        items = collect_rss_items(sources, parser=parser)

    assert items == []
    assert "Failed to parse RSS source Empty Broken RSS" in caplog.text


def test_rss_collector_falls_back_to_guid_when_link_is_missing():
    sources = [
        {
            "name": "Hugging Face Blog",
            "url": "https://huggingface.co/blog/feed.xml",
            "type": "rss",
            "category": "open_source",
            "enabled": True,
        }
    ]

    items = collect_rss_items(sources, parser=lambda url: feedparser.parse(SAMPLE_HF_RSS))

    assert items[0]["url"] == "https://huggingface.co/blog/open-source-model-tools"
    assert items[0]["category"] == "open_source"


def test_collector_loads_yaml_config_and_collects_only_enabled_rss():
    TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config_path = TEST_OUTPUT_DIR / "ai_sources.yaml"
    config_path.write_text(
        """
sources:
  - name: Enabled RSS
    url: https://example.com/rss.xml
    type: rss
    category: model
    enabled: true
  - name: Disabled RSS
    url: https://example.com/disabled.xml
    type: rss
    category: product
    enabled: false
  - name: HTML Candidate
    url: https://example.com/html
    type: html
    category: tool
    enabled: true
""".strip(),
        encoding="utf-8",
    )

    requested_urls = []

    def parser(url):
        requested_urls.append(url)
        return feedparser.parse(SAMPLE_RSS)

    sources = load_sources(config_path)
    items = collect_from_config(config_path, parser=parser)

    assert len(sources) == 3
    assert requested_urls == ["https://example.com/rss.xml"]
    assert len(items) == 1
    assert items[0]["source"] == "Enabled RSS"
