"""Executable local mock workflow for the Stage 7B agent design."""

from __future__ import annotations

from datetime import date
from typing import Any

from ai_intel_daily.agents import guardrails
from ai_intel_daily.agents.agent_specs import (
    CYBER_COMMITTEE_AGENT,
    EDITOR_AGENT,
    FACT_CHECK_AGENT,
    FINANCIAL_SAFETY_AGENT,
    MARKET_AGENT,
    NEWS_AGENT,
)
from ai_intel_daily.agents.workflow_design import DAILY_AGENT_WORKFLOW
from ai_intel_daily.llm.mock_client import MockLLMClient


MOCK_DATA_NOTICE = (
    "阶段 7B 本地 mock 模拟运行：所有输入均为确定性的本地假数据；"
    "不调用真实 OpenAI、DeepSeek、财经或其他外部数据 API。"
)

CHINESE_FINANCIAL_DISCLAIMER = (
    "本报告仅用于研究辅助，不构成投资建议，不提供买入、卖出或持有建议，也不承诺收益。"
)


def run_mock_daily_agent_workflow(report_date: date | str | None = None) -> dict[str, Any]:
    """Run the deterministic local Stage 7B mock agent workflow."""
    target_date = _normalize_report_date(report_date)
    mock_inputs = _build_mock_inputs(target_date)
    mock_client = MockLLMClient(model="stage7b-mock-agent")

    steps: list[dict[str, Any]] = []
    news_step = _run_news_agent(mock_inputs["news"], mock_client)
    steps.append(news_step)

    market_step = _run_market_agent(mock_inputs["market"], mock_client)
    steps.append(market_step)

    committee_step = _run_cyber_committee_agent(
        market_step["output"],
        mock_inputs["committee"],
        mock_client,
    )
    steps.append(committee_step)

    fact_check_step = _run_fact_check_agent(news_step, market_step, committee_step)
    steps.append(fact_check_step)

    safety_step = _run_financial_safety_agent(
        market_step,
        committee_step,
        fact_check_step,
    )
    steps.append(safety_step)

    editor_step = _run_editor_agent(target_date, steps)
    steps.append(editor_step)

    return {
        "report_date": target_date,
        "mock": True,
        "mock_data_notice": MOCK_DATA_NOTICE,
        "workflow": [step.agent_name for step in DAILY_AGENT_WORKFLOW],
        "steps": steps,
        "markdown": editor_step["output"]["markdown"],
    }


def _normalize_report_date(report_date: date | str | None) -> str:
    if report_date is None:
        return date.today().isoformat()
    if isinstance(report_date, date):
        return report_date.isoformat()
    return str(report_date)


def _build_mock_inputs(report_date: str) -> dict[str, Any]:
    return {
        "news": [
            {
                "title": "模拟模型发布说明强调更低推理资源占用",
                "summary": "本地样例称，某模拟模型供应商在发布说明中描述了更低的服务成本。",
                "source": "本地模拟 AI 新闻简报",
                "source_ref": "local-mock://ai-news/model-release",
                "published_at": f"{report_date}T08:00:00",
                "claim_type": "fact",
            },
            {
                "title": "模拟企业 AI 试点关注工作流集成",
                "summary": "本地样例描述了围绕搜索、客服和软件开发流程的企业 AI 试点。",
                "source": "本地模拟企业观察",
                "source_ref": "local-mock://ai-news/enterprise-pilots",
                "published_at": f"{report_date}T09:30:00",
                "claim_type": "fact",
            },
            {
                "title": "模拟开源工具生态保持活跃",
                "summary": "本地样例显示开发者兴趣仍在延续，但没有验证真实代码仓库活动。",
                "source": "本地模拟开发者生态观察",
                "source_ref": "local-mock://ai-news/tooling",
                "published_at": f"{report_date}T11:00:00",
                "claim_type": "uncertainty",
            },
        ],
        "market": {
            "overview": [
                {
                    "text": "模拟 AI 基础设施需求被整理为一个研究主题。",
                    "source": "本地模拟市场快照",
                    "claim_type": "fact",
                },
                {
                    "text": "云、芯片、数据中心和软件采用被拆分为独立的本地样例类别。",
                    "source": "本地模拟市场快照",
                    "claim_type": "fact",
                },
            ],
            "inferences": [
                {
                    "text": "如果 AI 工作负载采用范围扩大，基础设施利用率可能仍是重要研究变量。",
                    "source": "本地模拟市场快照",
                    "claim_type": "inference",
                }
            ],
            "uncertainties": [
                {
                    "text": "本地 mock 数据不包含真实价格、财务报表、业绩会内容或客户采用指标。",
                    "source": "本地模拟市场快照",
                    "claim_type": "uncertainty",
                }
            ],
            "risks": [
                "估值敏感性",
                "竞争变化",
                "供应链产能",
                "监管变化",
                "利率环境",
            ],
        },
        "committee": {
            "role_views": [
                {
                    "role": "Cyber Buffett",
                    "view": "关注长期业务质量，以及需求能否反复出现的证据。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
                {
                    "role": "Cyber Munger",
                    "view": "列出乐观 AI 基础设施叙事可能出错的路径。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
                {
                    "role": "Cyber Graham",
                    "view": "保持事实、假设和未知项可见分离。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
                {
                    "role": "Cyber Damodaran",
                    "view": "拆分收入、利润率、资本开支和资金成本等变量，避免直接给出估值结论。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
                {
                    "role": "Cyber Wood",
                    "view": "关注技术扩散路径和长期可选性，同时保留采用节奏的不确定性。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
                {
                    "role": "Cyber Lynch",
                    "view": "从产品使用、客户反馈和可理解的业务线索观察 AI 应用落地。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
                {
                    "role": "Cyber Taleb",
                    "view": "重点检查供应链、监管、能源和利率等尾部风险。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
                {
                    "role": "Cyber Huang",
                    "view": "从加速计算、系统架构、开发者生态和供给约束观察产业链协同。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                },
            ],
            "uncertainties": [
                {
                    "text": "真实公司文件和真实市场数据在本阶段被有意排除。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "uncertainty",
                }
            ],
        },
    }


def _run_news_agent(items: list[dict[str, str]], mock_client: MockLLMClient) -> dict[str, Any]:
    response = mock_client.complete(
        "按主题整理本地 mock AI 新闻条目。",
        system=NEWS_AGENT,
    )
    topics = [
        {"topic": "模型与推理", "items": [items[0]]},
        {"topic": "企业采用", "items": [items[1]]},
        {"topic": "开发者生态", "items": [items[2]]},
    ]
    return _step(
        NEWS_AGENT,
        f"{len(items)} 条本地模拟 AI 新闻",
        {
            "topics": topics,
            "sources": sorted({item["source"] for item in items}),
            "mock_client_response": response.text,
        },
        [],
    )


def _run_market_agent(snapshot: dict[str, Any], mock_client: MockLLMClient) -> dict[str, Any]:
    response = mock_client.complete(
        "将本地 mock AI 市场背景整理为研究辅助内容。",
        system=MARKET_AGENT,
    )
    return _step(
        MARKET_AGENT,
        "本地模拟 AI 市场快照",
        {
            "facts": snapshot["overview"],
            "inferences": snapshot["inferences"],
            "uncertainties": snapshot["uncertainties"],
            "risks": snapshot["risks"],
            "mock_client_response": response.text,
        },
        ["市场背景为模拟内容，不是真实市场数据。"],
    )


def _run_cyber_committee_agent(
    market_output: dict[str, Any],
    committee_input: dict[str, Any],
    mock_client: MockLLMClient,
) -> dict[str, Any]:
    response = mock_client.complete(
        "对比本地 mock 委员会视角，不输出交易指令。",
        system=CYBER_COMMITTEE_AGENT,
    )
    return _step(
        CYBER_COMMITTEE_AGENT,
        "市场背景加本地赛博委员会角色提示",
        {
            "role_views": committee_input["role_views"],
            "consensus": [
                {
                    "text": "模拟委员会将输出限制为研究问题、风险复核和证据追踪。",
                    "source": "本地模拟委员会输入",
                    "claim_type": "inference",
                }
            ],
            "disagreements": ["成长视角更重视采用路径，风险视角更重视证据缺口。"],
            "uncertainties": committee_input["uncertainties"] + market_output["uncertainties"],
            "mock_client_response": response.text,
        },
        ["委员会输出仅用于辅助研究。"],
    )


def _run_fact_check_agent(*prior_steps: dict[str, Any]) -> dict[str, Any]:
    claims = _extract_claims(prior_steps)
    missing_sources = [
        claim["text"] for claim in claims if not str(claim.get("source", "")).strip()
    ]
    missing_claim_types = [
        claim["text"]
        for claim in claims
        if claim.get("claim_type") not in {"fact", "inference", "uncertainty"}
    ]
    warnings = []
    if missing_sources:
        warnings.append("部分声明缺少来源。")
    if missing_claim_types:
        warnings.append("部分声明缺少事实/推断/不确定性标签。")

    return _step(
        FACT_CHECK_AGENT,
        f"来自前序 mock agent 的 {len(claims)} 条结构化声明",
        {
            "checked_claim_count": len(claims),
            "has_sources": not missing_sources,
            "separates_facts_inferences_uncertainties": not missing_claim_types,
            "missing_sources": missing_sources,
            "missing_claim_type_labels": missing_claim_types,
        },
        warnings,
    )


def _run_financial_safety_agent(*prior_steps: dict[str, Any]) -> dict[str, Any]:
    draft_text = _draft_safety_text(prior_steps)
    safety_check = guardrails.check_financial_safety_text(draft_text)
    warnings = []
    if safety_check.blocked_phrases:
        warnings.append("检测到被禁止的投资建议表达。")
    if safety_check.missing_disclaimer:
        warnings.append("缺少必要的金融安全免责声明。")

    return _step(
        FINANCIAL_SAFETY_AGENT,
        "与股票相关的 mock 市场和委员会段落",
        {
            "passed": safety_check.passed,
            "blocked_phrases": list(safety_check.blocked_phrases),
            "missing_disclaimer": safety_check.missing_disclaimer,
            "disclaimer": CHINESE_FINANCIAL_DISCLAIMER,
            "rules": list(guardrails.FINANCIAL_SAFETY_RULES),
        },
        warnings,
    )


def _run_editor_agent(report_date: str, prior_steps: list[dict[str, Any]]) -> dict[str, Any]:
    markdown = _render_editor_markdown(report_date, prior_steps)
    return _step(
        EDITOR_AGENT,
        "已检查的 mock workflow 输出",
        {
            "markdown": markdown,
            "section_count": markdown.count("\n## "),
        },
        [],
    )


def _step(
    agent_name: str,
    input_summary: str,
    output: dict[str, Any],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "agent_name": agent_name,
        "input_summary": input_summary,
        "output": output,
        "warnings": warnings,
    }


def _extract_claims(steps: tuple[dict[str, Any], ...]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    for step in steps:
        claims.extend(_claims_from_value(step["output"]))
    return claims


def _claims_from_value(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        found: list[dict[str, Any]] = []
        if "source" in value or "claim_type" in value:
            found.append(
                {
                    "text": str(value.get("text") or value.get("summary") or value.get("view") or ""),
                    "source": value.get("source", ""),
                    "claim_type": value.get("claim_type", ""),
                }
            )
        for child in value.values():
            found.extend(_claims_from_value(child))
        return found
    if isinstance(value, list):
        found = []
        for item in value:
            found.extend(_claims_from_value(item))
        return found
    return []


def _draft_safety_text(steps: tuple[dict[str, Any], ...]) -> str:
    claim_text = " ".join(claim["text"] for claim in _extract_claims(steps))
    return f"{claim_text}\n\n{guardrails.REQUIRED_FINANCIAL_DISCLAIMER}"


def _render_editor_markdown(report_date: str, steps: list[dict[str, Any]]) -> str:
    step_by_agent = {step["agent_name"]: step for step in steps}
    lines = [
        "# 阶段 7B 本地 Mock Agent 日报",
        "",
        f"日期：{report_date}",
        "",
        "## 本地 Mock 说明",
        "",
        MOCK_DATA_NOTICE,
        "",
        "## News Agent 输出",
        "",
        _render_news(step_by_agent[NEWS_AGENT]["output"]),
        "",
        "## Market Agent 输出",
        "",
        _render_market(step_by_agent[MARKET_AGENT]["output"]),
        "",
        "## Cyber Committee Agent 输出",
        "",
        _render_committee(step_by_agent[CYBER_COMMITTEE_AGENT]["output"]),
        "",
        "## Fact Check Agent 输出",
        "",
        _render_fact_check(step_by_agent[FACT_CHECK_AGENT]["output"]),
        "",
        "## Financial Safety Agent 输出",
        "",
        _render_financial_safety(step_by_agent[FINANCIAL_SAFETY_AGENT]["output"]),
        "",
        "## Editor Agent 汇总",
        "",
        "- 最终报告由本地 mock agent 输出整合而成。",
        "- 事实、推断和不确定性在来源段落中保持标签。",
        "- 写入报告前保留金融安全免责声明。",
        "",
        "## 免责声明",
        "",
        CHINESE_FINANCIAL_DISCLAIMER,
        "",
    ]
    return "\n".join(lines)


def _render_news(output: dict[str, Any]) -> str:
    lines: list[str] = []
    for topic in output.get("topics", []):
        lines.append(f"### {topic['topic']}")
        for item in topic.get("items", []):
            lines.append(
                "- "
                f"[{item['claim_type']}] {item['title']} "
                f"（来源：{item['source']}；引用：{item['source_ref']}）。摘要：{item['summary']}"
            )
        lines.append("")
    return "\n".join(lines).rstrip()


def _render_market(output: dict[str, Any]) -> str:
    lines = ["### 事实", _render_claim_list(output.get("facts", [])), ""]
    lines.extend(["### 推断", _render_claim_list(output.get("inferences", [])), ""])
    lines.extend(["### 不确定性", _render_claim_list(output.get("uncertainties", [])), ""])
    lines.extend(["### 后续观察风险", _render_plain_list(output.get("risks", []))])
    return "\n".join(lines).rstrip()


def _render_committee(output: dict[str, Any]) -> str:
    lines = ["### 角色视角"]
    for role_view in output.get("role_views", []):
        lines.append(
            "- "
            f"[{role_view['claim_type']}] {role_view['role']}：{role_view['view']}"
            f"（来源：{role_view['source']}）"
        )
    lines.extend(["", "### 共识", _render_claim_list(output.get("consensus", []))])
    lines.extend(["", "### 分歧", _render_plain_list(output.get("disagreements", []))])
    lines.extend(["", "### 不确定性", _render_claim_list(output.get("uncertainties", []))])
    return "\n".join(lines).rstrip()


def _render_fact_check(output: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"- 已检查声明数量：{output['checked_claim_count']}",
            f"- 来源字段：{_included_status(output['has_sources'])}",
            (
                "- 事实、推断和不确定性标签："
                f"{_separation_status(output['separates_facts_inferences_uncertainties'])}"
            ),
        ]
    )


def _render_financial_safety(output: dict[str, Any]) -> str:
    blocked = output["blocked_phrases"]
    blocked_text = "未发现" if not blocked else "已发现：" + "、".join(blocked)
    return "\n".join(
        [
            f"- 检查结果：{_pass_status(output['passed'])}",
            f"- 免责声明状态：{_missing_status(output['missing_disclaimer'])}",
            f"- 禁止性投资建议表达：{blocked_text}",
            f"- 免责声明：{output['disclaimer']}",
        ]
    )


def _render_claim_list(items: list[dict[str, str]]) -> str:
    if not items:
        return "- 无"
    return "\n".join(
        f"- [{item['claim_type']}] {item['text']}（来源：{item['source']}）"
        for item in items
    )


def _render_plain_list(items: list[str]) -> str:
    if not items:
        return "- 无"
    return "\n".join(f"- {item}" for item in items)


def _pass_status(value: bool) -> str:
    return "通过" if value else "未通过"


def _included_status(value: bool) -> str:
    return "已包含" if value else "存在缺口"


def _separation_status(value: bool) -> str:
    return "已区分" if value else "未区分"


def _missing_status(value: bool) -> str:
    return "缺失" if value else "已包含"
