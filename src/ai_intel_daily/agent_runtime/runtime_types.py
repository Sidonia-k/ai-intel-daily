"""Shared result types for Stage 7D agent runtimes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRuntimeResult:
    """Minimum output contract for manual and mock agent runtime runs."""

    provider: str
    model: str
    workflow_name: str
    final_markdown: str
    safety_passed: bool
    warnings: list[str]
    used_real_api: bool
