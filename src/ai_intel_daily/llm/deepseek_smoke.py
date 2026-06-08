"""Manual DeepSeek provider smoke test for Stage 7C."""

from __future__ import annotations

import os

from ai_intel_daily.llm.deepseek_client import DeepSeekClient, DeepSeekClientError


def main() -> int:
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("DEEPSEEK_API_KEY is not set. Set it as a local environment variable first.")
        return 1

    try:
        client = DeepSeekClient(
            model=os.environ.get("LLM_MODEL") or None,
            base_url=os.environ.get("LLM_BASE_URL") or None,
        )
        response = client.generate("用一句中文回复：DeepSeek provider is working.")
    except DeepSeekClientError as exc:
        print(f"DeepSeek smoke test failed: {exc}")
        return 1

    print(response.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
