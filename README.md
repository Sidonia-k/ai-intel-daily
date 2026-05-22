# ai-intel-daily

`ai-intel-daily` is a local-first project for generating daily AI intelligence reports.

Stage 0 creates the project skeleton and generates two Markdown reports with fixed fake data:

- AI industry changes worth watching
- AI-related stock market research notes

This stage does not connect to real APIs, does not automate schedules, does not use agents, and does not provide investment advice.

## Stage 0 Features

- Generate local Markdown reports from templates.
- Keep report output folders under `data/reports/`.
- Include clear financial safety disclaimers in the stock research report.
- Provide a small pytest suite for the basic project contract.

## Run

PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main
```

To generate reports for a specific date:

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main --date 2026-05-22
```

Generated reports are written to:

```text
data/reports/ai/
data/reports/stocks/
```

## Test

Install dependencies:

```powershell
pip install -r requirements.txt
```

PowerShell:

```powershell
$env:PYTHONPATH="src"
pytest
```

## Current Limits

- No real news, paper, social media, market, earnings, or brokerage APIs.
- No complex agent or multi-agent system.
- No n8n workflow, cron job, GitHub Actions workflow, or scheduler.
- No database, vector store, cache service, or external storage.
- No buy, sell, or hold recommendations.
- No API keys, passwords, tokens, or real credentials in code.
- No email, Slack, Feishu, Notion, or other distribution integration.
- No frontend, backend service, or deployment setup.
