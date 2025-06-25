#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动选中输入框功能
"""

import pyautogui
import time
import platform
import sys

def test_auto_select():
    """测试自动选中功能"""
    print("=== 自动选中输入框测试 ===")
    print(f"操作系统: {platform.system()}")
    print(f"Python版本: {sys.version}")
    
    # 设置pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    print("\n请按照以下步骤操作：")
    print("1. 打开QQ并进入聊天窗口")
    print("2. 在输入框中输入一些测试文字")
    print("3. 确保QQ窗口处于活动状态")
    print("4. 按回车键开始测试")
    
    input("按回车键开始测试...")
    
    print("\n开始测试自动选中功能...")
    
    try:
        # 测试Windows下的自动选中方法
        if platform.system() == "Windows":
            print("使用Windows自动选中方法...")
            
            # 方法1: Tab键切换焦点
            print("1. 使用Tab键切换焦点...")
            pyautogui.press('tab')
            time.sleep(0.5)
            
            # 方法2: Ctrl+A全选
            print("2. 使用Ctrl+A全选...")
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            
            # 方法3: Home键移动到开头
            print("3. 使用Home键移动到开头...")
            pyautogui.press('home')
            time.sleep(0.5)
            
            # 方法4: End键移动到末尾
            print("4. 使用End键移动到末尾...")
            pyautogui.press('end')
            time.sleep(0.5)
            
            # 方法5: Ctrl+End移动到末尾，然后Ctrl+Shift+Home选中全部
            print("5. 使用Ctrl+End移动到末尾...")
            pyautogui.hotkey('ctrl', 'end')
            time.sleep(0.5)
            
            print("6. 使用Ctrl+Shift+Home选中全部...")
            pyautogui.hotkey('ctrl', 'shift', 'home')
            time.sleep(0.5)
            
        elif platform.system() == "Darwin":  # macOS
            print("使用macOS自动选中方法...")
            pyautogui.hotkey('cmd', 'a')  # 全选
            time.sleep(0.5)
            
        else:  # Linux
            print("使用Linux自动选中方法...")
            pyautogui.hotkey('ctrl', 'a')  # 全选
            time.sleep(0.5)
        
        print("\n✅ 自动选中测试完成！")
        print("请检查QQ输入框中的文字是否被选中")
        
        # 测试输入
        print("\n测试输入功能...")
        test_text = "这是自动选中测试"
        pyautogui.write(test_text)
        time.sleep(1)
        
        print(f"✅ 已输入测试文字: {test_text}")
        print("请检查QQ输入框中是否显示了测试文字")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

def test_tab_navigation():
    """测试Tab键导航"""
    print("\n=== Tab键导航测试 ===")
    print("这个测试会使用Tab键循环切换焦点")
    
    input("按回车键开始Tab导航测试...")
    
    try:
        for i in range(10):
            print(f"第 {i+1} 次Tab键...")
            pyautogui.press('tab')
            time.sleep(0.5)
            
            # 检查是否有输入框被激活
            # 这里可以添加更多的检测逻辑
            
    except Exception as e:
        print(f"❌ Tab导航测试失败: {e}")
        return False
    
    print("✅ Tab导航测试完成")
    return True

def test_coordinate_click():
    """测试坐标点击"""
    print("\n=== 坐标点击测试 ===")
    print("这个测试会点击屏幕中心位置")
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    print(f"屏幕尺寸: {screen_width}x{screen_height}")
    print(f"中心坐标: ({center_x}, {center_y})")
    
    input("按回车键点击屏幕中心...")
    
    try:
        pyautogui.click(center_x, center_y)
        print("✅ 已点击屏幕中心")
        
    except Exception as e:
        print(f"❌ 坐标点击失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 QQ消息发送器 - 自动选中功能测试")
    print("=" * 50)
    
    # 显示安全提示
    print("⚠️  安全提示:")
    print("- 测试过程中请保持QQ窗口可见")
    print("- 如需紧急停止，请将鼠标移动到屏幕左上角")
    print("- 测试可能会影响当前输入框的内容")
    print()
    
    # 运行测试
    tests = [
        ("自动选中测试", test_auto_select),
        ("Tab导航测试", test_tab_navigation),
        ("坐标点击测试", test_coordinate_click)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print(f"\n❌ {test_name} 被用户中断")
            results.append((test_name, False))
            break
        except Exception as e:
            print(f"\n❌ {test_name} 发生异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print(f"\n{'='*20} 测试结果 {'='*20}")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n{'='*20} 总结 {'='*20}")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"总测试数: {total}")
    print(f"通过测试: {passed}")
    print(f"失败测试: {total - passed}")
    
    if passed == total:
        print("🎉 所有测试通过！自动选中功能应该可以正常工作")
    else:
        print("⚠️  部分测试失败，可能需要手动调整")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main() 