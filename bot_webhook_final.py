import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.types import Message, ChatMemberUpdated
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# ======= 1. Bot Token 配置 =======
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("请设置 BOT_TOKEN 环境变量")

# ======= 2. Webhook 配置 =======
PORT = int(os.getenv("PORT", 8000))
WEBHOOK_HOST = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
if not WEBHOOK_HOST:
    # 如果没有域名，使用默认路径
    WEBHOOK_PATH = "/webhook"
else:
    # 使用域名生成唯一路径
    WEBHOOK_PATH = f"/webhook/{BOT_TOKEN[:16]}"
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST else ""

# ======= 3. 群列表存放文件 =======
GROUPS_FILE = Path("/tmp/groups.json")

# ======= 4. 记账存放文件 =======
LEDGER_FILE = Path("/tmp/ledger.json")

# ================== 工具：钱的格式化 ==================
def fmt_money(v: float) -> str:
    if float(v).is_integer():
        return str(int(v))
    s = f"{v:.4f}"
    s = s.rstrip("0").rstrip(".")
    return s

# ================== 基础：群列表 保存/读取 ==================
def load_groups() -> dict:
    if not GROUPS_FILE.exists():
        return {}
    try:
        return json.loads(GROUPS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_groups(data: dict):
    GROUPS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def add_group(chat_id: int, title: str):
    data = load_groups()
    data[str(chat_id)] = {"title": title}
    save_groups(data)

def remove_group(chat_id: int):
    data = load_groups()
    if str(chat_id) in data:
        data.pop(str(chat_id))
        save_groups(data)

# ================== 记账：保存/读取 ==================
def load_ledger() -> dict:
    if not LEDGER_FILE.exists():
        return {}
    try:
        return json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_ledger(data: dict):
    LEDGER_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def add_ledger_entry(chat_id: int, user_name: str, amount: float, note: str) -> float:
    data = load_ledger()
    key = str(chat_id)
    if key not in data:
        data[key] = {"balance": 0.0, "entries": []}

    data[key]["balance"] = float(data[key].get("balance", 0.0)) + float(amount)
    balance = float(data[key]["balance"])

    entry = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_name": user_name,
        "amount": float(amount),
        "note": note,
    }
    data[key]["entries"].append(entry)

    save_ledger(data)
    return balance

def get_group_ledger(chat_id: int):
    data = load_ledger()
    return data.get(str(chat_id))

# ================== 群内记账处理 ==================
ACCOUNTING_PATTERN = re.compile(r'^[+-]\s*(\d+(?:\.\d+)?)(?:\s+(.*))?$', re.S)

async def handle_group_accounting(message: Message):
    if not message.text:
        return

    text = message.text.strip()
    chat_id = message.chat.id

    # 1) 账单指令
    if text == "账单":
        ledger = get_group_ledger(chat_id)
        if not ledger or not ledger.get("entries"):
            await message.answer("当前没有账单记录。")
            return

        entries = ledger["entries"]
        balance = float(ledger["balance"])

        lines = [f"共 {len(entries)} 条 记录，剩余 $ {fmt_money(balance)}"]

        for e in reversed(entries):
            amt = float(e["amount"])
            direction = "入" if amt > 0 else "出"
            line = f"{e['ts']} {e['user_name']} {direction} $ {fmt_money(abs(amt))}"
            lines.append(line)
            if e.get("note"):
                lines.append(e["note"])

        await message.answer("\n".join(lines))
        return

    # 2) 记账格式
    m = ACCOUNTING_PATTERN.match(text)
    if not m:
        return

    raw_amount = m.group(1)
    note = m.group(2) or ""

    sign = 1 if text.lstrip().startswith("+") else -1
    amount = sign * float(raw_amount)

    from_user = message.from_user
    user_name = (
        from_user.full_name
        or (from_user.username and f"@{from_user.username}")
        or str(from_user.id)
    )

    balance = add_ledger_entry(chat_id, user_name, amount, note)

    if amount > 0:
        resp = f"入金 $ {fmt_money(amount)}，剩余 $ {fmt_money(balance)}"
    else:
        resp = f"出金 $ {fmt_money(abs(amount))}，剩余 $ {fmt_money(balance)}"

    if note:
        resp = resp + "\n" + note

    await message.answer(resp)

# ================== 群消息入口（记录群 + 记账） ==================
async def handle_group_message(message: Message):
    chat = message.chat
    if chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        add_group(chat.id, chat.title or "")
        await handle_group_accounting(message)

# ================== 机器人进出群事件 ==================
async def handle_my_chat_member(update: ChatMemberUpdated):
    chat = update.chat
    if chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return

    new_status = update.new_chat_member.status

    if new_status in ("member", "administrator"):
        add_group(chat.id, chat.title or "")
    if new_status in ("kicked", "left", "restricted"):
        remove_group(chat.id)

# ================== 私聊：消息转发到所有群 ==================
async def handle_private_message(message: Message, bot: Bot):
    if message.chat.type != ChatType.PRIVATE:
        return

    groups = load_groups()
    if not groups:
        await message.answer("目前我还没有在任何群里，先把我拉进群再试。")
        return

    sent_count = 0
    for chat_id_str, info in groups.items():
        chat_id = int(chat_id_str)
        try:
            await bot.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
            sent_count += 1
        except Exception as e:
            print(f"send to {chat_id} failed: {e}")

    await message.answer(f"已发送到 {sent_count} 个群。")

# ================== /start ==================
async def cmd_start(message: Message):
    await message.answer(
        "你好，我是群转发 + 简易记账机器人。\n"
        "1. 私聊我 → 我把消息发到我在的所有群。\n"
        "2. 群里发 +100 / -50 / +87.6 备注 → 我帮你记账（支持小数）。\n"
        "3. 群里发'账单' → 我把本群账本列出来。\n"
        "\n🤖 Webhook模式运行中（无冲突）"
    )

# ================== 健康检查 ==================
async def health_check(request):
    """健康检查端点"""
    return web.Response(text="Bot is running with webhook mode - No conflicts!")

# ================== 主入口 ==================
async def main():
    try:
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )

        bot_info = await bot.get_me()
        print(f"🤖 Bot started: @{bot_info.username} (ID: {bot_info.id})")

        if WEBHOOK_URL:
            print(f"🌐 Webhook URL: {WEBHOOK_URL}")
        else:
            print(f"📡 Webhook Path: {WEBHOOK_PATH}")

        dp = Dispatcher()

        # 注册处理器
        dp.message.register(cmd_start, F.text == "/start")
        dp.message.register(handle_private_message, F.chat.type == ChatType.PRIVATE)
        dp.message.register(
            handle_group_message,
            F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP})
        )
        dp.my_chat_member.register(handle_my_chat_member)

        # 清除可能存在的旧webhook
        await bot.delete_webhook(drop_pending_updates=True)
        print("🧹 Old webhook cleared")

        # 设置新webhook
        if WEBHOOK_URL:
            await bot.set_webhook(
                url=WEBHOOK_URL,
                drop_pending_updates=True,
                allowed_updates=["message", "my_chat_member"]
            )
            print(f"✅ Webhook set: {WEBHOOK_URL}")
        else:
            print("⚠️ No domain available, webhook path only")

        # 创建web应用
        app = web.Application()

        # 创建webhook请求处理器
        webhook_request_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_request_handler.register(app, path=WEBHOOK_PATH)

        # 添加健康检查路由
        app.router.add_get("/", health_check)

        # 启动web服务器
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', PORT)
        await site.start()

        print(f"🚀 Webhook server running on port {PORT}")
        print(f"💚 Health check: http://localhost:{PORT}/")
        if WEBHOST_URL:
            print(f"🌐 External health check: {WEBHOOK_URL}")
        print("🎉 Bot running in webhook mode - No polling conflicts!")

        # 保持运行
        while True:
            await asyncio.sleep(3600)

    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())