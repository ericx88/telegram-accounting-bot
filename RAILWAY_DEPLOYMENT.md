# Railway 部署指南

本文档介绍如何将 Telegram 记账机器人部署到 Railway 平台。

## 🚀 快速部署

### 前置要求

1. **Railway 账号**：在 [railway.app](https://railway.app) 注册账号
2. **GitHub 账号**：用于代码托管和自动部署
3. **Telegram Bot Token**：从 [@BotFather](https://t.me/BotFather) 获取

### 部署步骤

#### 方法一：通过 GitHub 部署（推荐）

1. **上传代码到 GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Telegram accounting bot"
   git branch -M main
   git remote add origin https://github.com/your-username/telegram-accounting-bot.git
   git push -u origin main
   ```

2. **在 Railway 创建项目**
   - 登录 Railway 控制台
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择你的 GitHub 仓库
   - Railway 会自动检测 Python 项目并开始部署

3. **配置环境变量**
   - 在项目设置中添加环境变量：
     ```
     BOT_TOKEN=你的_BOT_TOKEN
     PYTHONUNBUFFERED=1
     PYTHONDONTWRITEBYTECODE=1
     ```

#### 方法二：通过 Railway CLI 部署

1. **安装 Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **登录并部署**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **设置环境变量**
   ```bash
   railway variables set BOT_TOKEN=你的_BOT_TOKEN
   railway variables set PYTHONUNBUFFERED=1
   railway variables set PYTHONDONTWRITEBYTECODE=1
   ```

## 📁 部署文件说明

| 文件 | 用途 |
|------|------|
| `railway.toml` | Railway 项目配置文件 |
| `Procfile` | 定义启动命令 |
| `runtime.txt` | 指定 Python 版本 |
| `app.json` | 应用元数据和环境变量配置 |
| `.railwayignore` | 忽略不需要上传的文件 |

## 🔧 配置说明

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `BOT_TOKEN` | ✅ | Telegram Bot Token |
| `PYTHONUNBUFFERED` | ❌ | 输出不缓冲（建议设为1） |
| `PYTHONDONTWRITEBYTECODE` | ❌ | 不生成字节码文件（建议设为1） |

### 数据持久化

- Railway 上使用 `/tmp` 目录存储数据文件
- `groups.json` 和 `ledger.json` 会在部署期间保持
- 重启后数据不会丢失

## 🐛 故障排除

### 常见问题

1. **部署失败**
   - 检查 `requirements.txt` 是否包含所有依赖
   - 确认 `Procfile` 格式正确
   - 查看构建日志找出具体错误

2. **机器人无响应**
   - 确认 `BOT_TOKEN` 环境变量设置正确
   - 检查部署日志是否有错误信息
   - 尝试重启部署

3. **数据丢失**
   - Railway 的 `/tmp` 目录在重新部署时是持久的
   - 但删除项目或严重故障时数据会丢失
   - 建议定期导出重要数据

### 查看日志

```bash
# 使用 Railway CLI
railway logs

# 或在 Railway 控制台查看实时日志
```

## 📊 监控和维护

### 性能监控

- Railway 提供基础监控指标
- 可以设置告警通知
- 建议定期检查日志和运行状态

### 更新部署

- 推送代码到 GitHub 会自动触发重新部署
- 或使用 `railway up` 手动部署

## 💰 费用说明

- Railway 提供 $5/月的免费额度
- 对于这个简单的机器人，免费额度足够使用
- 超出免费额度后按使用量计费

## 🔒 安全注意事项

1. **保护 Bot Token**：
   - 永远不要在代码中硬编码 Token
   - 使用环境变量存储敏感信息
   - 定期轮换 Token

2. **数据备份**：
   - 定期导出 `groups.json` 和 `ledger.json`
   - 考虑使用 Railway 的数据库服务存储重要数据

## 📚 参考资源

- [Railway 官方文档](https://docs.railway.app/)
- [Python 部署指南](https://docs.railway.app/deploy/python)
- [aiogram 文档](https://docs.aiogram.dev/)