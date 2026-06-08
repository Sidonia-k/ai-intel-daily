import pytest

from ai_intel_daily.llm.client_factory import create_llm_client
from ai_intel_daily.llm.deepseek_client import DeepSeekClient
from ai_intel_daily.llm.mock_client import MockLLMClient


def test_factory_defaults_to_mock(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("LLM_BASE_URL", raising=False)

    client = create_llm_client()

    assert isinstance(client, MockLLMClient)


def test_factory_returns_mock_for_explicit_mock(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")

    client = create_llm_client()

    assert isinstance(client, MockLLMClient)


def test_factory_returns_deepseek(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "deepseek")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-deepseek-key-123456")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("LLM_BASE_URL", raising=False)

    client = create_llm_client()

    assert isinstance(client, DeepSeekClient)
    assert client.model == "deepseek-v4-flash"
    assert client.base_url == "https://api.deepseek.com"


def test_factory_rejects_unknown_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "unknown")

    with pytest.raises(ValueError, match="Unsupported LLM_PROVIDER"):
        create_llm_client()
