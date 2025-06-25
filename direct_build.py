#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接调用PyInstaller的打包脚本
"""

import os
import sys
import traceback
from datetime import datetime

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")

def check_environment():
    """检查环境"""
    log("=== 检查环境 ===")
    
    # 检查Python版本
    version = sys.version_info
    log(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        log("❌ Python版本过低，需要3.6+", "ERROR")
        return False
    
    # 检查PyInstaller
    try:
        import PyInstaller
        log(f"✅ PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        log("❌ PyInstaller未安装", "ERROR")
        log("请运行: pip install pyinstaller")
        return False
    
    # 检查必要文件
    if not os.path.exists('qq_message_sender_web.py'):
        log("❌ 找不到 qq_message_sender_web.py", "ERROR")
        return False
    
    log("✅ 环境检查通过")
    return True

def create_templates_directory():
    """创建templates目录"""
    log("检查templates目录...")
    
    if not os.path.exists('templates'):
        log("创建templates目录...")
        try:
            os.makedirs('templates')
            log("✅ templates目录创建成功")
        except Exception as e:
            log(f"❌ 创建templates目录失败: {e}", "ERROR")
            return False
    else:
        log("✅ templates目录已存在")
    
    return True

def build_with_pyinstaller():
    """使用PyInstaller直接调用进行打包"""
    log("=== 开始打包 ===")
    
    try:
        import PyInstaller.__main__
        
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 根据操作系统选择正确的路径分隔符
        separator = ';' if sys.platform.startswith('win') else ':'
        
        # 构建参数列表
        args = [
            'qq_message_sender_web.py',  # 主程序文件
            '--name=QQ消息发送器',  # 生成的exe名称
            '--onefile',  # 打包成单个文件
            '--windowed',  # 使用窗口模式（不显示控制台）
            f'--add-data=templates{separator}templates',  # 添加模板文件夹
            '--clean',  # 清理临时文件
            '--noconfirm',  # 不询问确认
            '--log-level=INFO',  # 设置日志级别
        ]
        
        log(f"PyInstaller参数: {args}")
        log("开始调用PyInstaller...")
        
        # 直接调用PyInstaller
        PyInstaller.__main__.run(args)
        
        log("✅ PyInstaller调用完成")
        return True
        
    except ImportError as e:
        log(f"❌ 导入PyInstaller失败: {e}", "ERROR")
        return False
    except Exception as e:
        log(f"❌ PyInstaller调用异常: {e}", "ERROR")
        log(f"异常详情: {traceback.format_exc()}", "ERROR")
        return False

def check_output():
    """检查输出文件"""
    log("=== 检查输出文件 ===")
    
    exe_name = "QQ消息发送器.exe" if sys.platform.startswith('win') else "QQ消息发送器"
    exe_path = os.path.join('dist', exe_name)
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        log(f"✅ 找到exe文件: {exe_path}")
        log(f"文件大小: {size / (1024*1024):.2f} MB")
        return True
    else:
        log(f"❌ exe文件不存在: {exe_path}", "ERROR")
        return False

def cleanup_temp_files():
    """清理临时文件"""
    log("=== 清理临时文件 ===")
    
    temp_dirs = ['build', '__pycache__']
    temp_files = ['QQ消息发送器.spec']
    
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            try:
                import shutil
                shutil.rmtree(dir_name)
                log(f"✅ 已删除临时目录: {dir_name}")
            except Exception as e:
                log(f"⚠️ 删除临时目录失败: {dir_name} - {e}", "WARNING")
    
    for file_name in temp_files:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                log(f"✅ 已删除临时文件: {file_name}")
            except Exception as e:
                log(f"⚠️ 删除临时文件失败: {file_name} - {e}", "WARNING")

def main():
    """主函数"""
    log("=== QQ消息发送器 - 直接调用PyInstaller打包 ===")
    log(f"当前工作目录: {os.getcwd()}")
    log(f"Python可执行文件: {sys.executable}")
    log(f"操作系统: {sys.platform}")
    
    try:
        # 检查环境
        if not check_environment():
            return
        
        # 创建templates目录
        if not create_templates_directory():
            return
        
        # 打包
        if not build_with_pyinstaller():
            return
        
        # 检查输出
        if not check_output():
            return
        
        # 清理临时文件
        cleanup_temp_files()
        
        log("🎉 打包完成!")
        log("📁 生成文件: dist/QQ消息发送器.exe")
        log("使用方法:")
        log("1. 双击运行 dist/QQ消息发送器.exe")
        log("2. 在浏览器中访问 http://localhost:5000")
        
    except Exception as e:
        log(f"❌ 打包过程中发生异常: {e}", "ERROR")
        log(f"异常详情: {traceback.format_exc()}", "ERROR")
    
    finally:
        log("打包脚本执行完成")
        input("\n按回车键退出...")

if __name__ == "__main__":
    main() 