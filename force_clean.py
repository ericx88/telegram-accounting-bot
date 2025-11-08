#!/usr/bin/env python3
"""
强制清理Telegram Bot的所有冲突状态
"""

import asyncio
import os
from aiogram import Bot

async def force_cleanup():
    """强制清理bot的所有状态"""
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        print("❌ 未找到 BOT_TOKEN 环境变量")
        return

    try:
        bot = Bot(token=bot_token)

        print("🔧 开始强制清理...")

        # 1. 获取bot信息
        bot_info = await bot.get_me()
        print(f"✅ Bot信息: @{bot_info.username} (ID: {bot_info.id})")

        # 2. 获取当前webhook状态
        webhook_info = await bot.get_webhook_info()
        print(f"📋 当前Webhook: {webhook_info.url or '无'}")

        # 3. 强制删除webhook并丢弃所有待处理更新
        print("🧹 强制删除Webhook...")
        await bot.delete_webhook(drop_pending_updates=True)

        # 4. 再次确认webhook已删除
        webhook_info_after = await bot.get_webhook_info()
        if webhook_info_after.url:
            print("⚠️ Webhook仍然存在，尝试再次删除...")
            await bot.delete_webhook(drop_pending_updates=True)
            await asyncio.sleep(2)

        # 5. 最终检查
        final_webhook = await bot.get_webhook_info()
        print(f"✅ 最终Webhook状态: {final_webhook.url or '已清除'}")

        print("🎉 强制清理完成！现在可以安全启动webhook模式。")

    except Exception as e:
        print(f"❌ 清理过程中出错: {e}")
        if "Conflict" in str(e):
            print("⚠️ 检测到冲突！可能需要等待几分钟让Telegram服务器更新。")
            print("💡 建议联系@BotFather重新生成Token。")

if __name__ == "__main__":
    print("=== 强制清理工具 ===\n")
    asyncio.run(force_cleanup())