# Git / GitHub 工作流

本文用初学者能懂的方式说明本项目推荐的 Git 和 GitHub 使用方式。

## Issue 是什么

Issue 可以理解成一张任务卡。

它可以记录：

- 要做的新功能
- 发现的问题
- 需要讨论的想法
- 一个阶段的目标

在本项目中，一个 Issue 最好只描述一件清楚的事。例如：

- 阶段 2：建立 GitHub Actions CI
- 阶段 3：接入真实新闻数据源

## Branch 是什么

Branch 是分支。它像是从主线复制出来的一条工作线。

不要直接在默认主分支 `main` 或 `master` 上开发。每个阶段都应该创建独立功能分支，这样改动更容易检查，也更容易回退。

示例：

```bash
git switch -c stage2-github-workflow
```

## Commit 是什么

Commit 是一次保存到 Git 历史里的改动快照。

一个好的 commit 应该：

- 改动范围小
- 主题清楚
- 可以让别人看懂为什么改

示例：

```bash
git add README.md
git commit -m "docs: add local testing instructions"
```

## Pull / Push 是什么

`pull` 是把 GitHub 上的最新代码拉到本地。

```bash
git pull
```

`push` 是把本地提交推送到 GitHub。

```bash
git push
```

第一次推送新分支时通常需要：

```bash
git push -u origin stage2-github-workflow
```

## Pull Request 是什么

Pull Request，简称 PR，是把一个分支的改动请求合并到另一个分支。

在本项目中，通常是：

- 从阶段功能分支发起 PR
- 合并到默认主分支 `main` 或 `master`

PR 的作用是：

- 让自己或别人检查改动
- 让 GitHub Actions 自动运行测试
- 在合并前发现问题
- 保留清楚的开发记录

## 本项目推荐的开发流程

1. 确认当前阶段目标。
2. 从默认主分支更新最新代码。
3. 为当前阶段创建独立功能分支。
4. 小步修改文件。
5. 本地运行测试。
6. 创建 commit。
7. push 到 GitHub。
8. 创建 PR。
9. 等 CI 通过后再合并。

## 每个阶段如何操作

阶段开始时：

```bash
git switch main
git pull
git switch -c stage2-github-workflow
```

如果仓库默认主分支叫 `master`，就把上面的 `main` 换成 `master`。

开发中：

```bash
git status
```

查看哪些文件被修改。每次修改都尽量保持范围小，便于检查。

提交前：

```bash
PYTHONPATH=src python -m pytest -q
```

测试通过后提交：

```bash
git add README.md docs/git_workflow.md
git commit -m "docs: add git workflow guide"
```

推送分支：

```bash
git push -u origin stage2-github-workflow
```

创建 PR：

- 打开 GitHub 仓库页面
- 点击 Compare & pull request
- 写清楚本阶段做了什么
- 等 GitHub Actions 跑完

合并后：

```bash
git switch main
git pull
```

如果默认主分支是 `master`，同样把 `main` 换成 `master`。

