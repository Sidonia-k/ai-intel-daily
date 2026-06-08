"""Manual DeepSeek-backed agent runtime smoke for Stage 7D."""

from __future__ import annotations

from datetime import date
import os

from ai_intel_daily.agent_runtime.runtime_types import AgentRuntimeResult
from ai_intel_daily.agents.guardrails import (
    REQUIRED_FINANCIAL_DISCLAIMER,
    check_financial_safety_text,
)
from ai_intel_daily.collectors.market_collector import collect_market_research_snapshot
from ai_intel_daily.llm.deepseek_client import (
    DEFAULT_THINKING_DISABLED,
    DeepSeekClient,
    DeepSeekClientError,
)
from ai_intel_daily.llm.provider_config import ProviderConfig


WORKFLOW_NAME = "stage7d-deepseek-agent-runtime-smoke"


def run_deepseek_agent_runtime(report_date: date | str | None = None) -> AgentRuntimeResult:
    """Run a small manual DeepSeek workflow using only local mock inputs."""
    config = ProviderConfig(provider="deepseek", model=os.environ.get("LLM_MODEL", ""))
    target_date = _normalize_report_date(report_date)

    if not os.environ.get(config.api_key_env):
        return AgentRuntimeResult(
            provider="deepseek",
            model=config.model,
            workflow_name=WORKFLOW_NAME,
            final_markdown="",
            safety_passed=False,
            warnings=[
                "DEEPSEEK_API_KEY is not set. Set it locally before running the manual "
                "DeepSeek agent runtime smoke."
            ],
            used_real_api=False,
        )

    try:
        client = DeepSeekClient(
            model=config.model,
            base_url=os.environ.get("LLM_BASE_URL") or config.base_url,
        )
        response = client.generate(
            _build_messages(target_date),
            thinking=DEFAULT_THINKING_DISABLED,
        )
    except DeepSeekClientError as exc:
        return AgentRuntimeResult(
            provider="deepseek",
            model=config.model,
            workflow_name=WORKFLOW_NAME,
            final_markdown="",
            safety_passed=False,
            warnings=[f"DeepSeek agent runtime smoke failed: {exc}"],
            used_real_api=False,
        )

    markdown = _ensure_disclaimer(response.text)
    safety_check = check_financial_safety_text(markdown)
    warnings = []
    if not safety_check.passed:
        warnings.append("DeepSeek output did not pass the financial safety check.")
    if safety_check.blocked_phrases:
        warnings.append(
            "Blocked financial advice phrases: "
            + ", ".join(safety_check.blocked_phrases)
        )
    if safety_check.missing_disclaimer:
        warnings.append("DeepSeek output was missing the required financial disclaimer.")

    return AgentRuntimeResult(
        provider=response.provider,
        model=response.model,
        workflow_name=WORKFLOW_NAME,
        final_markdown=markdown,
        safety_passed=safety_check.passed,
        warnings=warnings,
        used_real_api=True,
    )


def _normalize_report_date(report_date: date | str | None) -> str:
    if report_date is None:
        return date.today().isoformat()
    if isinstance(report_date, date):
        return report_date.isoformat()
    return str(report_date)


def _build_messages(report_date: str) -> list[dict[str, str]]:
    snapshot = collect_market_research_snapshot(report_date)
    mock_news = [
        "Local mock news: a model provider described lower inference resource usage.",
        "Local mock news: enterprise AI pilots focused on workflow integration.",
        "Local mock news: open-source AI tooling activity remains a research variable.",
    ]
    prompt = "\n".join(
        [
            f"Report date: {report_date}",
            "",
            "Use only the local mock inputs below. Do not cite or request real market data.",
            "Write a minimal Chinese Markdown AI intelligence daily draft.",
            "Keep stock-related content as research assistance only.",
            "Do not provide buy, sell, hold, overweight, target-price, all-in, or guaranteed-return recommendations.",
            "Include this exact disclaimer:",
            REQUIRED_FINANCIAL_DISCLAIMER,
            "",
            "Mock news:",
            *[f"- {item}" for item in mock_news],
            "",
            "Mock market snapshot:",
            *[f"- {item}" for item in snapshot["market_overview"]],
            "",
            "Mock risks:",
            *[f"- {risk['name']}: {risk['detail']}" for risk in snapshot["risks"][:4]],
        ]
    )
    return [
        {
            "role": "system",
            "content": (
                "You are a cautious editor for a Stage 7D manual smoke test. "
                "Use only provided mock data and obey financial safety limits."
            ),
        },
        {"role": "user", "content": prompt},
    ]


def _ensure_disclaimer(markdown: str) -> str:
    clean_markdown = markdown.strip()
    if REQUIRED_FINANCIAL_DISCLAIMER in clean_markdown:
        return clean_markdown + "\n"
    return f"{clean_markdown}\n\n## Disclaimer\n\n{REQUIRED_FINANCIAL_DISCLAIMER}\n"
