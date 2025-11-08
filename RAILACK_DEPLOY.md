# 🚀 Railack 构建系统部署指南

## ✅ 已配置 Railack 支持

Railway 现在默认使用 **Railack** 构建系统，我已经更新了配置：

### 📁 当前配置文件

1. **`railway.toml`** - 使用 `builder = "NIXPACKS"`
2. **`nixpacks.toml`** - Railack 构建配置
3. **`requirements.txt`** - Python 依赖
4. **`bot.py`** - 主要代码
5. **`runtime.txt`** - Python 版本指定

### 🔧 Nixpacks 配置

```toml
[phases.setup]
nixPkgs = ["...", "python311"]

[phases.build]
cmd = "python -m pip install --upgrade pip && pip install -r requirements.txt"

[start]
cmd = "python bot.py"

[variables]
PYTHONUNBUFFERED = "1"
PYTHONDONTWRITEBYTECODE = "1"
```

## 🚀 部署步骤

### 1. 提交 Railack 配置

```bash
git add .
git commit -m "Switch to Railack build system"
git push
```

### 2. Railway 控制台

1. **访问 Railway 控制台**：
   - https://railway.app
   - 登录您的账户

2. **创建/选择项目**：
   - 如果是新项目：点击 "New Project"
   - 如果是现有项目：进入项目设置

3. **连接代码**：
   - 选择 "Deploy from GitHub repo"
   - 连接您的 GitHub 仓库
   - 或者直接在控制台中添加文件

4. **设置环境变量**：
   ```
   BOT_TOKEN=你的Token
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   ```

### 3. 自动构建

Railack 会自动：
- ✅ 检测到 Python 项目
- ✅ 安装 Python 3.11
- ✅ 安装 requirements.txt 中的依赖
- ✅ 运行 bot.py

## 📋 预期构建日志

成功的 Railack 构建应该显示：
```
📦 Building with Nixpacks
🐍 Python detected
📦 Installing Python 3.11
📦 Installing dependencies from requirements.txt
✅ Build completed
🚀 Starting service
Bot started successfully: @YourBot (ID: xxxxx)
```

## 🎯 Railack 的优势

1. **无需 Dockerfile**：自动检测项目类型
2. **更快构建**：优化的构建缓存
3. **自动依赖管理**：智能检测和安装依赖
4. **现代化**：Railway 的最新构建系统
5. **更可靠**：减少配置错误

## 🔍 如果构建失败

### 检查文件
确保以下文件存在且格式正确：
- ✅ `nixpacks.toml`
- ✅ `requirements.txt`
- ✅ `bot.py`
- ✅ `runtime.txt` (可选)

### 常见问题
1. **Python 版本**：确保 `runtime.txt` 指定正确版本
2. **依赖格式**：检查 `requirements.txt` 格式
3. **启动命令**：确认 `nixpacks.toml` 中的启动命令正确

### 调试方法
1. 查看构建日志中的错误信息
2. 检查文件语法和格式
3. 简化配置，逐步添加功能

## 📞 获取帮助

如果 Railack 部署仍有问题：
1. 查看详细的构建日志
2. 确认环境变量设置
3. 检查文件完整性
4. 联系 Railway 支持

---

现在使用 Railack 构建系统，应该能够成功部署！🚀