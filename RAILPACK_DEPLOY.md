# 🚀 Railpack 构建系统部署指南

## ✅ 已配置 Railpack 支持

Railway 现在默认使用 **Railpack** 构建系统，这是最新的构建引擎：

### 📁 当前配置文件

1. **`railway.toml`** - 使用 `builder = "RAILPACK"`
2. **`requirements.txt`** - Python 依赖
3. **`runtime.txt`** - Python 版本指定
4. **`bot.py`** - 主要代码

### 🔧 Railpack 配置

**railway.toml**:
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "python bot.py"
restartPolicyType = "ON_FAILURE"
```

**runtime.txt**:
```
python-3.11.0
```

**requirements.txt**:
```
aiogram>=3.0.0
```

## 🚀 部署步骤

### 1. 提交 Railpack 配置

```bash
git add .
git commit -m "Switch to Railpack build system"
git push
```

### 2. Railway 控制台

1. **访问 Railway 控制台**：
   - https://railway.app
   - 登录您的账户

2. **创建/选择项目**：
   - 如果是新项目：点击 "New Project"
   - 选择 "Deploy from GitHub repo"

3. **连接代码**：
   - 连接您的 GitHub 仓库
   - 选择 `main` 分支

4. **设置环境变量**：
   ```
   BOT_TOKEN=你的Token
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   ```

### 3. 自动构建

Railpack 会自动：
- ✅ 检测到 Python 项目
- ✅ 安装 Python 3.11
- ✅ 安装 requirements.txt 中的依赖
- ✅ 运行 bot.py

## 📋 预期构建日志

成功的 Railpack 构建应该显示：
```
📦 Building with Railpack
🐍 Python detected
📦 Installing Python 3.11
📦 Installing dependencies from requirements.txt
✅ Build completed
🚀 Starting service
Bot started successfully: @YourBot (ID: xxxxx)
```

## 🎯 Railpack 的优势

1. **更快的构建**：优化的构建缓存和并行处理
2. **智能检测**：自动检测项目类型和依赖
3. **无需 Dockerfile**：简化配置
4. **现代化**：Railway 的最新构建引擎
5. **更可靠**：减少配置错误

## 🔍 文件要求

确保以下文件存在且格式正确：

### requirements.txt
```
aiogram>=3.0.0
```

### runtime.txt
```
python-3.11.0
```

### railway.toml
```toml
[build]
builder = "RAILPACK"

[deploy]
startCommand = "python bot.py"
restartPolicyType = "ON_FAILURE"
```

### bot.py
```python
# 主要代码文件
import os
from aiogram import Bot, Dispatcher

# ... 其他代码
```

## 🚨 如果构建失败

### 检查清单
- ✅ `railway.toml` 使用 `RAILPACK`
- ✅ `requirements.txt` 格式正确
- ✅ `runtime.txt` 指定 Python 版本
- ✅ `bot.py` 语法正确
- ✅ 环境变量已设置

### 常见问题
1. **依赖冲突**：检查 `requirements.txt` 格式
2. **Python 版本**：确保 `runtime.txt` 版本正确
3. **启动命令**：确认 `startCommand` 正确

## 💡 为什么 Railpack 更好

- **性能优化**：比 Docker 和 Nixpacks 更快
- **自动检测**：智能识别项目结构
- **简化配置**：最少的配置文件
- **现代化**：Railway 的推荐构建方式

---

现在使用 Railpack 构建系统，应该能够成功快速部署！🚀