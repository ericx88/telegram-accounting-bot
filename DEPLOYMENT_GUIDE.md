# 🚀 Railway 部署指南（已更新构建系统）

## ✅ 配置更新

Railway 已弃用 Nixpacks，已更新为使用 **Heroku Buildpack**。

### 📁 已更新的配置文件

- `railway.toml` - 使用 `builder = "HEROKU"`
- `app.json` - 配置了 `heroku/python` buildpack
- `requirements.txt` - Python 依赖管理
- `Procfile` - 启动命令定义

## 🔧 快速部署步骤

### 1. 环境准备
确保你已经：
- [ ] 获取了新的 Bot Token（从 @BotFather）
- [ ] 运行了冲突清理工具（如果之前有冲突）

### 2. 提交代码
```bash
git add .
git commit -m "Update: Use Heroku buildpack instead of deprecated Nixpacks"
git push
```

### 3. Railway 配置
在 Railway 控制台中：
1. **创建或选择项目**
2. **连接 GitHub 仓库**
3. **设置环境变量**：
   ```
   BOT_TOKEN=你的新Token
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   ```

### 4. 部署
- Railway 会自动检测到代码更改并开始部署
- 使用 Heroku Python buildpack 构建环境
- 安装 `requirements.txt` 中的依赖

## 📋 验证部署成功

成功部署的日志应该显示：
```
-----> Python app detected
-----> Installing python-3.11.0
-----> Installing pip
-----> Installing requirements with pip
       Collecting aiogram>=3.0.0
       ...
-----> Discovering process types
       Procfile declares types -> web

-----> Compressing...
-----> Launching...
https://your-app.railway.app deployed to Railway

Bot started successfully: @YourBot (ID: xxxxx)
Bot is polling for messages...
```

## 🚨 故障排除

### 如果部署失败
1. **检查语法错误**：
   ```bash
   python -m py_compile bot.py
   ```

2. **检查依赖文件**：
   ```bash
   cat requirements.txt
   # 应该包含：
   # aiogram>=3.0.0
   ```

3. **查看构建日志**：
   - 在 Railway 控制台查看详细错误信息
   - 重点关注 build 和 launch 阶段

### 如果运行时冲突
1. **运行清理工具**：
   ```bash
   python complete_reset.py
   ```

2. **确保 Token 唯一**：
   - 检查没有其他地方使用相同 Token
   - 考虑重新生成新 Token

3. **重启服务**：
   ```bash
   railway restart
   ```

## 🔍 调试命令

```bash
# 检查构建
git status
git log --oneline -5

# 强制重新部署
railway up --force

# 查看日志
railway logs

# 重启服务
railway restart
```

## 📞 支持资源

- [Railway 文档](https://docs.railway.app/)
- [Heroku Python Buildpack](https://devcenter.heroku.com/articles/heroku-python)
- [aiogram 文档](https://docs.aiogram.dev/)

---

## 🎯 快速参考

| 文件 | 用途 |
|------|------|
| `railway.toml` | Railway 项目配置 |
| `app.json` | Buildpack 配置 |
| `requirements.txt` | Python 依赖 |
| `Procfile` | 启动命令 |
| `bot.py` | 主要代码 |

现在使用新的构建系统重新部署应该能成功！🚀