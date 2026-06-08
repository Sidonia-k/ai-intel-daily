"""Factory for Stage 7 model provider clients."""

from __future__ import annotations

import os

from ai_intel_daily.llm.deepseek_client import DeepSeekClient
from ai_intel_daily.llm.mock_client import MockLLMClient
from ai_intel_daily.llm.provider_config import SUPPORTED_PROVIDERS, ProviderConfig


def create_llm_client() -> MockLLMClient | DeepSeekClient:
    """Create a configured LLM client from local environment variables."""
    provider = os.environ.get("LLM_PROVIDER", "mock").strip().lower() or "mock"
    if provider not in SUPPORTED_PROVIDERS:
        supported = ", ".join(sorted(SUPPORTED_PROVIDERS))
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}. Supported providers: {supported}")

    config = ProviderConfig(
        provider=provider,
        model=os.environ.get("LLM_MODEL", ""),
        base_url=os.environ.get("LLM_BASE_URL", ""),
    )
    if config.provider == "mock":
        return MockLLMClient(model=config.model or "mock-model")
    if config.provider == "deepseek":
        return DeepSeekClient(model=config.model, base_url=config.base_url)

    raise ValueError(
        f"LLM_PROVIDER={config.provider} is recognized but not implemented in Stage 7C."
    )
