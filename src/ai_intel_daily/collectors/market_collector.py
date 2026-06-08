"""Local placeholder market research data for AI stock reports."""

from __future__ import annotations

from datetime import date
from typing import Any


SECTOR_NAMES = [
    "AI 芯片",
    "云计算",
    "数据中心",
    "软件",
    "机器人",
    "AI 应用公司",
]

RISK_CATEGORIES = [
    "估值风险",
    "竞争风险",
    "监管风险",
    "供应链风险",
    "技术路线风险",
    "宏观利率风险",
]


def collect_market_research_snapshot(report_date: date | str) -> dict[str, Any]:
    """Return a local simulated AI stock research snapshot.

    This Stage 5 collector intentionally does not connect to real market,
    earnings, brokerage, or financial data APIs.
    """
    date_text = report_date.isoformat() if isinstance(report_date, date) else str(report_date)
    return {
        "date": date_text,
        "market_overview": [
            "当前阶段使用本地模拟数据，不代表真实市场情况。",
            "模拟观察：AI 产业链关注点集中在算力需求、云基础设施投入和企业应用落地。",
            "模拟观察：不同板块与 AI 主题的相关性需要结合收入结构、客户需求和资本开支继续验证。",
        ],
        "sectors": [
            {
                "name": "AI 芯片",
                "facts": [
                    "模拟事实：AI 芯片板块通常与训练和推理算力需求相关。",
                    "模拟事实：先进制程、封装能力和供应链交付节奏会影响研究判断。",
                ],
                "inference": "如果算力需求持续扩散，相关供应链值得继续观察；但产能、价格和客户集中度仍需要进一步验证。",
            },
            {
                "name": "云计算",
                "facts": [
                    "模拟事实：云计算公司可能通过 AI 基础设施、模型服务和开发者工具承接需求。",
                    "模拟事实：资本开支和利用率是观察云业务质量的重要变量。",
                ],
                "inference": "云资源需求与 AI 采用率存在关联，但当前信息不足以形成结论。",
            },
            {
                "name": "数据中心",
                "facts": [
                    "模拟事实：数据中心板块与电力、散热、机柜和网络连接能力相关。",
                    "模拟事实：AI 负载可能提高对高密度部署和能源效率的要求。",
                ],
                "inference": "数据中心扩张与 AI 需求风险和机会并存，需要进一步验证建设周期和成本压力。",
            },
            {
                "name": "软件",
                "facts": [
                    "模拟事实：软件公司可能将 AI 功能嵌入办公、开发、安全和业务流程产品。",
                    "模拟事实：客户付费意愿、留存率和毛利率是后续观察重点。",
                ],
                "inference": "AI 功能可能改善产品体验，但商业化节奏仍需要继续观察。",
            },
            {
                "name": "机器人",
                "facts": [
                    "模拟事实：机器人方向涉及传感器、控制系统、模型能力和制造成本。",
                    "模拟事实：商业落地通常受应用场景、可靠性和规模化生产约束。",
                ],
                "inference": "机器人应用具备长期研究价值，但当前信息不足以形成结论。",
            },
            {
                "name": "AI 应用公司",
                "facts": [
                    "模拟事实：AI 应用公司通常依赖场景数据、分发渠道和客户续费能力。",
                    "模拟事实：应用层竞争可能随模型能力普及而变化。",
                ],
                "inference": "应用公司需要进一步验证真实使用率、付费转化和差异化壁垒。",
            },
        ],
        "companies": [
            "模拟公司 A：AI 芯片与加速计算相关研究对象。",
            "模拟公司 B：云计算与 AI 基础设施相关研究对象。",
            "模拟公司 C：企业软件与 AI 应用相关研究对象。",
        ],
        "company_news": [
            "模拟事实：模拟公司 A 发布新一代 AI 加速产品路线图。",
            "模拟事实：模拟公司 B 提到数据中心资本开支是管理层关注事项。",
            "模拟事实：模拟公司 C 将 AI 功能列为产品升级方向。",
        ],
        "earnings_events": [
            "模拟事实：后续财报可关注 AI 相关收入披露口径。",
            "模拟事实：后续事件可关注资本开支、供应链交付和客户采用率表述。",
        ],
        "sentiment": [
            "模拟观察：市场情绪可能受 AI 需求叙事、估值水平和宏观利率变化共同影响。",
            "模拟观察：短期叙事与长期基本面之间可能存在偏离，仅供研究参考。",
        ],
        "risks": [
            {"name": "估值风险", "detail": "模拟风险：估值可能先于基本面反映乐观预期。"},
            {"name": "竞争风险", "detail": "模拟风险：模型、芯片、云服务和应用层竞争可能压缩利润空间。"},
            {"name": "监管风险", "detail": "模拟风险：数据、出口管制、版权和安全规则变化可能影响业务节奏。"},
            {"name": "供应链风险", "detail": "模拟风险：先进制程、封装、电力和设备供应可能影响交付能力。"},
            {"name": "技术路线风险", "detail": "模拟风险：模型架构、推理成本和硬件路线变化可能改变产业链价值分配。"},
            {"name": "宏观利率风险", "detail": "模拟风险：利率变化可能影响成长资产估值和企业资本开支计划。"},
        ],
        "indicators_to_watch": [
            "AI 相关收入占比和增速披露。",
            "数据中心资本开支、利用率和能源成本。",
            "芯片交付周期、供应链限制和客户集中度。",
            "软件产品 AI 功能使用率、续费率和付费转化。",
            "监管政策、出口限制和数据合规变化。",
            "利率环境、风险偏好和估值水平变化。",
        ],
    }
