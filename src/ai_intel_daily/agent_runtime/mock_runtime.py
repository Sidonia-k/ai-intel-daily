"""Offline mock agent runtime for Stage 7D."""

from __future__ import annotations

from datetime import date

from ai_intel_daily.agent_runtime.runtime_types import AgentRuntimeResult
from ai_intel_daily.agents.guardrails import check_financial_safety_text
from ai_intel_daily.agents.mock_workflow import run_mock_daily_agent_workflow
from ai_intel_daily.llm.mock_client import MockLLMClient
from ai_intel_daily.reports.agent_daily_report import render_agent_daily_report


WORKFLOW_NAME = "stage7d-mock-agent-runtime"


def run_mock_agent_runtime(report_date: date | str | None = None) -> AgentRuntimeResult:
    """Run the deterministic local workflow without network or secrets."""
    client = MockLLMClient(model="stage7d-mock-agent-runtime")
    workflow_result = run_mock_daily_agent_workflow(report_date=report_date)
    markdown = render_agent_daily_report(workflow_result)
    safety_check = check_financial_safety_text(markdown)

    warnings = [
        warning
        for step in workflow_result.get("steps", [])
        for warning in step.get("warnings", [])
    ]
    if not safety_check.passed:
        warnings.append("Mock runtime output did not pass the financial safety check.")

    return AgentRuntimeResult(
        provider=client.provider,
        model=client.model,
        workflow_name=WORKFLOW_NAME,
        final_markdown=markdown,
        safety_passed=safety_check.passed,
        warnings=warnings,
        used_real_api=False,
    )
