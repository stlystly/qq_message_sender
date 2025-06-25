#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows平台窗口管理技术调研
测试各种获取和切换窗口的方法
"""

import time
import sys
import platform

def test_pyautogui_windows():
    """测试pyautogui的窗口功能"""
    print("🔍 测试pyautogui窗口功能")
    print("=" * 50)
    
    try:
        import pyautogui
        
        # 检查pyautogui版本
        print(f"pyautogui版本: {pyautogui.__version__}")
        
        # 测试getWindowsWithTitle方法
        print("\n1. 测试getWindowsWithTitle方法:")
        try:
            # 查找所有包含"QQ"的窗口
            qq_windows = pyautogui.getWindowsWithTitle("QQ")
            print(f"   找到 {len(qq_windows)} 个QQ相关窗口:")
            for i, window in enumerate(qq_windows):
                print(f"   {i+1}. 标题: {window.title}")
                print(f"      位置: ({window.left}, {window.top})")
                print(f"      大小: {window.width} x {window.height}")
                print(f"      是否激活: {window.isActive}")
                print(f"      是否最小化: {window.isMinimized}")
                print(f"      是否最大化: {window.isMaximized}")
        except AttributeError:
            print("   ❌ getWindowsWithTitle方法不可用")
        except Exception as e:
            print(f"   ❌ getWindowsWithTitle方法出错: {e}")
        
        # 测试getActiveWindow方法
        print("\n2. 测试getActiveWindow方法:")
        try:
            active_window = pyautogui.getActiveWindow()
            if active_window:
                print(f"   当前活动窗口: {active_window.title}")
                print(f"   位置: ({active_window.left}, {active_window.top})")
                print(f"   大小: {active_window.width} x {active_window.height}")
            else:
                print("   ❌ 没有活动窗口")
        except AttributeError:
            print("   ❌ getActiveWindow方法不可用")
        except Exception as e:
            print(f"   ❌ getActiveWindow方法出错: {e}")
        
        # 测试getAllWindows方法
        print("\n3. 测试getAllWindows方法:")
        try:
            all_windows = pyautogui.getAllWindows()
            print(f"   找到 {len(all_windows)} 个窗口")
            
            # 显示前10个窗口
            for i, window in enumerate(all_windows[:10]):
                print(f"   {i+1}. {window.title[:50]}...")
        except AttributeError:
            print("   ❌ getAllWindows方法不可用")
        except Exception as e:
            print(f"   ❌ getAllWindows方法出错: {e}")
        
        # 测试窗口激活
        print("\n4. 测试窗口激活:")
        try:
            qq_windows = pyautogui.getWindowsWithTitle("QQ")
            if qq_windows:
                print(f"   尝试激活第一个QQ窗口: {qq_windows[0].title}")
                qq_windows[0].activate()
                time.sleep(1)
                print("   ✅ 窗口激活成功")
            else:
                print("   ⚠️  未找到QQ窗口，无法测试激活")
        except Exception as e:
            print(f"   ❌ 窗口激活失败: {e}")
            
    except ImportError:
        print("❌ pyautogui未安装")

def test_win32gui():
    """测试win32gui模块"""
    print("\n🔍 测试win32gui模块")
    print("=" * 50)
    
    try:
        import win32gui
        import win32con
        import win32process
        
        print("✅ win32gui模块可用")
        
        # 获取前台窗口
        print("\n1. 获取前台窗口:")
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_text = win32gui.GetWindowText(hwnd)
            print(f"   前台窗口句柄: {hwnd}")
            print(f"   窗口标题: {window_text}")
            
            # 获取窗口类名
            class_name = win32gui.GetClassName(hwnd)
            print(f"   窗口类名: {class_name}")
            
            # 获取窗口位置和大小
            rect = win32gui.GetWindowRect(hwnd)
            print(f"   窗口位置: {rect}")
            
            # 获取进程ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            print(f"   进程ID: {pid}")
            
        except Exception as e:
            print(f"   ❌ 获取前台窗口失败: {e}")
        
        # 枚举所有窗口
        print("\n2. 枚举所有窗口:")
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text:  # 只显示有标题的窗口
                        windows.append((hwnd, window_text))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            print(f"   找到 {len(windows)} 个可见窗口")
            
            # 显示包含"QQ"的窗口
            qq_windows = [(hwnd, title) for hwnd, title in windows if "QQ" in title]
            print(f"   其中包含QQ的窗口: {len(qq_windows)} 个")
            
            for i, (hwnd, title) in enumerate(qq_windows[:5]):  # 只显示前5个
                print(f"   {i+1}. {title}")
                
        except Exception as e:
            print(f"   ❌ 枚举窗口失败: {e}")
        
        # 测试窗口切换
        print("\n3. 测试窗口切换:")
        try:
            qq_windows = [(hwnd, title) for hwnd, title in windows if "QQ" in title]
            if qq_windows:
                target_hwnd, target_title = qq_windows[0]
                print(f"   尝试切换到: {target_title}")
                
                # 激活窗口
                win32gui.ShowWindow(target_hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(target_hwnd)
                
                time.sleep(1)
                print("   ✅ 窗口切换成功")
            else:
                print("   ⚠️  未找到QQ窗口，无法测试切换")
                
        except Exception as e:
            print(f"   ❌ 窗口切换失败: {e}")
            
    except ImportError:
        print("❌ win32gui模块未安装")
        print("   安装命令: pip install pywin32")

def test_psutil():
    """测试psutil模块获取进程信息"""
    print("\n🔍 测试psutil模块")
    print("=" * 50)
    
    try:
        import psutil
        
        print("✅ psutil模块可用")
        
        # 获取当前活动进程
        print("\n1. 获取当前活动进程:")
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] and 'qq' in proc.info['name'].lower():
                    print(f"   QQ进程: {proc.info['name']} (PID: {proc.info['pid']})")
                    print(f"   路径: {proc.info['exe']}")
        except Exception as e:
            print(f"   ❌ 获取进程信息失败: {e}")
        
        # 获取系统进程列表
        print("\n2. 获取系统进程列表:")
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name']:
                    processes.append(proc.info)
            
            print(f"   系统总进程数: {len(processes)}")
            
            # 查找QQ相关进程
            qq_processes = [p for p in processes if 'qq' in p['name'].lower()]
            print(f"   QQ相关进程数: {len(qq_processes)}")
            
            for proc in qq_processes:
                print(f"   - {proc['name']} (PID: {proc['pid']})")
                
        except Exception as e:
            print(f"   ❌ 获取进程列表失败: {e}")
            
    except ImportError:
        print("❌ psutil模块未安装")
        print("   安装命令: pip install psutil")

def test_pywinauto():
    """测试pywinauto模块"""
    print("\n🔍 测试pywinauto模块")
    print("=" * 50)
    
    try:
        from pywinauto import Application, Desktop
        
        print("✅ pywinauto模块可用")
        
        # 连接到已运行的QQ
        print("\n1. 尝试连接到QQ进程:")
        try:
            # 查找QQ进程
            qq_apps = []
            for app in Application().connect(title_re=".*QQ.*"):
                qq_apps.append(app)
            
            print(f"   找到 {len(qq_apps)} 个QQ应用")
            
            for i, app in enumerate(qq_apps):
                print(f"   {i+1}. 主窗口: {app.window().window_text()}")
                
                # 获取子窗口
                try:
                    children = app.window().children()
                    print(f"      子窗口数: {len(children)}")
                    
                    # 显示前几个子窗口
                    for j, child in enumerate(children[:3]):
                        print(f"         {j+1}. {child.window_text()}")
                        
                except Exception as e:
                    print(f"      获取子窗口失败: {e}")
                    
        except Exception as e:
            print(f"   ❌ 连接QQ进程失败: {e}")
        
        # 获取桌面窗口
        print("\n2. 获取桌面窗口:")
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            
            print(f"   桌面窗口数: {len(windows)}")
            
            # 查找QQ相关窗口
            qq_windows = [w for w in windows if 'QQ' in w.window_text()]
            print(f"   QQ相关窗口数: {len(qq_windows)}")
            
            for i, window in enumerate(qq_windows[:3]):
                print(f"   {i+1}. {window.window_text()}")
                
        except Exception as e:
            print(f"   ❌ 获取桌面窗口失败: {e}")
            
    except ImportError:
        print("❌ pywinauto模块未安装")
        print("   安装命令: pip install pywinauto")

def test_alternatives():
    """测试其他替代方案"""
    print("\n🔍 测试其他替代方案")
    print("=" * 50)
    
    # 测试subprocess调用Windows命令
    print("\n1. 测试subprocess调用Windows命令:")
    try:
        import subprocess
        
        # 使用tasklist命令获取进程
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq QQ.exe'], 
                              capture_output=True, text=True, encoding='gbk')
        
        if result.returncode == 0:
            print("   ✅ tasklist命令执行成功")
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # 有进程信息
                print("   QQ进程信息:")
                for line in lines[1:]:  # 跳过标题行
                    if line.strip():
                        print(f"     {line}")
            else:
                print("   ⚠️  未找到QQ进程")
        else:
            print("   ❌ tasklist命令执行失败")
            
    except Exception as e:
        print(f"   ❌ subprocess测试失败: {e}")
    
    # 测试ctypes调用Windows API
    print("\n2. 测试ctypes调用Windows API:")
    try:
        import ctypes
        from ctypes import wintypes
        
        # 定义Windows API函数
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        
        # 获取前台窗口
        hwnd = user32.GetForegroundWindow()
        print(f"   前台窗口句柄: {hwnd}")
        
        # 获取窗口标题
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            print(f"   窗口标题: {buffer.value}")
        
        # 获取窗口类名
        buffer = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, buffer, 256)
        print(f"   窗口类名: {buffer.value}")
        
        print("   ✅ ctypes Windows API调用成功")
        
    except Exception as e:
        print(f"   ❌ ctypes测试失败: {e}")

def main():
    """主函数"""
    print("🚀 Windows平台窗口管理技术调研")
    print("=" * 60)
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    print("=" * 60)
    
    # 运行各种测试
    tests = [
        ("pyautogui窗口功能", test_pyautogui_windows),
        ("win32gui模块", test_win32gui),
        ("psutil模块", test_psutil),
        ("pywinauto模块", test_pywinauto),
        ("其他替代方案", test_alternatives)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
            results.append((test_name, True))
        except KeyboardInterrupt:
            print(f"\n❌ {test_name} 被用户中断")
            results.append((test_name, False))
            break
        except Exception as e:
            print(f"\n❌ {test_name} 发生异常: {e}")
            results.append((test_name, False))
    
    # 显示调研结果
    print(f"\n{'='*20} 调研结果总结 {'='*20}")
    for test_name, result in results:
        status = "✅ 可用" if result else "❌ 不可用"
        print(f"{test_name}: {status}")
    
    print(f"\n{'='*20} 推荐方案 {'='*20}")
    print("1. pyautogui: 简单易用，适合基础窗口操作")
    print("2. win32gui: 功能强大，适合复杂窗口管理")
    print("3. pywinauto: 现代化API，适合UI自动化")
    print("4. psutil: 适合进程管理")
    print("5. ctypes: 底层控制，适合高级用户")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        input("按回车键退出...") 