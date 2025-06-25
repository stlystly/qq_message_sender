#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ消息发送脚本安装程序
"""

import subprocess
import sys
import platform
import os

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("错误: 需要Python 3.6或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("正在安装依赖包...")
    
    try:
        # 升级pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # 安装依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("依赖包安装成功！")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"安装依赖包失败: {e}")
        return False

def show_mac_permissions():
    """显示Mac权限设置说明"""
    if platform.system() == "Darwin":
        print("\n=== macOS权限设置 ===")
        print("请在系统偏好设置中授予脚本辅助功能权限:")
        print("1. 打开 系统偏好设置")
        print("2. 点击 安全性与隐私")
        print("3. 选择 隐私 标签")
        print("4. 在左侧列表中选择 辅助功能")
        print("5. 点击左下角的锁图标解锁")
        print("6. 添加Python或终端应用到列表中")
        print("7. 勾选相应的应用")
        print()

def show_usage_examples():
    """显示使用示例"""
    print("\n=== 使用示例 ===")
    print("1. 运行完整版脚本:")
    print("   python qq_message_sender.py")
    print()
    print("2. 运行快速发送脚本:")
    print("   python quick_send.py '你好，这是一条测试消息'")
    print()
    print("3. 交互式发送:")
    print("   python quick_send.py")
    print()

def main():
    """主安装函数"""
    print("=== QQ消息发送脚本安装程序 ===")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print()
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 安装依赖
    if not install_dependencies():
        print("安装失败，请检查网络连接或手动安装依赖包")
        return
    
    # 显示系统特定说明
    show_mac_permissions()
    
    # 显示使用示例
    show_usage_examples()
    
    print("安装完成！")
    print("请确保QQ已打开并处于活动状态后再运行脚本。")

if __name__ == "__main__":
    main() 