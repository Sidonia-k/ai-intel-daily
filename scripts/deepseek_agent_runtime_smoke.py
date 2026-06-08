"""Manual Stage 7D DeepSeek agent runtime smoke.

This script calls the real DeepSeek API when DEEPSEEK_API_KEY is set, which may
incur cost. It is intentionally not named test_*.py and is not part of pytest.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import os
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
REPORTS_DIR = PROJECT_ROOT / "data" / "reports" / "agent_runtime"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ai_intel_daily.agent_runtime.deepseek_runtime import run_deepseek_agent_runtime


def main() -> int:
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print(
            "DEEPSEEK_API_KEY is not set. This manual smoke calls the real "
            "DeepSeek API and may incur cost, so set the key locally before running it."
        )
        return 1

    provider = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if provider and provider != "deepseek":
        print(
            f"LLM_PROVIDER is {provider!r}. This smoke uses DeepSeek explicitly; "
            "set LLM_PROVIDER=deepseek or unset it to avoid confusion."
        )
        return 1

    result = run_deepseek_agent_runtime()
    if not result.used_real_api:
        print("\n".join(result.warnings) or "DeepSeek agent runtime smoke did not run.")
        return 1
    if not result.safety_passed:
        print("DeepSeek agent runtime output failed the financial safety check.")
        for warning in result.warnings:
            print(f"- {warning}")
        return 1

    report_date = date.today().isoformat()
    report_path = REPORTS_DIR / f"{report_date}-deepseek-agent-runtime-smoke.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(result.final_markdown, encoding="utf-8")
    print(f"Wrote DeepSeek agent runtime smoke report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
