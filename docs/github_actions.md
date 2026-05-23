# GitHub Actions

## GitHub Actions 是什么

GitHub Actions 是 GitHub 提供的自动化工具。

当代码被推送到 GitHub，或者有人创建 Pull Request 时，GitHub Actions 可以自动执行一组命令。例如：

- 安装 Python
- 安装依赖
- 运行测试
- 检查代码是否能正常工作

这些命令写在 `.github/workflows/` 目录下的 YAML 文件里。

## 为什么本项目需要 GitHub Actions

`ai-intel-daily` 会逐步从本地假数据报告，扩展到更多数据来源和更完整的报告流程。

在早期阶段就加入 GitHub Actions 的好处是：

- 每次 push 后自动检查测试是否通过
- 每个 PR 合并前都能被验证
- 避免把明显坏掉的代码合并到默认主分支
- 让开发流程更稳定，也更适合初学者练习

## CI 是什么

CI 是 Continuous Integration，中文常叫持续集成。

它的意思是：每次代码发生变化时，自动把代码放到一个干净环境里运行检查。这样可以更早发现问题，而不是等很多改动堆在一起后才发现。

本项目当前的 CI 目标很简单：

- 安装依赖
- 设置 `PYTHONPATH=src`
- 运行 pytest

## 本项目如何自动运行测试

本项目的 CI workflow 文件是：

```text
.github/workflows/ci.yml
```

它会在以下情况运行：

- 有代码 push 到 GitHub
- 有 Pull Request 被创建或更新

CI 会使用 Python 3.11，并运行：

```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python -m pytest -q
```

因为本项目使用 `src/` 目录结构，所以 CI 需要设置 `PYTHONPATH=src`，让 Python 能找到 `ai_intel_daily` 包。

## 后续如何扩展到每日自动生成报告

未来如果项目进入真实数据阶段，可以考虑扩展 GitHub Actions：

- 使用 GitHub Secrets 保存 API key
- 增加定时触发 `schedule`
- 每天运行报告生成脚本
- 把生成的 Markdown 报告保存为 artifact 或提交到指定分支
- 增加失败通知

但当前阶段不创建每日自动任务，也不连接真实 API。这里只记录未来方向。

