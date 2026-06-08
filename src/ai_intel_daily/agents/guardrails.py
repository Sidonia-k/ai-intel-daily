"""Local guardrail definitions for Stage 7 agent design."""

from __future__ import annotations

from dataclasses import dataclass


REQUIRED_FINANCIAL_DISCLAIMER = (
    "This report is for research assistance only, is not investment advice, "
    "and does not provide buy, sell, or hold recommendations."
)


PROHIBITED_INVESTMENT_ADVICE_PHRASES: tuple[str, ...] = (
    "recommend buying",
    "recommend selling",
    "recommend holding",
    "strong buy",
    "strong sell",
    "must buy",
    "must sell",
    "should buy",
    "should sell",
    "guaranteed return",
    "guaranteed profit",
    "risk-free profit",
    "price target",
    "overweight recommendation",
    "建议买入",
    "建议卖出",
    "建议持有",
    "强烈买入",
    "强烈卖出",
    "应该买入",
    "应该卖出",
    "可以买入",
    "可以重仓",
    "保证收益",
    "保证盈利",
    "目标价",
    "必然上涨",
    "必涨",
    "稳赚",
    "满仓",
)


FINANCIAL_SAFETY_RULES: tuple[str, ...] = (
    "Stock-related output must be research assistance only, not investment advice.",
    "Do not provide deterministic buy, sell, hold, overweight, or trading recommendations.",
    "Do not claim guaranteed returns, guaranteed profits, or certain price outcomes.",
    "Do not provide personalized trading actions or target-price instructions.",
    "Include a disclaimer that no buy, sell, or hold recommendations are provided.",
)


@dataclass(frozen=True)
class FinancialSafetyCheck:
    """Result from the local phrase-based financial safety check."""

    passed: bool
    blocked_phrases: tuple[str, ...]
    missing_disclaimer: bool


def check_financial_safety_text(text: str) -> FinancialSafetyCheck:
    """Check text against local Stage 7 financial safety rules."""
    lowered = text.lower()
    blocked = tuple(
        phrase for phrase in PROHIBITED_INVESTMENT_ADVICE_PHRASES if phrase.lower() in lowered
    )
    disclaimer_markers = (
        "not investment advice",
        "does not provide buy, sell, or hold recommendations",
        "不构成投资建议",
        "不提供买入、卖出或持有建议",
    )
    missing_disclaimer = not any(marker.lower() in lowered for marker in disclaimer_markers)
    return FinancialSafetyCheck(
        passed=not blocked and not missing_disclaimer,
        blocked_phrases=blocked,
        missing_disclaimer=missing_disclaimer,
    )
