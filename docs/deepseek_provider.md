# DeepSeek Provider (Stage 7C)

## Goal

Stage 7C adds a small, local DeepSeek provider experiment for the LLM layer. DeepSeek is a replaceable provider, not a project-wide dependency. The default provider remains `mock`, so normal tests and CI do not call the real DeepSeek API.

This stage does not add OpenAI Agents SDK, LangGraph, real financial APIs, databases, vector stores, schedulers, or automated workflows.

## Environment Variables

`.env.example` is only a configuration template. A real `.env` file must not be committed.

This project does not currently include `python-dotenv` and does not automatically load `.env` files. In Stage 7C, configuration is read from system environment variables.

PowerShell example:

```powershell
$env:DEEPSEEK_API_KEY="your-local-key"
$env:LLM_PROVIDER="deepseek"
$env:LLM_MODEL="deepseek-v4-flash"
$env:LLM_BASE_URL="https://api.deepseek.com"
```

Future stages can add a separate configuration-loading enhancement, but Stage 7C intentionally does not add `python-dotenv` or any new dependency.

## Manual Smoke Test

Run this only when you intentionally want to make a small real DeepSeek API call:

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.llm.deepseek_smoke
```

The smoke test sends a tiny prompt and prints the model response. It uses `thinking: {"type": "disabled"}` by default because Stage 7C only checks connectivity.

If `DEEPSEEK_API_KEY` is missing, the smoke test prints a setup hint and exits without calling the API.

## Switching Back To Mock

Use the mock provider for normal local development, pytest, and CI:

```powershell
$env:LLM_PROVIDER="mock"
```

You can also remove the DeepSeek-related environment variable overrides from your shell session.

## Safety

- Do not commit `.env`.
- Do not paste API keys into README, docs, tests, code, issues, pull requests, or logs.
- Do not print `DEEPSEEK_API_KEY`, `Authorization`, or Bearer tokens.
- Default pytest and GitHub Actions must stay offline and must not call the real DeepSeek API.

## Cost Control

- Use small prompts.
- Keep `max_tokens` small; the Stage 7C DeepSeek client defaults to `300`.
- Do not default to batch daily-report generation with a real provider.
- Do not enable thinking mode by default.

## Financial Safety

DeepSeek can only assist text generation. Stock-related reports still must pass the financial safety check and remain research assistance only. They must not provide deterministic buy, sell, hold, overweight, target-price, or guaranteed-return recommendations, and they do not constitute investment advice.
