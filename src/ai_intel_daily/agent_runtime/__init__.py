"""Stage 7D lightweight agent runtime adapters."""

from ai_intel_daily.agent_runtime.deepseek_runtime import run_deepseek_agent_runtime
from ai_intel_daily.agent_runtime.mock_runtime import run_mock_agent_runtime
from ai_intel_daily.agent_runtime.runtime_types import AgentRuntimeResult


__all__ = [
    "AgentRuntimeResult",
    "run_deepseek_agent_runtime",
    "run_mock_agent_runtime",
]
