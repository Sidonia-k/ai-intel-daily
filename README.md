# ai-intel-daily

`ai-intel-daily` is a local-first project for generating daily AI intelligence reports.

Stage 4 adds a first AI daily report flow that reads configurable RSS/Atom
sources, deduplicates entries, and writes a Markdown report:

- AI industry changes worth watching
- AI-related stock market research notes

This project does not use API keys, does not automate schedules, does not use
agents, and does not provide investment advice.

## Features

- Generate a Markdown AI daily report from RSS/Atom sources in `config/ai_sources.yaml`.
- Continue when one RSS source fails.
- Deduplicate collected items by URL, then normalized title.
- Generate a "暂无有效数据" report when no valid items are collected.
- Keep report output folders under `data/reports/`.
- Include clear financial safety disclaimers in the stock research report.
- Provide a pytest suite that does not request real networks.

## Local Setup

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

This project uses a `src/` layout. Set `PYTHONPATH=src` when running commands locally.

## Run Locally

PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main
```

macOS / Linux:

```bash
PYTHONPATH=src python -m ai_intel_daily.main
```

To generate only the AI daily report:

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main --report ai
```

To generate reports for a specific date:

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main --report ai --date 2026-05-22
```

macOS / Linux:

```bash
PYTHONPATH=src python -m ai_intel_daily.main --report ai --date 2026-05-22
```

Generated reports are written to:

```text
data/reports/ai/
data/reports/stocks/
```

## Test Locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

PowerShell:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

macOS / Linux:

```bash
PYTHONPATH=src python -m pytest -q
```

## Recommended Git / GitHub Workflow

Do not develop directly on the default primary branch `main` or `master`. For each stage, create a separate feature branch.

Recommended flow:

1. Confirm the stage goal.
2. Update the default primary branch.
3. Create a feature branch for the stage.
4. Make small, easy-to-review changes.
5. Run local tests.
6. Commit the changes.
7. Push the branch to GitHub.
8. Open a Pull Request.
9. Merge only after review and CI pass.

Example:

```bash
git switch main
git pull
git switch -c stage2-github-workflow
PYTHONPATH=src python -m pytest -q
git add README.md
git commit -m "docs: update project workflow"
git push -u origin stage2-github-workflow
```

If the repository uses `master` as the default primary branch, replace `main` with `master`.

More details:

- `docs/git_workflow.md`
- `docs/github_actions.md`
- `docs/secrets.md`

## GitHub Actions

This project includes a CI workflow at `.github/workflows/ci.yml`.

The workflow runs on:

- `push`
- `pull_request`

It uses Python 3.11, installs dependencies from `requirements.txt`, sets `PYTHONPATH=src`, and runs:

```bash
python -m pytest -q
```

Current CI only runs tests. It does not connect to real APIs and does not create daily scheduled reports.

## Current Limits

- RSS/Atom only for the AI daily report; no HTML collectors yet.
- No paper, social media, market, earnings, or brokerage APIs.
- No complex agent or multi-agent system.
- No n8n workflow, cron job, daily report scheduler, or real automation against external services.
- No database, vector store, cache service, or external storage.
- No buy, sell, or hold recommendations.
- No API keys, passwords, tokens, or real credentials in code.
- No email, Slack, Feishu, Notion, or other distribution integration.
- No frontend, backend service, or deployment setup.
