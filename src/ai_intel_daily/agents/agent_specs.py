"""Static agent specifications for the Stage 7 design skeleton."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSpec:
    """Configuration data for a planned report agent."""

    name: str
    role: str
    responsibilities: tuple[str, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    tools: tuple[str, ...]
    disallowed_actions: tuple[str, ...]
    guardrails: tuple[str, ...]


NEWS_AGENT = "News Agent"
MARKET_AGENT = "Market Agent"
CYBER_COMMITTEE_AGENT = "Cyber Committee Agent"
FACT_CHECK_AGENT = "Fact Check Agent"
FINANCIAL_SAFETY_AGENT = "Financial Safety Agent"
EDITOR_AGENT = "Editor Agent"


AGENT_SPECS: tuple[AgentSpec, ...] = (
    AgentSpec(
        name=NEWS_AGENT,
        role="AI news organizer",
        responsibilities=(
            "Summarize AI industry news from allowed local inputs.",
            "Group news items by topic while preserving sources.",
            "Mark unclear or incomplete items as uncertain.",
        ),
        inputs=("RSS or Atom items", "source names", "URLs", "timestamps", "summaries"),
        outputs=("topic-grouped news notes", "source list", "uncertainty notes"),
        tools=("rss_collector", "dedupe_processor", "future_source_metadata_parser"),
        disallowed_actions=(
            "invent sources",
            "claim unverified facts",
            "call real APIs during Stage 7",
            "write trading conclusions",
        ),
        guardrails=("source_required", "uncertainty_labeling", "no_real_api_calls"),
    ),
    AgentSpec(
        name=MARKET_AGENT,
        role="AI market context organizer",
        responsibilities=(
            "Organize AI-related market context as research assistance.",
            "Track sector themes, business metrics, and risk factors.",
            "Preserve simulated-data notices when inputs are simulated.",
        ),
        inputs=("market research snapshot", "sector list", "company news", "risk categories"),
        outputs=("market context notes", "risk notes", "metrics to watch"),
        tools=("local_market_snapshot_reader", "future_earnings_calendar_reader"),
        disallowed_actions=(
            "connect to real financial APIs during Stage 7",
            "produce buy, sell, hold, overweight, or target-price language",
            "claim guaranteed returns",
            "use private information",
        ),
        guardrails=("financial_safety", "simulated_data_notice", "no_real_api_calls"),
    ),
    AgentSpec(
        name=CYBER_COMMITTEE_AGENT,
        role="multi-perspective research assistant",
        responsibilities=(
            "Apply the cyber committee style to auxiliary analysis.",
            "Compare viewpoints and disagreements.",
            "Surface follow-up questions without making trading decisions.",
        ),
        inputs=("market context", "risk lists", "uncertainty notes", "financial safety policy"),
        outputs=("role views", "committee consensus", "disagreements", "follow-up indicators"),
        tools=("local_committee_role_templates", "future_scenario_checklist"),
        disallowed_actions=(
            "provide personalized investment advice",
            "state deterministic trading actions",
            "choose winners as recommendations",
            "weaken safety disclaimers",
        ),
        guardrails=("financial_safety", "research_assistance_only", "uncertainty_labeling"),
    ),
    AgentSpec(
        name=FACT_CHECK_AGENT,
        role="source and claim checker",
        responsibilities=(
            "Check source coverage and citation gaps.",
            "Separate facts from inferences and uncertainties.",
            "Flag unsupported statements before editing.",
        ),
        inputs=("news notes", "market notes", "committee analysis", "source metadata"),
        outputs=("fact-check notes", "citation gaps", "unsupported-claim warnings"),
        tools=("future_citation_checker", "future_source_url_validator", "dedupe_processor"),
        disallowed_actions=(
            "invent citations",
            "silently convert unsupported claims into facts",
            "skip uncertainty labels",
        ),
        guardrails=("source_required", "facts_inferences_uncertainties_separated"),
    ),
    AgentSpec(
        name=FINANCIAL_SAFETY_AGENT,
        role="stock-report safety reviewer",
        responsibilities=(
            "Enforce stock-report safety boundaries.",
            "Block deterministic investment advice.",
            "Check that required disclaimers are present.",
        ),
        inputs=("market notes", "committee analysis", "draft markdown", "financial safety policy"),
        outputs=("safety result", "blocked phrases", "required disclaimer notes"),
        tools=("financial_policy_scanner", "report_section_validator"),
        disallowed_actions=(
            "approve buy, sell, hold, overweight, or trading recommendations",
            "approve guaranteed-return language",
            "approve target-price instructions",
        ),
        guardrails=("financial_safety", "required_disclaimer", "no_deterministic_advice"),
    ),
    AgentSpec(
        name=EDITOR_AGENT,
        role="final Markdown report editor",
        responsibilities=(
            "Assemble checked sections into final Markdown.",
            "Preserve citations, uncertainty labels, and disclaimers.",
            "Keep facts, inferences, and uncertainties visibly separated.",
        ),
        inputs=("checked news notes", "checked market notes", "safety result", "fact-check notes"),
        outputs=("final markdown report draft",),
        tools=("markdown_template_renderer", "future_style_checker"),
        disallowed_actions=(
            "remove safety disclaimers",
            "turn uncertainty into certainty",
            "invent sources",
            "add trading advice",
        ),
        guardrails=("required_disclaimer", "source_required", "facts_inferences_uncertainties_separated"),
    ),
)


def get_agent_spec(name: str) -> AgentSpec:
    """Return an agent spec by exact name."""
    for spec in AGENT_SPECS:
        if spec.name == name:
            return spec
    raise KeyError(f"Unknown agent spec: {name}")
