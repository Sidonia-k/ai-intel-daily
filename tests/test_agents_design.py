from ai_intel_daily.agents.agent_specs import (
    AGENT_SPECS,
    CYBER_COMMITTEE_AGENT,
    FACT_CHECK_AGENT,
    FINANCIAL_SAFETY_AGENT,
    MARKET_AGENT,
    NEWS_AGENT,
    EDITOR_AGENT,
)
from ai_intel_daily.agents.guardrails import FINANCIAL_SAFETY_RULES
from ai_intel_daily.agents.workflow_design import DAILY_AGENT_WORKFLOW


EXPECTED_AGENT_NAMES = {
    NEWS_AGENT,
    MARKET_AGENT,
    CYBER_COMMITTEE_AGENT,
    FACT_CHECK_AGENT,
    FINANCIAL_SAFETY_AGENT,
    EDITOR_AGENT,
}


def test_all_stage7_agents_are_defined():
    assert {agent.name for agent in AGENT_SPECS} == EXPECTED_AGENT_NAMES

    for agent in AGENT_SPECS:
        assert agent.role
        assert agent.responsibilities
        assert agent.inputs
        assert agent.outputs
        assert agent.disallowed_actions
        assert agent.guardrails


def test_financial_safety_agent_exists():
    assert FINANCIAL_SAFETY_AGENT in {agent.name for agent in AGENT_SPECS}


def test_cyber_committee_agent_exists():
    assert CYBER_COMMITTEE_AGENT in {agent.name for agent in AGENT_SPECS}


def test_guardrails_include_ban_on_investment_advice():
    rules_text = " ".join(FINANCIAL_SAFETY_RULES).lower()

    assert "not investment advice" in rules_text
    assert "buy, sell, hold" in rules_text
    assert "deterministic" in rules_text
    assert "trading recommendations" in rules_text


def test_workflow_includes_fact_check_and_financial_safety_check():
    step_names = [step.name for step in DAILY_AGENT_WORKFLOW]
    agent_names = [step.agent_name for step in DAILY_AGENT_WORKFLOW]

    assert "fact check" in step_names
    assert "financial safety check" in step_names
    assert FACT_CHECK_AGENT in agent_names
    assert FINANCIAL_SAFETY_AGENT in agent_names
