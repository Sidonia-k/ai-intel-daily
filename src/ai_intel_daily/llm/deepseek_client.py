"""Small DeepSeek chat-completions client for Stage 7C smoke testing."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ai_intel_daily.llm.provider_config import ProviderConfig


DEFAULT_DEEPSEEK_MAX_TOKENS = 300
DEFAULT_DEEPSEEK_TIMEOUT_SECONDS = 30
DEFAULT_THINKING_DISABLED: dict[str, str] = {"type": "disabled"}


class DeepSeekClientError(RuntimeError):
    """Raised when the DeepSeek client cannot safely complete a request."""


@dataclass(frozen=True)
class DeepSeekLLMResponse:
    """Minimum response shape shared with the Stage 7 mock client contract."""

    provider: str
    model: str
    text: str
    finish_reason: str = ""


class DeepSeekClient:
    """Minimal DeepSeek provider using the OpenAI-compatible chat API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        max_tokens: int = DEFAULT_DEEPSEEK_MAX_TOKENS,
        timeout: int = DEFAULT_DEEPSEEK_TIMEOUT_SECONDS,
    ) -> None:
        config = ProviderConfig(provider="deepseek")
        self.provider = "deepseek"
        self.model = model or config.model
        self.base_url = (base_url or config.base_url).rstrip("/")
        self.max_tokens = max_tokens
        self.timeout = timeout
        self._api_key = api_key if api_key is not None else os.environ.get(config.api_key_env, "")
        if not self._api_key:
            raise DeepSeekClientError(
                "Missing DEEPSEEK_API_KEY. Set it as a local environment variable before "
                "using the DeepSeek provider."
            )

    def generate(
        self,
        prompt_or_messages: str | list[dict[str, Any]],
        *,
        thinking: dict[str, Any] | None = None,
    ) -> DeepSeekLLMResponse:
        """Generate a response from a prompt string or chat messages."""
        messages = self._normalize_messages(prompt_or_messages)
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "stream": False,
            "thinking": thinking if thinking is not None else DEFAULT_THINKING_DISABLED,
        }
        data = self._post_json(payload)
        return self._parse_response(data)

    def complete(self, prompt: str, *, system: str = "") -> DeepSeekLLMResponse:
        """Complete a prompt while matching the current mock client's method shape."""
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self.generate(messages)

    def _post_json(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                response_body = response.read().decode("utf-8")
        except HTTPError as exc:
            raise DeepSeekClientError(
                f"DeepSeek API HTTP error: status={exc.code}, reason={_safe_reason(exc.reason, self._api_key)}"
            ) from exc
        except URLError as exc:
            raise DeepSeekClientError(
                f"DeepSeek API connection error: reason={_safe_reason(exc.reason, self._api_key)}"
            ) from exc

        try:
            data = json.loads(response_body)
        except json.JSONDecodeError as exc:
            raise DeepSeekClientError("DeepSeek API returned invalid JSON.") from exc
        if not isinstance(data, dict):
            raise DeepSeekClientError("DeepSeek API returned an unexpected JSON shape.")
        return data

    def _parse_response(self, data: dict[str, Any]) -> DeepSeekLLMResponse:
        choices = data.get("choices")
        if not choices:
            raise DeepSeekClientError("DeepSeek API response did not include any choices.")
        if not isinstance(choices, list):
            raise DeepSeekClientError("DeepSeek API response choices must be a list.")

        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            raise DeepSeekClientError("DeepSeek API response choice has an unexpected shape.")
        message = first_choice.get("message")
        if not isinstance(message, dict):
            raise DeepSeekClientError("DeepSeek API response choice is missing message content.")

        content = message.get("content")
        text = "" if content is None else str(content)
        finish_reason = str(first_choice.get("finish_reason") or "")
        if finish_reason != "stop" and not text:
            raise DeepSeekClientError(
                f"DeepSeek API response ended with finish_reason={finish_reason or 'unknown'} "
                "and no content."
            )
        return DeepSeekLLMResponse(
            provider=self.provider,
            model=self.model,
            text=text,
            finish_reason=finish_reason,
        )

    def _normalize_messages(self, prompt_or_messages: str | list[dict[str, Any]]) -> list[dict[str, Any]]:
        if isinstance(prompt_or_messages, str):
            return [{"role": "user", "content": prompt_or_messages}]
        if not isinstance(prompt_or_messages, list):
            raise TypeError("DeepSeek prompt must be a string or a list of chat messages.")
        return prompt_or_messages


def _safe_reason(reason: object, api_key: str = "") -> str:
    text = str(reason)
    for marker in ("Authorization", "Bearer", "DEEPSEEK_API_KEY"):
        if marker.lower() in text.lower():
            return "[redacted]"
    if api_key and api_key in text:
        return text.replace(api_key, "[redacted]")[:120]
    return text[:120]
