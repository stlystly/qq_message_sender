#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ快速发送脚本 - 简化版本
"""

import pyautogui
import time
import sys
import platform

def check_system():
    """检查系统并显示相应提示"""
    system = platform.system()
    print(f"检测到系统: {system}")
    
    if system == "Darwin":
        print("macOS提示：请确保已在系统偏好设置中授予辅助功能权限")
    elif system == "Windows":
        print("Windows提示：请确保QQ窗口处于活动状态")
    else:
        print(f"未知系统: {system}")

def quick_send(message, delay=3):
    """
    快速发送消息到QQ
    
    Args:
        message: 要发送的消息
        delay: 延迟时间（秒），给用户时间切换到QQ窗口
    """
    print(f"将在 {delay} 秒后发送消息: {message}")
    print("请确保QQ窗口处于活动状态，光标在输入框中")
    print("提示：将鼠标移动到屏幕左上角可紧急停止脚本")
    
    # 倒计时
    for i in range(delay, 0, -1):
        print(f"倒计时: {i} 秒...")
        time.sleep(1)
    
    try:
        # 输入消息
        pyautogui.write(message)
        time.sleep(0.5)
        
        # 发送消息
        pyautogui.press('enter')
        
        print("消息发送成功！")
        
    except Exception as e:
        print(f"发送失败: {e}")
        print("请检查QQ窗口是否处于活动状态")

def main():
    """主函数"""
    # 设置pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    print("=== QQ快速发送脚本 ===")
    check_system()
    print("使用方法: python quick_send.py '消息内容'")
    print("或者直接运行脚本，然后输入消息")
    print()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        message = sys.argv[1]
        quick_send(message)
    else:
        # 交互式输入
        message = input("请输入要发送的消息: ").strip()
        if message:
            delay_input = input("请输入延迟时间（秒，默认3秒）: ").strip()
            try:
                delay = int(delay_input) if delay_input else 3
            except ValueError:
                delay = 3
            
            quick_send(message, delay)
        else:
            print("消息不能为空")

if __name__ == "__main__":
    main() 