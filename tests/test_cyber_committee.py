from datetime import date

from ai_intel_daily.collectors.market_collector import collect_market_research_snapshot
from ai_intel_daily.committee.cyber_committee import (
    COMMITTEE_FINANCIAL_SAFETY_DISCLAIMER,
    build_cyber_committee_analysis,
)
from ai_intel_daily.committee.roles import CYBER_ROLES


EXPECTED_ROLE_NAMES = [
    "Cyber Buffett",
    "Cyber Munger",
    "Cyber Graham",
    "Cyber Damodaran",
    "Cyber Wood",
    "Cyber Lynch",
    "Cyber Taleb",
    "Cyber Huang",
]


def test_cyber_roles_are_defined_with_required_fields():
    assert [role["name"] for role in CYBER_ROLES] == EXPECTED_ROLE_NAMES

    for role in CYBER_ROLES:
        assert role["name"]
        assert role["focus"]
        assert isinstance(role["key_questions"], list)
        assert role["key_questions"]


def test_cyber_committee_analysis_contains_required_sections():
    snapshot = collect_market_research_snapshot(date(2026, 5, 22))

    analysis = build_cyber_committee_analysis(snapshot)

    assert set(analysis) == {
        "facts_basis",
        "role_views",
        "committee_consensus",
        "major_disagreements",
        "uncertainties",
        "follow_up_indicators",
        "financial_safety_disclaimer",
    }
    assert analysis["financial_safety_disclaimer"] == COMMITTEE_FINANCIAL_SAFETY_DISCLAIMER
    assert [role["name"] for role in analysis["role_views"]] == EXPECTED_ROLE_NAMES
    assert analysis["facts_basis"]
    assert analysis["committee_consensus"]
    assert analysis["major_disagreements"]
    assert analysis["uncertainties"]
    assert analysis["follow_up_indicators"]


def test_cyber_committee_analysis_avoids_deterministic_advice_phrases():
    snapshot = collect_market_research_snapshot(date(2026, 5, 22))
    analysis_text = str(build_cyber_committee_analysis(snapshot))

    allowed_disclaimer = "不提供买入、卖出或持有建议"
    assert allowed_disclaimer in analysis_text

    banned_phrases = [
        "建议买入",
        "建议卖出",
        "推荐买入",
        "推荐卖出",
        "强烈买入",
        "强烈卖出",
        "必然上涨",
        "保证收益",
        "稳赚",
        "目标价",
    ]
    for phrase in banned_phrases:
        assert phrase not in analysis_text
