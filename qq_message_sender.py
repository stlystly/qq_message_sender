#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ消息发送脚本 - 兼容Mac和Windows
使用pyautogui实现跨平台自动化操作
"""

import pyautogui
import time
import sys
import os
import platform
from typing import Optional, List

class QQMessageSender:
    def __init__(self):
        """初始化QQ消息发送器"""
        self.system = platform.system()
        self.setup_pyautogui()
        
    def setup_pyautogui(self):
        """根据操作系统设置pyautogui"""
        # 设置安全边界，防止鼠标移动到屏幕边缘
        pyautogui.FAILSAFE = True
        
        # 设置操作间隔，避免操作过快
        pyautogui.PAUSE = 0.5
        
        if self.system == "Darwin":  # macOS
            # macOS可能需要特殊权限
            print("检测到macOS系统")
        elif self.system == "Windows":
            print("检测到Windows系统")
        else:
            print(f"检测到未知系统: {self.system}")
    
    def find_qq_window(self) -> bool:
        """
        查找QQ窗口
        返回: 是否找到QQ窗口
        """
        try:
            # 尝试查找QQ窗口
            if self.system == "Darwin":
                # macOS使用更通用的方法
                print("macOS系统：请手动确保QQ窗口处于活动状态")
                return True
            else:
                # Windows使用窗口标题搜索
                try:
                    qq_windows = pyautogui.getWindowsWithTitle("QQ")
                    if qq_windows:
                        qq_windows[0].activate()
                        return True
                except AttributeError:
                    # 如果getWindowsWithTitle不存在，使用备用方法
                    print("Windows系统：请手动确保QQ窗口处于活动状态")
                    return True
            
            print("未找到QQ窗口，请确保QQ已打开并处于活动状态")
            return False
            
        except Exception as e:
            print(f"查找QQ窗口时出错: {e}")
            print("请手动确保QQ窗口处于活动状态")
            return True  # 返回True让用户手动处理
    
    def send_message(self, message: str, contact_name: Optional[str] = None):
        """
        发送消息到QQ
        
        Args:
            message: 要发送的消息内容
            contact_name: 联系人名称（可选，如果不提供则发送到当前聊天窗口）
        """
        try:
            # 确保QQ窗口处于活动状态
            if not self.find_qq_window():
                print("请先打开QQ并确保窗口处于活动状态")
                return False
            
            # 等待一下确保窗口激活
            time.sleep(1)
            
            # 如果需要指定联系人
            if contact_name:
                self._search_contact(contact_name)
            
            # 输入消息
            self._type_message(message)
            
            # 发送消息
            self._send_message()
            
            print(f"消息已发送: {message}")
            return True
            
        except Exception as e:
            print(f"发送消息时出错: {e}")
            return False
    
    def _search_contact(self, contact_name: str):
        """搜索联系人"""
        try:
            # 使用快捷键打开搜索
            if self.system == "Darwin":
                pyautogui.hotkey('cmd', 'f')
            else:
                pyautogui.hotkey('ctrl', 'f')
            
            time.sleep(0.5)
            
            # 输入联系人名称
            pyautogui.write(contact_name)
            time.sleep(1)
            
            # 按回车选择第一个结果
            pyautogui.press('enter')
            time.sleep(1)
            
        except Exception as e:
            print(f"搜索联系人时出错: {e}")
    
    def _type_message(self, message: str):
        """输入消息内容"""
        try:
            # 确保焦点在输入框
            pyautogui.click()
            time.sleep(0.5)
            
            # 输入消息
            pyautogui.write(message)
            time.sleep(0.5)
            
        except Exception as e:
            print(f"输入消息时出错: {e}")
    
    def _send_message(self):
        """发送消息"""
        try:
            # 按回车发送消息
            pyautogui.press('enter')
            
        except Exception as e:
            print(f"发送消息时出错: {e}")
    
    def send_multiple_messages(self, messages: List[str], contact_name: Optional[str] = None):
        """
        发送多条消息
        
        Args:
            messages: 消息列表
            contact_name: 联系人名称（可选）
        """
        print(f"准备发送 {len(messages)} 条消息...")
        
        for i, message in enumerate(messages, 1):
            print(f"正在发送第 {i} 条消息...")
            success = self.send_message(message, contact_name)
            
            if not success:
                print(f"第 {i} 条消息发送失败")
                break
            
            # 消息间隔
            if i < len(messages):
                time.sleep(2)
        
        print("批量发送完成")

def main():
    """主函数"""
    print("=== QQ消息发送脚本 ===")
    print("兼容Mac和Windows系统")
    print("请确保QQ已打开并处于活动状态")
    print()
    
    # 创建发送器实例
    sender = QQMessageSender()
    
    while True:
        print("\n请选择操作:")
        print("1. 发送单条消息")
        print("2. 发送多条消息")
        print("3. 退出")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == "1":
            message = input("请输入要发送的消息: ").strip()
            if message:
                contact = input("请输入联系人名称（直接回车发送到当前聊天窗口）: ").strip()
                contact = contact if contact else None
                sender.send_message(message, contact)
            else:
                print("消息不能为空")
        
        elif choice == "2":
            messages = []
            print("请输入要发送的消息（输入空行结束）:")
            while True:
                msg = input(f"消息 {len(messages) + 1}: ").strip()
                if not msg:
                    break
                messages.append(msg)
            
            if messages:
                contact = input("请输入联系人名称（直接回车发送到当前聊天窗口）: ").strip()
                contact = contact if contact else None
                sender.send_multiple_messages(messages, contact)
            else:
                print("没有输入任何消息")
        
        elif choice == "3":
            print("退出程序")
            break
        
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 