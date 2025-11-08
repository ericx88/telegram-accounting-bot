import asyncio
import os
from aiogram import Bot

async def clear_conflicts():
    """清理所有冲突"""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Error: BOT_TOKEN not found")
        return

    bot = Bot(token=bot_token)

    try:
        # 获取bot信息
        bot_info = await bot.get_me()
        print(f"Bot: @{bot_info.username}")

        # 获取webhook信息
        webhook_info = await bot.get_webhook_info()
        print(f"Current webhook: {webhook_info.url}")

        # 强制删除webhook
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook deleted successfully")

        # 等待几秒钟
        await asyncio.sleep(3)

        # 再次确认
        final_webhook = await bot.get_webhook_info()
        print(f"Final webhook status: {final_webhook.url}")

        print("Conflicts cleared! Now you can restart the bot.")

    except Exception as e:
        print(f"Error: {e}")
        if "Conflict" in str(e):
            print("Still conflicting! You may need to:")
            print("1. Wait 5-10 minutes")
            print("2. Generate a new token from @BotFather")

if __name__ == "__main__":
    asyncio.run(clear_conflicts())