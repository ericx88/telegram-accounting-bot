#!/usr/bin/env python3
"""
完全重置Telegram Bot状态
清除所有可能的冲突源
"""

import asyncio
import os
import sys
from aiogram import Bot

async def complete_reset():
    """完全重置bot状态"""
    bot_token = input("请输入新的Bot Token: ").strip()

    if not bot_token:
        print("❌ Token不能为空")
        return

    print(f"🔧 开始完全重置Bot: {bot_token[:20]}...")

    try:
        bot = Bot(token=bot_token)

        # 1. 获取bot信息验证token有效性
        print("\n1️⃣ 验证Token...")
        bot_info = await bot.get_me()
        print(f"✅ Bot信息: @{bot_info.username} (ID: {bot_info.id})")

        # 2. 获取当前状态
        print("\n2️⃣ 检查当前状态...")
        webhook_info = await bot.get_webhook_info()
        print(f"   当前Webhook: {webhook_info.url or '无'}")
        print(f"   待处理更新: {webhook_info.pending_update_count}")
        print(f"   最后错误: {webhook_info.last_error_message or '无'}")

        # 3. 强制清除webhook（多次尝试）
        print("\n3️⃣ 强制清除Webhook...")
        for i in range(5):
            try:
                await bot.delete_webhook(drop_pending_updates=True)
                print(f"   清除尝试 {i+1}/5 ✅")
                await asyncio.sleep(2)  # 等待2秒
            except Exception as e:
                print(f"   清除尝试 {i+1}/5 ❌: {e}")

        # 4. 再次确认webhook状态
        print("\n4️⃣ 验证清除结果...")
        final_webhook = await bot.get_webhook_info()
        print(f"   最终Webhook: {final_webhook.url or '已清除'}")
        print(f"   待处理更新: {final_webhook.pending_update_count}")

        # 5. 测试获取me信息（确保连接正常）
        print("\n5️⃣ 测试连接...")
        test_info = await bot.get_me()
        print(f"✅ 连接测试成功: @{test_info.username}")

        # 6. 提供后续步骤
        print(f"\n🎉 重置完成！")
        print(f"\n📋 后续步骤:")
        print(f"1. 等待2-3分钟让Telegram服务器完全更新")
        print(f"2. 在Railway中设置新的BOT_TOKEN环境变量")
        print(f"3. 重新部署项目: railway up")
        print(f"4. 确保没有其他地方运行相同的机器人")

        # 7. 生成配置命令
        print(f"\n🔧 Railway环境变量设置:")
        print(f"BOT_TOKEN={bot_token}")
        print(f"PYTHONUNBUFFERED=1")
        print(f"PYTHONDONTWRITEBYTECODE=1")

    except Exception as e:
        print(f"❌ 重置过程中出错: {e}")
        if "Conflict" in str(e):
            print(f"\n⚠️ 仍然检测到冲突！")
            print(f"可能的原因:")
            print(f"1. 有其他进程在使用这个Token")
            print(f"2. 需要更长时间等待Telegram服务器更新")
            print(f"3. 可能需要再次重新生成Token")
            print(f"\n💡 建议:")
            print(f"1. 检查是否有本地或其他服务器在运行机器人")
            print(f"2. 等待10-15分钟后重试")
            print(f"3. 联系@BotFather再次重新生成Token")

if __name__ == "__main__":
    print("=== Telegram Bot 完全重置工具 ===\n")
    asyncio.run(complete_reset())