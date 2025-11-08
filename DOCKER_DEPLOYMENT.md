# 🐳 Docker 部署指南（推荐）

## ✅ 更新内容

已切换到 **Docker 部署方式**，这是 Railway 推荐的现代化部署方案。

### 📁 当前配置文件

- `Dockerfile` - Docker 镜像构建文件
- `railway.toml` - 使用 `builder = "DOCKERFILE"`
- `requirements.txt` - Python 依赖管理
- `bot.py` - 主要代码

## 🚀 部署步骤

### 1. 提交更新
```bash
git add .
git commit -m "Switch to Docker deployment (modern approach)"
git push
```

### 2. Railway 配置
在 Railway 控制台：
1. **创建/选择项目**
2. **连接 GitHub 仓库**
3. **设置环境变量**：
   ```
   BOT_TOKEN=你的新Token
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   ```

### 3. 自动部署
Railway 会：
- 检测到 `Dockerfile`
- 构建 Docker 镜像
- 运行容器

## 📋 预期构建日志

成功部署时您应该看到：
```
✓ Building image
✓ Pushing image
✓ Creating deployment
✓ Deployment is live

🤖 Bot started successfully: @YourBot (ID: xxxxx)
📡 Bot is polling for messages...
```

## 🔧 Dockerfile 特点

- **多阶段构建优化**：先安装依赖，再复制代码
- **非root用户**：提高安全性
- **Docker缓存优化**：requirements.txt 变化时才重新安装依赖
- **环境变量预设**：在镜像中设置推荐的环境变量

## 🚨 故障排除

### 构建失败
1. **检查 Dockerfile 语法**：
   ```bash
   docker build -t test-bot .
   ```

2. **检查依赖文件**：
   ```bash
   cat requirements.txt
   # 确保格式正确
   ```

3. **查看详细日志**：
   - Railway 控制台的 Build 日志
   - 重点关注 Docker 构建步骤

### 运行时问题
1. **检查容器日志**：
   ```bash
   railway logs
   ```

2. **环境变量确认**：
   ```bash
   railway variables list
   ```

3. **重启容器**：
   ```bash
   railway restart
   ```

## 🔍 调试命令

```bash
# 本地测试Docker镜像
docker build -t telegram-bot .
docker run --rm -e BOT_TOKEN=你的Token telegram-bot

# 强制重新部署
railway up --force

# 查看部署状态
railway status

# 查看实时日志
railway logs --follow
```

## 💡 Docker 部署的优势

1. **一致性**：本地和生产环境完全一致
2. **缓存优化**：Docker 层缓存加速构建
3. **隔离性**：容器化部署，环境隔离
4. **可扩展**：易于扩展和迁移
5. **现代化**：符合容器化部署最佳实践

## 📦 文件说明

| 文件 | 用途 | 必需 |
|------|------|------|
| `Dockerfile` | 定义Docker镜像 | ✅ |
| `railway.toml` | Railway项目配置 | ✅ |
| `requirements.txt` | Python依赖 | ✅ |
| `bot.py` | 主要代码 | ✅ |
| `groups.json` | 群组数据 | ❌（会自动创建）|
| `ledger.json` | 账单数据 | ❌（会自动创建）|

---

## 🎯 快速参考

### 常用命令
```bash
# 构建并测试（本地）
docker build -t bot .
docker run --rm -e BOT_TOKEN=test bot

# 部署到Railway
git push origin main

# 查看状态
railway status
railway logs
```

### 环境变量
```bash
BOT_TOKEN=你的Token
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

现在使用 Docker 方式部署应该更加稳定和可靠！🚀