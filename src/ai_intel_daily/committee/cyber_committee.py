"""Local rule-based cyber investment committee analysis."""

from __future__ import annotations

from typing import Any

from ai_intel_daily.committee.roles import CYBER_ROLES


COMMITTEE_FINANCIAL_SAFETY_DISCLAIMER = (
    "本模块仅用于研究辅助，不构成投资建议，不提供买入、卖出或持有建议，"
    "不承诺收益；所有内容均基于本地模拟数据。"
)


def build_cyber_committee_analysis(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Build a local structured committee analysis from simulated snapshot data."""
    facts_basis = _facts_basis(snapshot)
    role_views = [_build_role_view(role, snapshot) for role in CYBER_ROLES]
    return {
        "facts_basis": facts_basis,
        "role_views": role_views,
        "committee_consensus": _committee_consensus(snapshot),
        "major_disagreements": _major_disagreements(snapshot),
        "uncertainties": _uncertainties(snapshot),
        "follow_up_indicators": _as_strings(snapshot.get("indicators_to_watch", [])),
        "financial_safety_disclaimer": COMMITTEE_FINANCIAL_SAFETY_DISCLAIMER,
    }


def _build_role_view(role: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": role["name"],
        "focus": role["focus"],
        "key_questions": role["key_questions"],
        "local_observations": _role_observations(str(role["name"]), snapshot),
    }


def _role_observations(role_name: str, snapshot: dict[str, Any]) -> list[str]:
    sectors = _sector_names(snapshot)
    risks = _risk_names(snapshot)
    if role_name == "Cyber Buffett":
        return [
            "重点观察 AI 需求是否能持续沉淀为收入质量，而不是只停留在主题关注。",
            "结合板块覆盖范围评估长期业务韧性：" + _join_or_empty(sectors),
        ]
    if role_name == "Cyber Munger":
        return [
            "优先列出可能推翻研究假设的反例，包括需求放缓、成本上升和客户集中。",
            "当前风险清单提示需要避免单一乐观叙事：" + _join_or_empty(risks),
        ]
    if role_name == "Cyber Graham":
        return [
            "当前资料仍是模拟事实集合，适合做证据清单，不适合做确定性结论。",
            "需要继续区分事实基础、合理推断和不确定性。",
        ]
    if role_name == "Cyber Damodaran":
        return [
            "估值相关研究应先拆分收入、利润率、资本开支和资本成本变量。",
            "现阶段没有真实财务数字，因此只能记录敏感变量，不能给出估值结论。",
        ]
    if role_name == "Cyber Wood":
        return [
            "技术扩散视角关注算力、云、软件和应用层之间的长期联动。",
            "需要验证 AI 功能是否产生真实采用率和付费转化。",
        ]
    if role_name == "Cyber Lynch":
        return [
            "从产品和客户线索出发，关注 AI 功能是否易理解、可复用、可续费。",
            "公司新闻可作为后续追踪入口，但不能替代真实客户数据。",
        ]
    if role_name == "Cyber Taleb":
        return [
            "尾部风险集中在供应链、监管、能源、利率和技术路线变化。",
            "需要为需求波动和交付延迟保留不确定性空间。",
        ]
    if role_name == "Cyber Huang":
        return [
            "加速计算视角关注芯片、封装、网络、数据中心和软件生态协同。",
            "供给约束和部署节奏是后续验证重点。",
        ]
    return ["暂无有效数据。"]


def _facts_basis(snapshot: dict[str, Any]) -> list[str]:
    facts: list[str] = []
    facts.extend(_as_strings(snapshot.get("market_overview", []))[:2])
    facts.extend(_as_strings(snapshot.get("company_news", []))[:3])
    facts.extend(_as_strings(snapshot.get("earnings_events", []))[:2])
    for sector in snapshot.get("sectors", []):
        if not isinstance(sector, dict):
            continue
        name = str(sector.get("name", "")).strip()
        sector_facts = _as_strings(sector.get("facts", []))
        if name and sector_facts:
            facts.append(f"{name}: {sector_facts[0]}")
    return facts


def _committee_consensus(snapshot: dict[str, Any]) -> list[str]:
    sectors = _sector_names(snapshot)
    return [
        "AI 相关研究应先围绕可验证事实、业务变量和风险清单展开。",
        "算力、云基础设施、数据中心、软件和应用层需要作为相互关联的产业链观察对象。",
        "当前阶段只能形成研究问题和观察框架，不能形成交易决策。",
        "已覆盖板块：" + _join_or_empty(sectors),
    ]


def _major_disagreements(snapshot: dict[str, Any]) -> list[str]:
    return [
        "长期创新扩散视角会更关注可选性，价值纪律视角会更关注证据充分性。",
        "成长情景更重视技术采用曲线，风险视角更重视供应链、监管和利率压力。",
        "不同角色对资本开支的解读不同：它既可能支持长期能力，也可能带来回报压力。",
    ]


def _uncertainties(snapshot: dict[str, Any]) -> list[str]:
    values = [
        "现有数据为本地模拟数据，不包含真实行情、真实财报或管理层原文。",
        "AI 相关收入占比、客户采用率、续费率和资本开支回报仍需进一步验证。",
    ]
    values.extend(_as_strings(snapshot.get("sentiment", []))[:2])
    return values


def _sector_names(snapshot: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for sector in snapshot.get("sectors", []):
        if isinstance(sector, dict):
            name = str(sector.get("name", "")).strip()
            if name:
                names.append(name)
    return names


def _risk_names(snapshot: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for risk in snapshot.get("risks", []):
        if isinstance(risk, dict):
            name = str(risk.get("name", "")).strip()
            if name:
                names.append(name)
        elif str(risk).strip():
            names.append(str(risk).strip())
    return names


def _join_or_empty(values: list[str]) -> str:
    return "、".join(values) if values else "暂无有效数据"


def _as_strings(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    return [str(item).strip() for item in items if str(item).strip()]
