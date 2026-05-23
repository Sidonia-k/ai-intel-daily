# Secrets 管理

## Secrets 是什么

Secrets 是需要保密的敏感信息，例如：

- API key
- 密码
- token
- 邮箱登录凭据

这些信息不能直接写进代码，也不能提交到 GitHub。

## 为什么 API key 不能写进代码

如果 API key 被写进代码并提交到 GitHub，可能会导致：

- 任何看到仓库的人都能使用这个 key
- 账号产生额外费用
- 数据或服务权限被滥用
- 即使后来删除，也可能留在 Git 历史里

所以真实密钥必须放在本地环境或 GitHub Secrets 中，不应该出现在代码、文档、测试快照或日志里。

## `.env`、`.env.example`、GitHub Secrets 的区别

`.env` 是本地真实配置文件。

- 可以放真实 API key
- 只存在于自己的电脑上
- 必须加入 `.gitignore`
- 不能提交到 GitHub

`.env.example` 是示例配置文件。

- 只写变量名或假值
- 用来告诉别人需要哪些配置
- 可以提交到 GitHub

GitHub Secrets 是 GitHub 仓库里的加密配置。

- 用于 GitHub Actions
- 适合保存 CI 或自动任务需要的密钥
- 不会直接显示在 workflow 日志里
- 仍然要避免在脚本中打印出来

## 本项目未来可能需要的 secrets

未来接入真实数据或邮件功能时，可能需要：

```text
OPENAI_API_KEY
NEWS_API_KEY
MARKET_DATA_API_KEY
EMAIL_USER
EMAIL_PASSWORD
```

当前阶段不需要配置这些 secrets，也不会连接真实 API。

## 不要在日志里打印 secrets

即使 secrets 没有写进代码，也要避免在日志中输出它们。

不要这样做：

```python
print(api_key)
```

也不要把完整请求头、完整环境变量或完整错误上下文直接打印出来。

更安全的做法是只打印非敏感状态：

```python
print("API key is configured")
```

股票相关报告也必须保持为研究辅助，不构成投资建议，不提供买入、卖出或持有建议。

