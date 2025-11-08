#!/usr/bin/env python3
"""
脚本用于清理Telegram Bot冲突问题
使用前请确保已安装aiogram: pip install aiogram
"""

import asyncio
import os
from aiogram import Bot

async def clear_webhook_and_get_info():
    """清除webhook并获取bot信息"""
    bot_token = input("请输入你的Bot Token: ").strip()

    if not bot_token:
        print("Token不能为空！")
        return

    try:
        bot = Bot(token=bot_token)

        # 获取bot信息
        bot_info = await bot.get_me()
        print(f"\n✅ Bot信息:")
        print(f"   用户名: @{bot_info.username}")
        print(f"   ID: {bot_info.id}")
        print(f"   名称: {bot_info.first_name}")

        # 获取当前webhook信息
        webhook_info = await bot.get_webhook_info()
        print(f"\n📋 当前Webhook信息:")
        print(f"   URL: {webhook_info.url or '未设置'}")
        print(f"   自定义证书: {webhook_info.custom_certificate or '无'}")
        print(f"   待处理更新数: {webhook_info.pending_update_count}")
        print(f"   最后错误日期: {webhook_info.last_error_date or '无'}")
        print(f"   最后错误信息: {webhook_info.last_error_message or '无'}")

        # 清除webhook
        print(f"\n🧹 正在清除Webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook已清除！")

        # 再次确认
        webhook_info_after = await bot.get_webhook_info()
        print(f"\n📋 清除后的Webhook信息:")
        print(f"   URL: {webhook_info_after.url or '未设置'}")
        print(f"   待处理更新数: {webhook_info_after.pending_update_count}")

        print(f"\n🎉 冲突已清理！现在可以重新部署机器人了。")
        print(f"   建议等待1-2分钟后再部署，确保Telegram服务器完全更新。")

    except Exception as e:
        print(f"❌ 错误: {e}")
        if "Conflict" in str(e):
            print(f"\n⚠️  仍然存在冲突！可能的原因:")
            print(f"   1. 有另一个机器人实例正在运行")
            print(f"   2. Token被其他服务使用")
            print(f"   3. 需要等待几分钟让Telegram服务器更新")
            print(f"\n💡 解决方案:")
            print(f"   1. 检查是否有本地进程在运行: ps aux | grep python")
            print(f"   2. 停止所有相关进程")
            print(f"   3. 重新生成Token (联系@BotFather使用/revoke)")
        else:
            print(f"   请检查Token是否正确")

if __name__ == "__main__":
    print("=== Telegram Bot 冲突清理工具 ===\n")
    asyncio.run(clear_webhook_and_get_info())