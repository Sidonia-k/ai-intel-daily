"""A deterministic local model client used for tests and Stage 7 design."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MockLLMResponse:
    """Local response shape matching the minimum future client contract."""

    provider: str
    model: str
    text: str


class MockLLMClient:
    """Fake LLM client that never performs network or credential access."""

    def __init__(self, model: str = "mock-model") -> None:
        self.model = model
        self.provider = "mock"

    def complete(self, prompt: str, *, system: str = "") -> MockLLMResponse:
        """Return a deterministic local response for a prompt."""
        clean_prompt = " ".join(prompt.split())
        clean_system = " ".join(system.split())
        parts = ["[mock response]"]
        if clean_system:
            parts.append(f"system={clean_system[:80]}")
        if clean_prompt:
            parts.append(f"prompt={clean_prompt[:160]}")
        return MockLLMResponse(
            provider=self.provider,
            model=self.model,
            text=" | ".join(parts),
        )
