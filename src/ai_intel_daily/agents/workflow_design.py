"""Planned Stage 7 daily report agent workflow."""

from __future__ import annotations

from dataclasses import dataclass

from ai_intel_daily.agents.agent_specs import (
    CYBER_COMMITTEE_AGENT,
    EDITOR_AGENT,
    FACT_CHECK_AGENT,
    FINANCIAL_SAFETY_AGENT,
    MARKET_AGENT,
    NEWS_AGENT,
)


@dataclass(frozen=True)
class WorkflowStep:
    """A planned workflow step, not an executable agent runtime."""

    name: str
    agent_name: str
    purpose: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    guardrails: tuple[str, ...] = ()


DAILY_AGENT_WORKFLOW: tuple[WorkflowStep, ...] = (
    WorkflowStep(
        name="news collection summary",
        agent_name=NEWS_AGENT,
        purpose="Summarize AI news from allowed local inputs.",
        inputs=("deduplicated RSS or Atom items",),
        outputs=("news notes", "news source list", "news uncertainties"),
        guardrails=("source_required", "no_real_api_calls"),
    ),
    WorkflowStep(
        name="market summary",
        agent_name=MARKET_AGENT,
        purpose="Summarize AI-related market context as research assistance.",
        inputs=("local or simulated market snapshot",),
        outputs=("market notes", "risk notes", "metrics to watch"),
        guardrails=("financial_safety", "simulated_data_notice", "no_real_api_calls"),
    ),
    WorkflowStep(
        name="cyber committee analysis",
        agent_name=CYBER_COMMITTEE_AGENT,
        purpose="Produce multi-perspective auxiliary analysis without trading advice.",
        inputs=("market notes", "risk notes", "metrics to watch"),
        outputs=("committee role views", "disagreements", "uncertainties"),
        guardrails=("research_assistance_only", "financial_safety"),
    ),
    WorkflowStep(
        name="fact check",
        agent_name=FACT_CHECK_AGENT,
        purpose="Review source coverage, citations, and unsupported claims.",
        inputs=("news notes", "market notes", "committee role views"),
        outputs=("fact-check notes", "citation gaps", "unsupported-claim warnings"),
        guardrails=("source_required", "facts_inferences_uncertainties_separated"),
    ),
    WorkflowStep(
        name="financial safety check",
        agent_name=FINANCIAL_SAFETY_AGENT,
        purpose="Block deterministic investment advice and verify required disclaimers.",
        inputs=("market notes", "committee role views", "draft stock-related sections"),
        outputs=("safety result", "blocked phrases", "disclaimer notes"),
        guardrails=("no_deterministic_advice", "required_disclaimer"),
    ),
    WorkflowStep(
        name="editor final markdown",
        agent_name=EDITOR_AGENT,
        purpose="Assemble the checked sections into final Markdown.",
        inputs=("news notes", "market notes", "fact-check notes", "safety result"),
        outputs=("final markdown report draft",),
        guardrails=("required_disclaimer", "facts_inferences_uncertainties_separated"),
    ),
)
