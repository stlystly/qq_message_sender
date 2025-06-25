#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试pyautogui功能的脚本
"""

import pyautogui
import platform
import sys

def test_pyautogui_functions():
    """测试pyautogui的可用功能"""
    print("=== pyautogui功能测试 ===")
    print(f"pyautogui版本: {pyautogui.__version__}")
    print(f"操作系统: {platform.system()}")
    print()
    
    # 测试基本功能
    print("1. 测试基本功能:")
    try:
        screen_size = pyautogui.size()
        print(f"   屏幕尺寸: {screen_size}")
    except Exception as e:
        print(f"   获取屏幕尺寸失败: {e}")
    
    try:
        mouse_pos = pyautogui.position()
        print(f"   鼠标位置: {mouse_pos}")
    except Exception as e:
        print(f"   获取鼠标位置失败: {e}")
    
    # 测试窗口相关功能
    print("\n2. 测试窗口功能:")
    
    # 检查getWindowsWithTitle方法
    try:
        windows = pyautogui.getWindowsWithTitle("")
        print(f"   getWindowsWithTitle方法可用，找到 {len(windows)} 个窗口")
    except AttributeError:
        print("   getWindowsWithTitle方法不可用")
    except Exception as e:
        print(f"   getWindowsWithTitle方法出错: {e}")
    
    # 检查getActiveWindow方法
    try:
        active_window = pyautogui.getActiveWindow()
        if active_window:
            print(f"   getActiveWindow方法可用，当前活动窗口: {active_window.title}")
        else:
            print("   getActiveWindow方法可用，但没有活动窗口")
    except AttributeError:
        print("   getActiveWindow方法不可用")
    except Exception as e:
        print(f"   getActiveWindow方法出错: {e}")
    
    # 检查其他可能的方法
    print("\n3. 检查其他方法:")
    methods_to_check = [
        'getAllWindows',
        'getWindowsAt',
        'getWindow',
        'window'
    ]
    
    for method in methods_to_check:
        try:
            if hasattr(pyautogui, method):
                print(f"   {method} 方法存在")
            else:
                print(f"   {method} 方法不存在")
        except Exception as e:
            print(f"   检查 {method} 方法时出错: {e}")
    
    print("\n4. 测试键盘输入功能:")
    try:
        print("   测试键盘输入功能...")
        # 这里不实际输入，只是测试方法是否存在
        if hasattr(pyautogui, 'write'):
            print("   write方法可用")
        if hasattr(pyautogui, 'press'):
            print("   press方法可用")
        if hasattr(pyautogui, 'hotkey'):
            print("   hotkey方法可用")
    except Exception as e:
        print(f"   测试键盘功能时出错: {e}")
    
    print("\n=== 测试完成 ===")

def show_usage_suggestions():
    """显示使用建议"""
    print("\n=== 使用建议 ===")
    print("基于测试结果，建议使用以下方法:")
    print("1. 使用 pyautogui.write() 输入文本")
    print("2. 使用 pyautogui.press('enter') 发送消息")
    print("3. 使用 pyautogui.hotkey() 组合键")
    print("4. 手动确保QQ窗口处于活动状态")
    print("5. 使用倒计时给用户时间切换到QQ窗口")

if __name__ == "__main__":
    test_pyautogui_functions()
    show_usage_suggestions() 