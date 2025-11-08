#!/usr/bin/env python3
import asyncio
import os
from aiogram import Bot

async def quick_clear():
    """快速清理Telegram冲突"""
    token = "8424353653:AAFAgNubsDb1xwGEtwkelH6OYc3JwdynD5Y"

    print("🔧 开始快速清理Telegram冲突...")

    try:
        bot = Bot(token=token)

        # 获取bot信息
        bot_info = await bot.get_me()
        print(f"✅ Bot信息: @{bot_info.username} (ID: {bot_info.id})")

        # 获取当前webhook状态
        webhook_info = await bot.get_webhook_info()
        print(f"📋 当前Webhook: {webhook_info.url or '无'}")

        # 强制删除webhook
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook已删除")

        # 等待几秒
        await asyncio.sleep(3)

        # 再次确认
        final_webhook = await bot.get_webhook_info()
        print(f"📋 最终状态: {final_webhook.url or '已清除'}")

        print("🎉 冲突清理完成！现在可以重启机器人了。")

    except Exception as e:
        print(f"❌ 错误: {e}")
        if "Conflict" in str(e):
            print("⚠️ 仍然冲突！建议:")
            print("1. 重新生成Token")
            print("2. 等待5-10分钟")
            print("3. 联系@BotFather")

if __name__ == "__main__":
    asyncio.run(quick_clear())