#!/usr/bin/env python3
"""
检查是否有其他机器人实例在运行
"""

import subprocess
import os
import psutil

def check_running_processes():
    """检查运行中的Python进程"""
    print("🔍 检查运行中的Python进程...")

    # 方法1: 使用psutil
    try:
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any('python' in str(cmd) for cmd in cmdline):
                    if any('bot' in str(cmd).lower() for cmd in cmdline):
                        python_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if python_processes:
            print(f"⚠️ 发现 {len(python_processes)} 个可能的机器人进程:")
            for proc in python_processes:
                print(f"   PID: {proc['pid']}, 命令: {' '.join(proc['cmdline'])}")
        else:
            print("✅ 未发现本地机器人进程")

    except ImportError:
        print("⚠️ psutil未安装，使用基础检查...")

    # 方法2: 使用系统命令
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            if 'python.exe' in result.stdout.lower():
                print("⚠️ 发现Windows上的Python进程")
            else:
                print("✅ Windows上未发现Python进程")
        else:  # Linux/Mac
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            bot_lines = [line for line in result.stdout.split('\n') if 'bot' in line.lower() and 'python' in line.lower()]
            if bot_lines:
                print(f"⚠️ 发现 {len(bot_lines)} 个机器人进程:")
                for line in bot_lines:
                    print(f"   {line}")
            else:
                print("✅ 未发现机器人进程")

    except Exception as e:
        print(f"❌ 进程检查失败: {e}")

def check_environment():
    """检查环境变量"""
    print("\n🔧 检查环境变量...")
    bot_token = os.getenv("BOT_TOKEN")
    if bot_token:
        print(f"✅ BOT_TOKEN已设置: {bot_token[:20]}...")
    else:
        print("❌ BOT_TOKEN未设置")

def check_railway_status():
    """检查Railway状态（如果可能）"""
    print("\n🚂 检查Railway相关...")
    railway_token = os.getenv("RAILWAY_TOKEN")
    if railway_token:
        print("✅ 检测到Railway Token")
    else:
        print("ℹ️ 未检测到Railway Token（正常）")

def main():
    print("=== 机器人实例检查工具 ===\n")

    check_running_processes()
    check_environment()
    check_railway_status()

    print(f"\n📋 检查完成！")
    print(f"\n💡 如果发现其他机器人进程:")
    print(f"1. 在Windows: taskkill /PID <进程ID>")
    print(f"2. 在Linux/Mac: kill <进程ID>")
    print(f"3. 或者停止相关应用程序")

if __name__ == "__main__":
    main()