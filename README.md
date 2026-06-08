# ai-intel-daily

`ai-intel-daily` 是一个本地优先的项目，用于生成 AI 情报日报。

阶段 4 增加了第一版 AI 日报流程：读取可配置的 RSS/Atom 来源，去重条目，并写出 Markdown 报告。报告主要覆盖：

- 值得关注的 AI 行业变化
- AI 相关股票市场研究笔记

本项目不使用真实 API key，不创建自动化日程，不运行真实 agent，也不提供投资建议。

## 功能

- 从 `config/ai_sources.yaml` 中配置的 RSS/Atom 来源生成 Markdown AI 日报。
- 当单个 RSS 来源失败时继续运行。
- 按 URL 和规范化标题对采集条目去重。
- 当没有有效条目时，生成“暂无有效数据”报告。
- 将报告输出目录保持在 `data/reports/` 下。
- 在股票研究报告中包含清晰的金融安全免责声明。
- 提供不会请求真实网络的 pytest 测试套件。

## 阶段 7：多 Agent 架构

阶段 7 增加了面向未来多 Agent 日报架构的设计文档和轻量代码骨架。当前实现只包含文档、静态 agent specs、workflow 设计、guardrails 定义、模型供应商配置，以及确定性的 mock 模型客户端。

这个骨架的目标是让后续阶段可以接入真实 Agents SDK、OpenAI、DeepSeek、LiteLLM 或本地模型适配器，而不是把某一个供应商写死在报告逻辑中。本阶段不导入 `openai-agents`，不调用 OpenAI 或 DeepSeek，也不连接真实市场数据 API。

股票相关报告内容仍然只用于研究辅助，不构成投资建议，也不提供买入、卖出或持有建议。

## 阶段 7B：本地 mock 多 Agent 工作流模拟运行

阶段 7B 增加了一个完全本地、确定性的 mock 多 Agent workflow，用于模拟：

1. News Agent
2. Market Agent
3. Cyber Committee Agent
4. Fact Check Agent
5. Financial Safety Agent
6. Editor Agent

当前阶段仍然不接真实 OpenAI API、DeepSeek API 或财经 API，也不导入 `openai-agents`。workflow 只使用本地假数据、现有 agent specs、确定性的 mock client 和本地 guardrails。

报告输出默认使用中文内容；保留英文 agent 名称仅用于和 `agent_specs.py` 中的结构化名称保持一致。

生成 mock agent 日报：

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main --mock-agent
```

输出路径：

```text
data/reports/agent/YYYY-MM-DD-agent-daily-report.md
```

股票和市场相关内容仍然只作为研究辅助，不构成投资建议，不提供买入、卖出或持有建议，也不承诺收益。

后续规划：

- 阶段 7C 已加入 DeepSeek provider 小范围连通性试验。
- 阶段 7D 加入 DeepSeek Agent Runtime 手动 smoke。
- 原计划阶段 8 保留给 LangGraph。

## 阶段 7C：DeepSeek provider 本地小范围试验

阶段 7C 增加了一个可替换的 DeepSeek LLM provider，用于本地小范围连通性试验。默认 provider 仍然是 `mock`，普通 pytest 和 GitHub Actions 默认不得调用真实 DeepSeek API。

真实 DeepSeek 调用需要用户在本地系统环境变量中设置 `DEEPSEEK_API_KEY`。`.env.example` 只是配置模板，真实 `.env` 不应提交。当前项目没有引入 `python-dotenv`，也没有实现 `.env` 自动加载器，所以把 key 写进 `.env` 并不会被 Python 自动读取。

PowerShell 示例：

```powershell
$env:DEEPSEEK_API_KEY="your-local-key"
$env:LLM_PROVIDER="deepseek"
$env:LLM_MODEL="deepseek-v4-flash"
$env:LLM_BASE_URL="https://api.deepseek.com"
```

手动 smoke test：

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.llm.deepseek_smoke
```

DeepSeek smoke test 默认使用 `thinking: {"type": "disabled"}`，因为阶段 7C 只验证连通性。切回 mock：

```powershell
$env:LLM_PROVIDER="mock"
```

后续可以单独做配置加载增强；本阶段不引入 `python-dotenv`，不新增依赖。

## 阶段 7D：DeepSeek Agent Runtime 小范围接入

阶段 7D 增加一个轻量 agent runtime 层，把现有本地多 Agent 架构和 Stage 7C DeepSeek provider 串起来。当前默认仍然是 `mock`，普通运行、pytest 和 GitHub Actions 不调用真实 API。

DeepSeek 是本阶段唯一真实 LLM provider。手动运行 DeepSeek runtime smoke 前，需要在本地设置 `DEEPSEEK_API_KEY`，并建议设置 `LLM_PROVIDER=deepseek`：

```powershell
$env:DEEPSEEK_API_KEY="your-local-key"
$env:LLM_PROVIDER="deepseek"
$env:PYTHONPATH="src"
python scripts/deepseek_agent_runtime_smoke.py
```

这个 smoke 会调用真实 DeepSeek API，可能产生费用；输出写入：

```text
data/reports/agent_runtime/
```

本阶段不使用 OpenAI API，不导入 `openai-agents`，也不接真实财经 API。股票相关内容仍然只作为研究辅助，不构成投资建议，不提供买入、卖出或持有建议，也不承诺收益。

## 本地设置

安装依赖：

```bash
python -m pip install -r requirements.txt
```

本项目使用 `src/` 布局。本地运行命令时需要设置 `PYTHONPATH=src`。

## 本地运行

PowerShell：

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main
```

macOS / Linux：

```bash
PYTHONPATH=src python -m ai_intel_daily.main
```

只生成 AI 日报：

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main --report ai
```

指定日期生成报告：

```powershell
$env:PYTHONPATH="src"
python -m ai_intel_daily.main --report ai --date 2026-05-22
```

macOS / Linux：

```bash
PYTHONPATH=src python -m ai_intel_daily.main --report ai --date 2026-05-22
```

生成的报告会写入：

```text
data/reports/ai/
data/reports/stocks/
```

## 本地测试

安装依赖：

```bash
python -m pip install -r requirements.txt
```

PowerShell：

```powershell
$env:PYTHONPATH="src"
python -m pytest -q
```

macOS / Linux：

```bash
PYTHONPATH=src python -m pytest -q
```

## 推荐 Git / GitHub 工作流

不要直接在默认主分支 `main` 或 `master` 上开发。每个阶段都应创建独立功能分支。

推荐流程：

1. 确认当前阶段目标。
2. 更新默认主分支。
3. 创建阶段功能分支。
4. 做小而容易检查的改动。
5. 运行本地测试。
6. 提交改动。
7. 推送分支到 GitHub。
8. 打开 Pull Request。
9. 仅在 review 和 CI 通过后合并。

示例：

```bash
git switch main
git pull
git switch -c stage2-github-workflow
PYTHONPATH=src python -m pytest -q
git add README.md
git commit -m "docs: update project workflow"
git push -u origin stage2-github-workflow
```

如果仓库使用 `master` 作为默认主分支，请把示例中的 `main` 替换为 `master`。

更多说明：

- `docs/git_workflow.md`
- `docs/github_actions.md`
- `docs/secrets.md`

## GitHub Actions

本项目包含 CI workflow：`.github/workflows/ci.yml`。

workflow 会在以下事件触发：

- `push`
- `pull_request`

它使用 Python 3.11，安装 `requirements.txt` 中的依赖，设置 `PYTHONPATH=src`，并运行：

```bash
python -m pytest -q
```

当前 CI 只运行测试，不连接真实 API，也不创建每日定时报告。

## 当前限制

- AI 日报当前只支持 RSS/Atom；暂不支持 HTML collector。
- 不接论文、社交媒体、市场、财报或券商 API。
- 没有可执行的复杂 agent 或多 Agent runtime；阶段 7 只包含设计骨架和 mock 模型客户端。
- 没有 n8n workflow、cron、日报 scheduler，或针对外部服务的真实自动化。
- 没有数据库、向量库、缓存服务或外部存储。
- 不提供买入、卖出或持有建议。
- 代码中没有 API key、密码、token 或真实凭据。
- 没有 email、Slack、飞书、Notion 或其他分发集成。
- 没有前端、后端服务或部署设置。
