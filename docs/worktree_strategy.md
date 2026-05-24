# Git Worktree Strategy

本文用初学者能懂的方式说明本项目推荐的 Git worktree 使用方式。

当前阶段只讨论本地开发策略，不连接真实 API，不创建 n8n 工作流，也不创建自动化计划。

## Worktree 是什么

worktree 可以理解成：同一个 Git 仓库的多个工作文件夹。

平时我们克隆一个仓库，通常只有一个项目文件夹。例如：

```text
D:\Codex\ai-intel-daily
```

使用 worktree 后，同一个仓库可以有多个文件夹，每个文件夹可以切到不同分支。例如：

```text
D:\Codex\ai-intel-daily
D:\Codex\ai-intel-daily-ai-report
D:\Codex\ai-intel-daily-stock-report
D:\Codex\ai-intel-daily-skills
```

这些文件夹共享同一个 Git 仓库历史，但每个文件夹里的工作区是分开的。你可以在一个文件夹里开发 AI 圈日报，在另一个文件夹里开发股票日报，互不打扰。

## Branch 和 Worktree 的区别

branch 是分支。它像是一条代码历史上的工作线。

worktree 是工作文件夹。它是某个分支真正被放到磁盘上的地方。

可以这样理解：

- branch 负责记录“我要在哪条线上改代码”。
- worktree 负责提供“我在哪个文件夹里改代码”。

一个 branch 不一定需要单独的 worktree。普通开发时，一个项目文件夹里切换不同 branch 就够了。

但是当你想同时处理多个任务时，worktree 更清楚：

- 一个任务一个 branch。
- 一个 branch 一个 worktree 文件夹。
- 进入哪个文件夹，就只做那个任务。

## 为什么 Codex 适合配合 Worktree 使用

Codex 很适合在明确边界的文件夹里工作。

如果所有任务都挤在同一个项目文件夹里，容易出现这些问题：

- AI 圈日报还没做完，又开始改股票日报。
- 自动化实验改到了主分支附近的文件。
- 多个阶段的修改混在一起，很难检查。

使用 worktree 后，可以把每个任务放进独立文件夹：

- Codex 只在当前任务的 worktree 里修改。
- 每个任务都有自己的 branch，改动更容易 review。
- `main` 或 `master` 保持稳定，不承载半成品。
- 如果某个实验方向失败，可以直接删除对应 worktree，不影响其他任务。

这对 `ai-intel-daily` 这样的阶段式项目很有帮助。我们可以一边保持主线稳定，一边并行探索日报、股票研究、自动化、skills 等方向。

## 本项目的 Worktree 方案

下面是 `ai-intel-daily` 推荐的 worktree 规划。

### ai-report

用途：开发 AI 圈日报。

建议分支：

```text
feature/ai-report
```

建议目录：

```text
D:\Codex\ai-intel-daily-ai-report
```

适合做的事：

- 改进 AI 日报模板。
- 调整 Markdown 报告结构。
- 增加本地假数据示例。
- 增加针对 AI 日报输出的测试。

当前阶段不要连接真实新闻、论文、社交媒体或搜索 API。

### stock-report

用途：开发 AI 股票日报。

建议分支：

```text
feature/stock-report
```

建议目录：

```text
D:\Codex\ai-intel-daily-stock-report
```

适合做的事：

- 改进股票研究报告模板。
- 增加风险提示和研究问题。
- 检查报告中是否包含必要的免责声明。
- 增加金融安全相关测试。

股票相关内容必须保持为研究辅助，不是投资建议。报告不得提供买入、卖出、持有、重仓或保证收益等确定性建议。

### committee

用途：开发赛博投资委员会方向。

建议分支：

```text
feature/committee
```

建议目录：

```text
D:\Codex\ai-intel-daily-committee
```

适合做的事：

- 先写产品设想和文档。
- 设计委员会报告应该包含哪些 Markdown 章节。
- 用简单本地代码模拟不同视角的研究问题。

当前项目仍处于 Stage 0，不要实现复杂 agent 或 multi-agent workflow。这个 worktree 只适合做轻量原型和文档设计。

### automation

用途：开发 GitHub Actions / n8n 自动化方向。

建议分支：

```text
feature/automation
```

建议目录：

```text
D:\Codex\ai-intel-daily-automation
```

适合做的事：

- 改进 GitHub Actions CI 文档。
- 研究未来自动生成报告的流程。
- 写清楚 secrets、测试、失败处理等设计。

当前阶段不要创建真实定时任务，不要创建 n8n workflow，也不要连接外部服务。自动化想法应优先写进文档或 `docs/roadmap.md`。

### skills

用途：开发自建 Codex skills。

建议分支：

```text
feature/skills
```

建议目录：

```text
D:\Codex\ai-intel-daily-skills
```

适合做的事：

- 设计面向本项目的 Codex skill 说明。
- 总结日报生成、金融安全检查、PR review 等固定工作流。
- 先写文档，再决定是否需要真正创建 skill 文件。

skills 方向也应保持简单，不要提前引入复杂 agent、外部存储或真实 API。

## 常用命令

### 查看当前分支

```bash
git branch
```

当前分支前面会有一个 `*`。

也可以用：

```bash
git status
```

它会告诉你当前在哪个分支，以及有哪些文件被修改。

### 查看已有 Worktree

```bash
git worktree list
```

这个命令会列出当前仓库关联的所有 worktree 文件夹，以及每个文件夹对应的分支。

### 创建 Worktree

从最新主分支创建新任务时，可以这样做：

```bash
git switch master
git pull
git worktree add ..\ai-intel-daily-ai-report -b feature/ai-report
```

如果仓库默认主分支叫 `main`，就把 `master` 换成 `main`：

```bash
git switch main
git pull
git worktree add ..\ai-intel-daily-ai-report -b feature/ai-report
```

这会创建：

- 一个新分支：`feature/ai-report`
- 一个新文件夹：`..\ai-intel-daily-ai-report`

之后进入新文件夹工作：

```bash
cd ..\ai-intel-daily-ai-report
git status
```

### 移除 Worktree

任务合并后，可以删除本地 worktree：

```bash
git worktree remove ..\ai-intel-daily-ai-report
```

如果 Git 提示 worktree 里还有未提交改动，先进入该目录运行：

```bash
git status
```

确认不需要的改动不要随便删除。需要保留的内容应先 commit 或备份。

### 查看状态

开发过程中经常运行：

```bash
git status
```

它可以帮助你确认：

- 当前在哪个分支。
- 哪些文件被修改。
- 哪些文件还没加入 commit。

## 本项目推荐工作流

1. 让 `main` 或 `master` 保持稳定。
2. 开始新任务前，先更新默认主分支。
3. 为每个任务创建独立 branch 和 worktree。
4. 进入对应 worktree，让 Codex 只在这个文件夹里修改。
5. 小步修改，避免一次改太多文件。
6. 修改后运行测试。
7. 测试通过后创建 commit。
8. push 到 GitHub。
9. 创建 Pull Request。
10. 等 CI 通过后再合并。
11. 合并后删除远程分支和本地 worktree。

示例流程：

```bash
git switch master
git pull
git worktree add ..\ai-intel-daily-ai-report -b feature/ai-report
cd ..\ai-intel-daily-ai-report
git status
PYTHONPATH=src python -m pytest -q
git add docs/worktree_strategy.md
git commit -m "docs: add worktree strategy"
git push -u origin feature/ai-report
```

如果默认主分支是 `main`，把第一行的 `master` 换成 `main`。

PR 合并后：

```bash
git switch master
git pull
git worktree remove ..\ai-intel-daily-ai-report
git branch -d feature/ai-report
git push origin --delete feature/ai-report
```

如果 GitHub 已经自动删除远程分支，最后一行可能不需要运行。

## 容易踩坑的地方

### 在错误文件夹里修改

多个 worktree 同时存在时，很容易忘记自己在哪个文件夹。

开始让 Codex 修改前，先运行：

```bash
git status
```

确认当前目录和分支都对。

### main 没同步就创建 Worktree

如果主分支落后于 GitHub，基于它创建的新 worktree 也会落后。

创建新 worktree 前，先更新默认主分支：

```bash
git switch master
git pull
```

如果默认主分支叫 `main`，就用：

```bash
git switch main
git pull
```

### 多个 Worktree 同时改同一个文件

不同 worktree 可以同时存在，但如果它们都修改同一个文件，最后合并 PR 时可能产生冲突。

建议：

- 一个任务只改自己真正需要的文件。
- 公共文件例如 `README.md`、模板文件、测试文件要谨慎修改。
- 如果两个任务都需要改同一块内容，先决定哪个任务先合并。

### 合并后忘记删除 Worktree

PR 合并后，如果不删除本地 worktree，旧文件夹会越来越多，后面容易混淆。

定期查看：

```bash
git worktree list
```

合并完成且不再需要的 worktree 应删除：

```bash
git worktree remove ..\ai-intel-daily-ai-report
```

### 不知道自己当前在哪个分支

这是 Git 初学者最常见的问题之一。

随时运行：

```bash
git branch
git status
```

如果看到自己在 `master` 或 `main` 上，就不要直接开发业务改动。先创建任务分支和 worktree。

## 阶段 3 检查清单

- [ ] 我知道 worktree 是同一个仓库的多个工作文件夹。
- [ ] 我知道 branch 是代码历史上的工作线。
- [ ] 我知道 worktree 和 branch 不是同一个东西。
- [ ] 我能用 `git worktree list` 查看已有 worktree。
- [ ] 我能用 `git worktree add` 创建新任务文件夹。
- [ ] 我能用 `git status` 确认当前目录和分支。
- [ ] 我知道 `main` 或 `master` 应保持稳定。
- [ ] 我知道每个任务应使用独立 branch 和 worktree。
- [ ] 我知道让 Codex 修改前要确认自己在正确 worktree。
- [ ] 我知道测试通过后再 commit 和 push。
- [ ] 我知道 PR 合并后要删除不再需要的 worktree。
- [ ] 我知道股票报告只能作为研究辅助，不提供投资建议。
- [ ] 我知道当前阶段不创建真实 API、n8n workflow 或自动化计划。
