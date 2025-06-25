#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows平台QQ消息发送测试脚本
用于测试pyautogui在Windows下的功能
"""

import pyautogui
import time
import sys

def test_pyautogui():
    """测试pyautogui基本功能"""
    print("🧪 Windows平台pyautogui测试")
    print("=" * 50)
    
    # 设置pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    print("✅ pyautogui设置完成")
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    print(f"📱 屏幕尺寸: {screen_width} x {screen_height}")
    
    # 获取当前鼠标位置
    x, y = pyautogui.position()
    print(f"🖱️ 当前鼠标位置: ({x}, {y})")
    
    # 测试键盘输入
    print("\n⌨️ 测试键盘输入...")
    print("请在3秒内切换到记事本或其他文本编辑器")
    
    for i in range(3, 0, -1):
        print(f"倒计时: {i} 秒...")
        time.sleep(1)
    
    try:
        # 测试输入
        pyautogui.write("Hello Windows! 测试中文输入")
        print("✅ 键盘输入测试完成")
        
        # 测试快捷键
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        print("✅ 快捷键测试完成")
        
    except Exception as e:
        print(f"❌ 键盘测试失败: {e}")
    
    # 测试鼠标操作
    print("\n🖱️ 测试鼠标操作...")
    print("鼠标将在3秒后移动到屏幕中央")
    
    for i in range(3, 0, -1):
        print(f"倒计时: {i} 秒...")
        time.sleep(1)
    
    try:
        # 移动到屏幕中央
        center_x = screen_width // 2
        center_y = screen_height // 2
        pyautogui.moveTo(center_x, center_y, duration=1)
        print(f"✅ 鼠标移动到中央: ({center_x}, {center_y})")
        
        # 测试点击
        pyautogui.click()
        print("✅ 鼠标点击测试完成")
        
    except Exception as e:
        print(f"❌ 鼠标测试失败: {e}")
    
    print("\n🎉 测试完成！")
    print("如果所有测试都通过，说明pyautogui在Windows下工作正常")

def test_qq_simulation():
    """模拟QQ消息发送测试"""
    print("\n💬 QQ消息发送模拟测试")
    print("=" * 50)
    
    print("⚠️  请确保QQ窗口已打开并处于活动状态")
    print("⚠️  请确保光标在QQ输入框中")
    
    delay = int(input("请输入延迟时间（秒）: ") or "3")
    
    print(f"\n⏰ {delay}秒后开始测试...")
    for i in range(delay, 0, -1):
        print(f"倒计时: {i} 秒...")
        time.sleep(1)
    
    try:
        # 模拟自动选中输入框
        print("🔍 尝试自动选中输入框...")
        
        # 方法1: Tab键切换
        pyautogui.press('tab')
        time.sleep(0.3)
        
        # 方法2: Ctrl+A全选
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        
        # 方法3: Home键
        pyautogui.press('home')
        time.sleep(0.3)
        
        print("✅ 自动选中操作完成")
        
        # 输入测试消息
        test_message = "这是一条Windows平台测试消息 - " + time.strftime("%H:%M:%S")
        print(f"📝 输入测试消息: {test_message}")
        
        pyautogui.write(test_message)
        time.sleep(0.5)
        
        # 询问是否发送
        send = input("\n是否发送这条消息？(y/n): ").lower().strip()
        
        if send == 'y':
            pyautogui.press('enter')
            print("✅ 消息已发送")
        else:
            print("❌ 消息未发送")
            
    except Exception as e:
        print(f"❌ QQ模拟测试失败: {e}")

def main():
    """主函数"""
    print("🚀 Windows平台QQ消息发送器测试工具")
    print("=" * 60)
    
    while True:
        print("\n请选择测试项目:")
        print("1. 基础pyautogui功能测试")
        print("2. QQ消息发送模拟测试")
        print("3. 退出")
        
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == '1':
            test_pyautogui()
        elif choice == '2':
            test_qq_simulation()
        elif choice == '3':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        input("按回车键退出...") 