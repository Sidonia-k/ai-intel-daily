from ai_intel_daily.processors.dedupe import dedupe_items, normalize_title, normalize_url


def test_dedupe_removes_duplicate_urls():
    items = [
        {"title": "First", "url": "https://Example.com/news/"},
        {"title": "Second", "url": "https://example.com/news"},
        {"title": "Third", "url": "https://example.com/other"},
    ]

    unique = dedupe_items(items)

    assert [item["title"] for item in unique] == ["First", "Third"]


def test_dedupe_removes_duplicate_titles_when_url_is_missing():
    items = [
        {"title": "New Model: Ships Today!", "url": ""},
        {"title": "new model ships today", "url": ""},
        {"title": "Different title", "url": ""},
    ]

    unique = dedupe_items(items)

    assert [item["title"] for item in unique] == ["New Model: Ships Today!", "Different title"]


def test_normalizers_are_stable_for_stage4_contract():
    assert normalize_url("https://Example.com/path/#section") == "https://example.com/path"
    assert normalize_title("  模型，发布！ ") == "模型发布"
