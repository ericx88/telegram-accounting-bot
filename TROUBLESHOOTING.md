# 故障排除指南

## Telegram 冲突错误解决

### 错误信息
```
TelegramConflictError: Telegram server says - Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

### 问题原因
这个错误表示有多个机器人实例在使用同一个 Token 同时调用 Telegram API。

### 解决方案

#### 1. 检查并停止本地运行的实例

**确认本地没有运行机器人：**
```bash
# 检查是否有 Python 进程在运行
ps aux | grep python

# 如果有，停止相关进程
pkill -f "python bot.py"
```

#### 2. 在 Railway 上重新部署

**方法一：通过控制台重新部署**
1. 登录 [Railway 控制台](https://railway.app)
2. 进入你的项目
3. 点击 "Redeploy" 按钮
4. 等待部署完成

**方法二：使用 CLI 重新部署**
```bash
railway up
```

#### 3. 检查是否有多个部署实例

1. 在 Railway 控制台中检查项目设置
2. 确保只有一个环境/实例在运行
3. 如果有多个，删除不需要的实例

#### 4. 重启 Railway 项目

1. 在 Railway 控制台中
2. 点击项目设置
3. 点击 "Restart" 按钮

#### 5. 清理并重新创建项目（终极方案）

如果以上方法都不奏效：

1. **备份重要数据**
   ```bash
   # 如果有重要数据，先导出
   railway logs > logs.txt
   ```

2. **删除并重新创建项目**
   - 在 Railway 控制台删除项目
   - 重新创建项目
   - 重新配置环境变量
   - 重新部署

### 预防措施

#### 1. 使用环境变量管理
确保不要在代码中硬编码 Token，始终使用环境变量。

#### 2. 单实例运行
Railway 默认运行单个实例，这是好的实践。避免配置多个实例。

#### 3. 部署前检查
在部署前，确保：
- 本地没有运行相同的机器人
- 之前的其他部署已经停止
- Token 没有在其他地方使用

### 验证解决方法

部署成功后，检查日志应该看到：
```
Bot started successfully: @your_bot_username (ID: 123456789)
Bot is polling for messages...
```

而不是冲突错误信息。

### 其他可能的问题

#### 1. Token 被其他服务使用
如果你怀疑 Token 被其他服务使用：
1. 联系 [@BotFather](https://t.me/BotFather)
2. 使用 `/revoke` 命令撤销当前 Token
3. 生成新的 Token
4. 更新环境变量

#### 2. 网络问题
偶尔网络问题也会导致类似错误，通常重启项目可以解决。

## 🆕 Webhook 模式解决方案

如果轮询模式持续冲突，可以切换到 Webhook 模式：

### 1. 使用新的 Webhook 版本

项目现在包含 `bot_webhook.py`，这是 Webhook 模式的版本：

- 自动适配 Railway 的 HTTP 端口
- 使用唯一的 Webhook 路径
- 包含健康检查端点
- 自动处理 Webhook 设置和清理

### 2. 切换到 Webhook 模式

1. **更新 Procfile**（已完成）：
   ```
   web: python bot_webhook.py
   ```

2. **重新部署**：
   ```bash
   railway up
   ```

3. **验证部署**：
   - 访问 `https://your-app.railway.app/` 应该显示 "Bot is running with webhook mode"
   - Railway 会自动为 Webhook 配置 SSL

### 3. 使用冲突清理工具

运行提供的清理脚本：
```bash
python CLEAR_CONFLICT.py
```

这个脚本会：
- 检查 Bot 状态
- 显示当前 Webhook 信息
- 清除所有冲突的 Webhook
- 提供诊断信息

### 4. 终极解决方案：重新生成 Token

如果以上方法都不奏效：

1. **联系 @BotFather**
2. **使用 `/revoke` 命令**撤销当前 Token
3. **生成新的 Token**
4. **更新 Railway 环境变量**
5. **重新部署**

### 联系支持

如果问题持续存在：
1. 收集相关日志信息
2. 记录你尝试过的解决方案
3. 联系 [Railway 支持](https://railway.app/support)
4. 或在 GitHub Issues 中寻求帮助