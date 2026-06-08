import re
from pathlib import Path

from ai_intel_daily.llm.mock_client import MockLLMClient
from ai_intel_daily.llm.provider_config import ProviderConfig, SUPPORTED_PROVIDERS


ROOT = Path(__file__).resolve().parents[1]


def test_provider_config_supports_planned_providers():
    expected = {"openai", "deepseek", "litellm", "local", "mock"}

    assert SUPPORTED_PROVIDERS == expected
    for provider in expected:
        config = ProviderConfig(provider=provider)
        assert config.provider == provider


def test_provider_config_defaults_to_mock():
    config = ProviderConfig()

    assert config.provider == "mock"
    assert config.model == ""
    assert config.base_url == ""
    assert config.api_key_env == ""


def test_provider_config_deepseek_defaults():
    config = ProviderConfig(provider="deepseek")

    assert config.provider == "deepseek"
    assert config.model == "deepseek-v4-flash"
    assert config.base_url == "https://api.deepseek.com"
    assert config.api_key_env == "DEEPSEEK_API_KEY"


def test_provider_config_stores_secret_env_name_not_secret_value():
    config = ProviderConfig(provider="openai", model="future-model")

    assert config.api_key_env == "OPENAI_API_KEY"
    assert config.uses_secret_env


def test_mock_client_returns_local_response_without_network(monkeypatch):
    import socket

    def fail_socket(*args, **kwargs):
        raise AssertionError("mock client must not access the network")

    monkeypatch.setattr(socket, "socket", fail_socket)

    client = MockLLMClient()
    response = client.complete("Summarize local Stage 7 design.", system="No API calls.")

    assert response.provider == "mock"
    assert response.model == "mock-model"
    assert "[mock response]" in response.text
    assert "Stage 7" in response.text


def test_mock_client_source_does_not_import_network_libraries():
    source = (ROOT / "src" / "ai_intel_daily" / "llm" / "mock_client.py").read_text(encoding="utf-8")

    banned_imports = ("import requests", "import urllib", "import http.client", "import socket")
    for banned_import in banned_imports:
        assert banned_import not in source


def test_stage7_files_do_not_contain_hardcoded_api_keys():
    paths = [
        ROOT / ".env.example",
        ROOT / "src" / "ai_intel_daily" / "agents" / "agent_specs.py",
        ROOT / "src" / "ai_intel_daily" / "agents" / "workflow_design.py",
        ROOT / "src" / "ai_intel_daily" / "agents" / "guardrails.py",
        ROOT / "src" / "ai_intel_daily" / "llm" / "provider_config.py",
        ROOT / "src" / "ai_intel_daily" / "llm" / "mock_client.py",
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
