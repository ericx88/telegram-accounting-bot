# Telegram 记账机器人

这是一个基于 aiogram 的 Telegram 机器人，提供群组记账和消息转发功能。

## 功能特性

- **群组记账**：支持 `+100`、`-50`、`+87.6 备注` 等格式记录收支
- **账单查询**：发送"账单"查看所有记录
- **消息转发**：私聊消息自动转发到机器人所在的所有群组
- **数据持久化**：JSON 格式存储账单和群组信息

## 快速部署

### 使用 Docker Compose

1. **克隆项目并配置**
   ```bash
   git clone <repository-url>
   cd telegram-accounting-bot
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入你的 Bot Token
   ```

3. **启动服务**
   ```bash
   docker-compose up -d
   ```

### 使用 Docker

1. **构建镜像**
   ```bash
   docker build -t telegram-bot .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name telegram-bot \
     --restart unless-stopped \
     -e BOT_TOKEN=your_bot_token_here \
     -v $(pwd)/data:/app/data \
     telegram-bot
   ```

## 使用说明

1. **获取 Bot Token**：
   - 与 [@BotFather](https://t.me/BotFather) 对话
   - 发送 `/newbot` 创建新机器人
   - 获取 Token 并填入环境变量

2. **机器人命令**：
   - `/start` - 查看帮助信息
   - `+100` - 记录收入100元
   - `-50` - 记录支出50元
   - `+87.6 工资` - 记录收入87.6元并添加备注
   - `账单` - 查看当前群组的账单记录

3. **私聊转发**：
   - 在私聊中发送消息，机器人会自动转发到其所在的所有群组

## 数据存储

- `groups.json` - 存储群组信息
- `ledger.json` - 存储账单记录
- 建议使用 Docker 卷挂载实现数据持久化

## 开发环境

```bash
# 安装依赖
pip install aiogram

# 运行机器人
python bot.py
```

## 注意事项

1. 确保机器人有足够的权限在群组中发送消息
2. 建议定期备份 `groups.json` 和 `ledger.json` 文件
3. 生产环境建议使用环境变量管理敏感信息