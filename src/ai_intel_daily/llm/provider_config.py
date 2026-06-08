"""Provider configuration for future model-client adapters."""

from __future__ import annotations

from dataclasses import dataclass


SUPPORTED_PROVIDERS: frozenset[str] = frozenset(
    {
        "openai",
        "deepseek",
        "litellm",
        "local",
        "mock",
    }
)


DEFAULT_API_KEY_ENV_BY_PROVIDER: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "litellm": "LITELLM_API_KEY",
    "local": "",
    "mock": "",
}


DEFAULT_MODEL_BY_PROVIDER: dict[str, str] = {
    "openai": "",
    "deepseek": "deepseek-v4-flash",
    "litellm": "",
    "local": "",
    "mock": "",
}


DEFAULT_BASE_URL_BY_PROVIDER: dict[str, str] = {
    "openai": "",
    "deepseek": "https://api.deepseek.com",
    "litellm": "",
    "local": "",
    "mock": "",
}


@dataclass(frozen=True)
class ProviderConfig:
    """Configuration shape for future model providers.

    The config stores the environment variable name for a secret, not the secret
    value itself.
    """

    provider: str = "mock"
    model: str = ""
    base_url: str = ""
    api_key_env: str = ""

    def __post_init__(self) -> None:
        normalized_provider = self.provider.strip().lower()
        if normalized_provider not in SUPPORTED_PROVIDERS:
            supported = ", ".join(sorted(SUPPORTED_PROVIDERS))
            raise ValueError(f"Unsupported provider: {self.provider}. Supported providers: {supported}")
        object.__setattr__(self, "provider", normalized_provider)
        if not self.api_key_env:
            object.__setattr__(
                self,
                "api_key_env",
                DEFAULT_API_KEY_ENV_BY_PROVIDER[normalized_provider],
            )
        if not self.model:
            object.__setattr__(
                self,
                "model",
                DEFAULT_MODEL_BY_PROVIDER[normalized_provider],
            )
        if not self.base_url:
            object.__setattr__(
                self,
                "base_url",
                DEFAULT_BASE_URL_BY_PROVIDER[normalized_provider],
            )

    @property
    def uses_secret_env(self) -> bool:
        """Return whether this provider expects an API key environment variable."""
        return bool(self.api_key_env)
