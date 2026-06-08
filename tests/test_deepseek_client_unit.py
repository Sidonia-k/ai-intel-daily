import json
import re
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError

import pytest

from ai_intel_daily.llm import deepseek_client
from ai_intel_daily.llm.deepseek_client import (
    DEFAULT_DEEPSEEK_MAX_TOKENS,
    DeepSeekClient,
    DeepSeekClientError,
)


ROOT = Path(__file__).resolve().parents[1]
FAKE_KEY = "test-deepseek-key-123456"


class FakeHTTPResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        if isinstance(self.payload, bytes):
            return self.payload
        return json.dumps(self.payload).encode("utf-8")


def _install_success_urlopen(monkeypatch, payload=None, captured=None):
    if payload is None:
        payload = {
            "choices": [
                {
                    "message": {"content": "ok"},
                    "finish_reason": "stop",
                }
            ]
        }

    def fake_urlopen(request, timeout):
        if captured is not None:
            captured["request"] = request
            captured["timeout"] = timeout
            captured["payload"] = json.loads(request.data.decode("utf-8"))
        return FakeHTTPResponse(payload)

    monkeypatch.setattr(deepseek_client, "urlopen", fake_urlopen)


def test_missing_deepseek_api_key_has_clear_error(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    with pytest.raises(DeepSeekClientError) as exc_info:
        DeepSeekClient()

    message = str(exc_info.value)
    assert "Missing DEEPSEEK_API_KEY" in message
    assert "Bearer" not in message


def test_default_deepseek_model_base_url_and_payload(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    captured = {}
    _install_success_urlopen(monkeypatch, captured=captured)

    client = DeepSeekClient()
    response = client.generate("hello")

    assert client.model == "deepseek-v4-flash"
    assert client.base_url == "https://api.deepseek.com"
    assert response.text == "ok"
    assert captured["payload"]["model"] == "deepseek-v4-flash"
    assert captured["payload"]["max_tokens"] == DEFAULT_DEEPSEEK_MAX_TOKENS
    assert captured["payload"]["thinking"] == {"type": "disabled"}
    assert captured["payload"]["messages"] == [{"role": "user", "content": "hello"}]
    assert captured["timeout"] == 30


def test_generate_allows_explicit_thinking_override(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    captured = {}
    _install_success_urlopen(monkeypatch, captured=captured)

    client = DeepSeekClient()
    client.generate("hello", thinking={"type": "enabled"})

    assert captured["payload"]["thinking"] == {"type": "enabled"}


def test_complete_builds_system_and_user_messages(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    captured = {}
    _install_success_urlopen(monkeypatch, captured=captured)

    client = DeepSeekClient()
    client.complete("user prompt", system="system prompt")

    assert captured["payload"]["messages"] == [
        {"role": "system", "content": "system prompt"},
        {"role": "user", "content": "user prompt"},
    ]


def test_complete_without_system_builds_only_user_message(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    captured = {}
    _install_success_urlopen(monkeypatch, captured=captured)

    client = DeepSeekClient()
    client.complete("user prompt")

    assert captured["payload"]["messages"] == [{"role": "user", "content": "user prompt"}]


def test_http_error_is_redacted(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)

    def fake_urlopen(request, timeout):
        raise HTTPError(
            request.full_url,
            401,
            f"Authorization Bearer {FAKE_KEY}",
            hdrs=None,
            fp=BytesIO(b"secret body"),
        )

    monkeypatch.setattr(deepseek_client, "urlopen", fake_urlopen)

    with pytest.raises(DeepSeekClientError) as exc_info:
        DeepSeekClient().generate("hello")

    _assert_no_secret_leak(str(exc_info.value))
    assert "status=401" in str(exc_info.value)


def test_url_error_is_redacted(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)

    def fake_urlopen(request, timeout):
        raise URLError(f"connection failed with {FAKE_KEY}")

    monkeypatch.setattr(deepseek_client, "urlopen", fake_urlopen)

    with pytest.raises(DeepSeekClientError) as exc_info:
        DeepSeekClient().generate("hello")

    _assert_no_secret_leak(str(exc_info.value))
    assert "connection error" in str(exc_info.value)


def test_invalid_json_error_is_redacted(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    _install_success_urlopen(monkeypatch, payload=b"{not-json")

    with pytest.raises(DeepSeekClientError) as exc_info:
        DeepSeekClient().generate("hello")

    _assert_no_secret_leak(str(exc_info.value))
    assert "invalid JSON" in str(exc_info.value)


def test_response_with_empty_choices_raises_clear_error(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    _install_success_urlopen(monkeypatch, payload={"choices": []})

    with pytest.raises(DeepSeekClientError, match="did not include any choices"):
        DeepSeekClient().generate("hello")


def test_response_missing_message_raises_clear_error(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    _install_success_urlopen(monkeypatch, payload={"choices": [{"finish_reason": "stop"}]})

    with pytest.raises(DeepSeekClientError, match="missing message"):
        DeepSeekClient().generate("hello")


def test_response_null_content_degrades_to_empty_text(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    _install_success_urlopen(
        monkeypatch,
        payload={"choices": [{"message": {"content": None}, "finish_reason": "stop"}]},
    )

    response = DeepSeekClient().generate("hello")

    assert response.text == ""
    assert response.finish_reason == "stop"


def test_response_non_stop_finish_reason_keeps_text(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    _install_success_urlopen(
        monkeypatch,
        payload={"choices": [{"message": {"content": "partial"}, "finish_reason": "length"}]},
    )

    response = DeepSeekClient().generate("hello")

    assert response.text == "partial"
    assert response.finish_reason == "length"


def test_response_non_stop_finish_reason_without_text_raises(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", FAKE_KEY)
    _install_success_urlopen(
        monkeypatch,
        payload={"choices": [{"message": {"content": ""}, "finish_reason": "length"}]},
    )

    with pytest.raises(DeepSeekClientError, match="finish_reason=length"):
        DeepSeekClient().generate("hello")


def test_deepseek_sources_do_not_contain_hardcoded_api_keys():
    paths = [
        ROOT / "src" / "ai_intel_daily" / "llm" / "deepseek_client.py",
        ROOT / "src" / "ai_intel_daily" / "llm" / "client_factory.py",
        ROOT / "src" / "ai_intel_daily" / "llm" / "deepseek_smoke.py",
        ROOT / ".env.example",
    ]
    secret_patterns = (
        re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
        re.compile(r"Bearer\s+[A-Za-z0-9._-]{8,}", re.IGNORECASE),
        re.compile(r"api_key\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE),
    )

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            for pattern in secret_patterns:
                assert not pattern.search(stripped)


def _assert_no_secret_leak(message):
    assert "Authorization" not in message
    assert "Bearer" not in message
    assert "DEEPSEEK_API_KEY" not in message
    assert FAKE_KEY not in message
