# DeepSeek Agent Runtime (Stage 7D)

## Goal

Stage 7D connects the existing local multi-agent architecture to the Stage 7C DeepSeek provider in one small manual smoke path. The goal is to generate a minimal Markdown daily draft with DeepSeek while keeping default development, pytest, and GitHub Actions fully offline.

This stage does not connect to real financial APIs, does not use the OpenAI API, and does not import `openai-agents`.

## Stage 7C vs Stage 7D

- Stage 7C validates basic DeepSeek provider connectivity.
- Stage 7D uses DeepSeek to run a minimal agent workflow smoke with local mock news and a local mock market snapshot.

DeepSeek is the only real LLM provider used in this stage. The default provider remains `mock` so normal runs do not call a real model.

## Manual Environment

Set environment variables in PowerShell before running the manual smoke:

```powershell
$env:DEEPSEEK_API_KEY="你的 key"
$env:LLM_PROVIDER="deepseek"
```

Do not commit real keys to code, tests, docs, `.env`, issues, pull requests, or logs.

## Manual Smoke

Run this only when you intentionally want to call the real DeepSeek API. It may incur cost.

```powershell
$env:PYTHONPATH="src"
python scripts/deepseek_agent_runtime_smoke.py
```

The script writes a Markdown draft under:

```text
data/reports/agent_runtime/
```

If `DEEPSEEK_API_KEY` is missing, the script prints a setup hint and exits without calling the API.

## Test And Safety Contract

普通 `pytest` 不会调用真实 DeepSeek API，也不需要 `DEEPSEEK_API_KEY`。DeepSeek runtime 的真实调用路径只由手动 smoke 脚本触发。

股票相关内容仍然只用于研究辅助，不构成投资建议，不提供买入、卖出或持有建议，也不承诺收益。输出必须经过本地 financial safety check。

Future Stage 8 can connect this runtime shape to LangGraph while keeping the same default-mock and manual-real-provider safety boundary.
