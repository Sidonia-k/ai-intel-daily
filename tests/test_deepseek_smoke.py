import importlib
import socket


def test_importing_deepseek_smoke_does_not_access_network(monkeypatch):
    def fail_socket(*args, **kwargs):
        raise AssertionError("importing deepseek_smoke must not access the network")

    monkeypatch.setattr(socket, "socket", fail_socket)

    module = importlib.import_module("ai_intel_daily.llm.deepseek_smoke")

    assert hasattr(module, "main")


def test_deepseek_smoke_missing_key_prints_hint_without_network(monkeypatch, capsys):
    from ai_intel_daily.llm import deepseek_smoke

    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    exit_code = deepseek_smoke.main()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "DEEPSEEK_API_KEY is not set" in captured.out
    assert "Bearer" not in captured.out


def test_deepseek_smoke_module_name_avoids_pytest_default_test_suffix():
    from ai_intel_daily.llm import deepseek_smoke

    assert deepseek_smoke.__file__.endswith("deepseek_smoke.py")
    assert not deepseek_smoke.__file__.endswith("_test.py")
