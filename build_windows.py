#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows平台QQ消息发送器打包脚本
使用PyInstaller将Web版本打包成exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("📦 正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller安装失败: {e}")
        return False

def clean_build():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    # 要清理的目录和文件
    cleanup_items = [
        'build',
        'dist',
        '*.spec',
        '__pycache__',
        'templates/__pycache__'
    ]
    
    for item in cleanup_items:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
            print(f"✅ 已删除: {item}")

def build_exe():
    """构建exe文件"""
    print("🔨 开始构建exe文件...")
    
    # PyInstaller命令参数
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 无控制台窗口
        "--name=QQ消息发送器",          # 可执行文件名称
        "--icon=icon.ico",              # 图标文件（如果存在）
        "--add-data=templates;templates",  # 包含模板文件
        "--hidden-import=flask",
        "--hidden-import=werkzeug",
        "--hidden-import=jinja2",
        "qq_message_sender_web.py"      # 主脚本
    ]
    
    # 如果没有图标文件，移除图标参数
    if not os.path.exists("icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
        print("⚠️  未找到icon.ico文件，将使用默认图标")
    
    try:
        print("🚀 执行PyInstaller命令...")
        print(f"命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 构建成功！")
            print("📁 可执行文件位置: dist/QQ消息发送器.exe")
            return True
        else:
            print("❌ 构建失败")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中出错: {e}")
        return False

def create_icon():
    """创建简单的图标文件（如果不存在）"""
    if os.path.exists("icon.ico"):
        print("✅ 图标文件已存在")
        return
    
    print("🎨 创建默认图标文件...")
    
    # 这里可以添加创建图标的代码
    # 由于创建图标比较复杂，我们暂时跳过
    print("⚠️  跳过图标创建，将使用默认图标")

def create_readme():
    """创建说明文件"""
    readme_content = """# QQ消息发送器 - Windows版本

## 使用说明

1. 双击运行 `QQ消息发送器.exe`
2. 在浏览器中访问 `http://localhost:5000`
3. 确保QQ窗口处于活动状态
4. 在Web界面中设置消息内容和发送参数
5. 点击发送按钮开始发送消息

## 注意事项

- 请确保QQ窗口已打开并处于活动状态
- 建议使用自动选中输入框模式
- 发送前请仔细检查消息内容
- 如遇问题，请检查防火墙设置

## 系统要求

- Windows 7/8/10/11
- 已安装QQ客户端
- 网络连接正常

## 技术支持

如有问题，请检查：
1. QQ是否正常运行
2. 防火墙是否阻止程序
3. 端口5000是否被占用
"""
    
    with open("README_Windows.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ 说明文件已创建: README_Windows.txt")

def main():
    """主函数"""
    print("🚀 Windows平台QQ消息发送器打包工具")
    print("=" * 60)
    
    # 检查当前目录
    if not os.path.exists("qq_message_sender_web.py"):
        print("❌ 未找到主脚本文件 qq_message_sender_web.py")
        print("请确保在正确的目录中运行此脚本")
        input("按回车键退出...")
        return
    
    # 检查PyInstaller
    if not check_pyinstaller():
        install_choice = input("是否安装PyInstaller？(y/n): ").lower().strip()
        if install_choice == 'y':
            if not install_pyinstaller():
                input("按回车键退出...")
                return
        else:
            print("❌ 需要PyInstaller才能继续")
            input("按回车键退出...")
            return
    
    # 清理构建文件
    clean_build()
    
    # 创建图标
    create_icon()
    
    # 构建exe
    if build_exe():
        # 创建说明文件
        create_readme()
        
        print("\n🎉 打包完成！")
        print("=" * 60)
        print("📁 生成的文件:")
        print("  - dist/QQ消息发送器.exe (主程序)")
        print("  - README_Windows.txt (使用说明)")
        print("\n💡 使用提示:")
        print("  1. 将exe文件复制到任意位置即可使用")
        print("  2. 首次运行可能需要几秒钟启动")
        print("  3. 如果被杀毒软件误报，请添加信任")
    else:
        print("\n❌ 打包失败，请检查错误信息")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        input("按回车键退出...") 