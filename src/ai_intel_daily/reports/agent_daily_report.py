"""Markdown rendering and writing for Stage 7B mock agent reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "data" / "reports"


def render_agent_daily_report(workflow_result: dict[str, Any]) -> str:
    """Render Markdown from a Stage 7B mock workflow result."""
    markdown = str(workflow_result.get("markdown", "")).strip()
    if markdown:
        return markdown + "\n"

    editor_step = _find_step(workflow_result, "Editor Agent")
    if editor_step:
        editor_markdown = str(editor_step.get("output", {}).get("markdown", "")).strip()
        if editor_markdown:
            return editor_markdown + "\n"

    raise ValueError("workflow_result does not contain Editor Agent markdown")


def write_agent_daily_report(
    workflow_result: dict[str, Any],
    output_dir: str | Path | None = None,
) -> Path:
    """Write the Stage 7B mock agent Markdown report to disk."""
    report_date = str(workflow_result["report_date"])
    reports_dir = Path(output_dir) if output_dir is not None else DEFAULT_REPORTS_DIR
    report_path = reports_dir / "agent" / f"{report_date}-agent-daily-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_agent_daily_report(workflow_result), encoding="utf-8")
    return report_path


def _find_step(workflow_result: dict[str, Any], agent_name: str) -> dict[str, Any] | None:
    for step in workflow_result.get("steps", []):
        if step.get("agent_name") == agent_name:
            return step
    return None
