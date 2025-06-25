#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ消息发送脚本 - Web界面版本
使用Flask创建Web界面, 支持跨平台访问
"""

from flask import Flask, render_template, request, jsonify, session
import pyautogui
import time
import threading
import platform
import json
import os
from datetime import datetime
from typing import Optional, List

app = Flask(__name__)
app.secret_key = 'qq_message_sender_secret_key'

class QQMessageSender:
    def __init__(self):
        self.system = platform.system()
        self.setup_pyautogui()
        self.sending = False
        self.current_task = None
        
    def setup_pyautogui(self):
        """设置pyautogui"""
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
    def send_messages(self, messages: List[str], contact: Optional[str] = None, 
                     delay: int = 3, interval: int = 2, callback=None):
        """发送消息"""
        if self.sending:
            return False
            
        self.sending = True
        
        def send_thread():
            try:
                if callback:
                    callback(f"准备发送 {len(messages)} 条消息...")
                    callback(f"请在 {delay} 秒内切换到QQ窗口并确保光标在输入框中")
                
                # 倒计时
                for i in range(delay, 0, -1):
                    if not self.sending:
                        break
                    if callback:
                        callback(f"倒计时: {i} 秒...")
                    time.sleep(1)
                    
                if not self.sending:
                    if callback:
                        callback("发送已取消")
                    return
                    
                # 发送消息
                for i, message in enumerate(messages, 1):
                    if not self.sending:
                        break
                        
                    if callback:
                        callback(f"正在发送第 {i}/{len(messages)} 条消息: {message[:30]}...")
                    
                    try:
                        # 输入消息
                        pyautogui.write(message)
                        time.sleep(0.5)
                        
                        # 发送消息
                        pyautogui.press('enter')
                        
                        if callback:
                            callback(f"第 {i} 条消息发送成功")
                        
                        # 消息间隔
                        if i < len(messages) and self.sending:
                            time.sleep(interval)
                            
                    except Exception as e:
                        if callback:
                            callback(f"第 {i} 条消息发送失败: {e}")
                        break
                        
                if self.sending:
                    if callback:
                        callback("所有消息发送完成")
                else:
                    if callback:
                        callback("发送已停止")
                    
            except Exception as e:
                if callback:
                    callback(f"发送过程中出错: {e}")
            finally:
                self.sending = False
                
        # 启动发送线程
        thread = threading.Thread(target=send_thread)
        thread.daemon = True
        thread.start()
        return True
        
    def stop_sending(self):
        """停止发送"""
        self.sending = False

# 创建全局发送器实例
sender = QQMessageSender()

# 存储日志的全局变量
message_logs = []

def add_log(message):
    """添加日志"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'message': message,
        'type': 'info'
    }
    message_logs.append(log_entry)
    # 保持日志数量在合理范围内
    if len(message_logs) > 100:
        message_logs.pop(0)

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/send', methods=['POST'])
def send_messages():
    """发送消息API"""
    try:
        data = request.get_json()
        
        # 获取参数
        message_type = data.get('message_type', 'single')
        contact = data.get('contact', '').strip() or None
        delay = int(data.get('delay', 3))
        interval = int(data.get('interval', 2))
        
        # 获取消息
        messages = []
        if message_type == 'single':
            message = data.get('single_message', '').strip()
            if not message:
                return jsonify({'success': False, 'message': '请输入要发送的消息'})
            messages = [message]
        else:
            multiple_messages = data.get('multiple_messages', '').strip()
            if not multiple_messages:
                return jsonify({'success': False, 'message': '请输入要发送的消息'})
            messages = [line.strip() for line in multiple_messages.split('\n') if line.strip()]
        
        # 清空日志
        message_logs.clear()
        
        # 开始发送
        success = sender.send_messages(messages, contact, delay, interval, add_log)
        
        if success:
            return jsonify({'success': True, 'message': '开始发送消息'})
        else:
            return jsonify({'success': False, 'message': '发送器正在运行中'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'发送失败: {e}'})

@app.route('/api/stop', methods=['POST'])
def stop_sending():
    """停止发送API"""
    try:
        sender.stop_sending()
        add_log("正在停止发送...")
        return jsonify({'success': True, 'message': '已停止发送'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'停止失败: {e}'})

@app.route('/api/logs')
def get_logs():
    """获取日志API"""
    return jsonify({'logs': message_logs})

@app.route('/api/status')
def get_status():
    """获取状态API"""
    return jsonify({
        'sending': sender.sending,
        'system': sender.system
    })

def create_templates():
    """创建模板目录和文件"""
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    # 创建HTML模板
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QQ消息发送器 - Web版本</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.8;
            font-size: 1.1em;
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 30px;
        }
        
        .panel {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border: 1px solid #e9ecef;
        }
        
        .panel h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.3em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .form-control:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .radio-group {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .radio-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .radio-item input[type="radio"] {
            transform: scale(1.2);
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-right: 10px;
        }
        
        .btn-primary {
            background: #3498db;
            color: white;
        }
        
        .btn-primary:hover {
            background: #2980b9;
        }
        
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c0392b;
        }
        
        .btn-secondary {
            background: #95a5a6;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #7f8c8d;
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .settings-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .log-container {
            background: #2c3e50;
            color: #ecf0f1;
            border-radius: 8px;
            padding: 15px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
        }
        
        .log-entry {
            margin-bottom: 5px;
            padding: 2px 0;
        }
        
        .log-timestamp {
            color: #3498db;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 15px;
        }
        
        .progress-fill {
            height: 100%;
            background: #3498db;
            width: 0%;
            transition: width 0.3s;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-idle {
            background: #95a5a6;
        }
        
        .status-sending {
            background: #f39c12;
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .hidden {
            display: none;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
                gap: 20px;
                padding: 20px;
            }
            
            .settings-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 QQ消息发送器</h1>
            <p>跨平台QQ消息自动发送工具 - Web版本</p>
        </div>
        
        <div class="content">
            <!-- 左侧面板 -->
            <div class="panel">
                <h3>📝 消息设置</h3>
                
                <!-- 联系人设置 -->
                <div class="form-group">
                    <label for="contact">联系人名称 (可选):</label>
                    <input type="text" id="contact" class="form-control" placeholder="输入联系人名称">
                </div>
                
                <!-- 消息类型选择 -->
                <div class="form-group">
                    <label>消息类型:</label>
                    <div class="radio-group">
                        <div class="radio-item">
                            <input type="radio" id="single" name="messageType" value="single" checked>
                            <label for="single">单条消息</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="multiple" name="messageType" value="multiple">
                            <label for="multiple">多条消息</label>
                        </div>
                    </div>
                </div>
                
                <!-- 单条消息输入 -->
                <div class="form-group" id="singleMessageGroup">
                    <label for="singleMessage">消息内容:</label>
                    <input type="text" id="singleMessage" class="form-control" placeholder="输入要发送的消息">
                </div>
                
                <!-- 多条消息输入 -->
                <div class="form-group hidden" id="multipleMessageGroup">
                    <label for="multipleMessage">多条消息 (每行一条):</label>
                    <textarea id="multipleMessage" class="form-control" rows="6" placeholder="输入多条消息，每行一条"></textarea>
                </div>
                
                <!-- 发送设置 -->
                <div class="form-group">
                    <label>发送设置:</label>
                    <div class="settings-grid">
                        <div>
                            <label for="delay">延迟时间 (秒):</label>
                            <input type="number" id="delay" class="form-control" value="3" min="1" max="60">
                        </div>
                        <div>
                            <label for="interval">消息间隔 (秒):</label>
                            <input type="number" id="interval" class="form-control" value="2" min="1" max="60">
                        </div>
                    </div>
                </div>
                
                <!-- 控制按钮 -->
                <div class="form-group">
                    <button id="sendBtn" class="btn btn-primary">🚀 发送消息</button>
                    <button id="stopBtn" class="btn btn-danger" disabled>⏹️ 停止发送</button>
                    <button id="clearBtn" class="btn btn-secondary">🗑️ 清空内容</button>
                </div>
            </div>
            
            <!-- 右侧面板 -->
            <div class="panel">
                <h3>📊 状态信息</h3>
                
                <!-- 状态指示器 -->
                <div class="form-group">
                    <div>
                        <span class="status-indicator status-idle" id="statusIndicator"></span>
                        <span id="statusText">系统就绪</span>
                    </div>
                </div>
                
                <!-- 进度条 -->
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                
                <!-- 日志显示 -->
                <div class="form-group">
                    <label>操作日志:</label>
                    <div class="log-container" id="logContainer">
                        <div class="log-entry">
                            <span class="log-timestamp">[系统]</span> Web界面已启动，请确保QQ窗口处于活动状态
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 全局变量
        let isSending = false;
        let logUpdateInterval;
        
        // DOM元素
        const sendBtn = document.getElementById('sendBtn');
        const stopBtn = document.getElementById('stopBtn');
        const clearBtn = document.getElementById('clearBtn');
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        const logContainer = document.getElementById('logContainer');
        const progressFill = document.getElementById('progressFill');
        
        // 消息类型切换
        document.querySelectorAll('input[name="messageType"]').forEach(radio => {
            radio.addEventListener('change', function() {
                const singleGroup = document.getElementById('singleMessageGroup');
                const multipleGroup = document.getElementById('multipleMessageGroup');
                
                if (this.value === 'single') {
                    singleGroup.classList.remove('hidden');
                    multipleGroup.classList.add('hidden');
                } else {
                    singleGroup.classList.add('hidden');
                    multipleGroup.classList.remove('hidden');
                }
            });
        });
        
        // 发送消息
        sendBtn.addEventListener('click', async function() {
            if (isSending) return;
            
            const messageType = document.querySelector('input[name="messageType"]:checked').value;
            const contact = document.getElementById('contact').value;
            const delay = parseInt(document.getElementById('delay').value);
            const interval = parseInt(document.getElementById('interval').value);
            
            let messages = [];
            if (messageType === 'single') {
                const message = document.getElementById('singleMessage').value.trim();
                if (!message) {
                    alert('请输入要发送的消息');
                    return;
                }
                messages = [message];
            } else {
                const text = document.getElementById('multipleMessage').value.trim();
                if (!text) {
                    alert('请输入要发送的消息');
                    return;
                }
                messages = text.split('\\n').filter(line => line.trim());
            }
            
            const data = {
                message_type: messageType,
                contact: contact,
                delay: delay,
                interval: interval,
                single_message: document.getElementById('singleMessage').value,
                multiple_messages: document.getElementById('multipleMessage').value
            };
            
            try {
                const response = await fetch('/api/send', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    setSendingState(true);
                    startLogUpdates();
                } else {
                    alert(result.message);
                }
            } catch (error) {
                alert('发送失败: ' + error.message);
            }
        });
        
        // 停止发送
        stopBtn.addEventListener('click', async function() {
            try {
                const response = await fetch('/api/stop', {
                    method: 'POST'
                });
                
                const result = await response.json();
                if (result.success) {
                    setSendingState(false);
                    stopLogUpdates();
                }
            } catch (error) {
                alert('停止失败: ' + error.message);
            }
        });
        
        // 清空内容
        clearBtn.addEventListener('click', function() {
            document.getElementById('contact').value = '';
            document.getElementById('singleMessage').value = '';
            document.getElementById('multipleMessage').value = '';
            document.getElementById('delay').value = '3';
            document.getElementById('interval').value = '2';
            addLog('内容已清空', 'system');
        });
        
        // 设置发送状态
        function setSendingState(sending) {
            isSending = sending;
            sendBtn.disabled = sending;
            stopBtn.disabled = !sending;
            
            if (sending) {
                statusIndicator.className = 'status-indicator status-sending';
                statusText.textContent = '正在发送消息...';
            } else {
                statusIndicator.className = 'status-indicator status-idle';
                statusText.textContent = '系统就绪';
            }
        }
        
        // 添加日志
        function addLog(message, type = 'info') {
            const timestamp = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.innerHTML = `<span class="log-timestamp">[${timestamp}]</span> ${message}`;
            logContainer.appendChild(logEntry);
            logContainer.scrollTop = logContainer.scrollHeight;
        }
        
        // 开始日志更新
        function startLogUpdates() {
            logUpdateInterval = setInterval(updateLogs, 1000);
        }
        
        // 停止日志更新
        function stopLogUpdates() {
            if (logUpdateInterval) {
                clearInterval(logUpdateInterval);
                logUpdateInterval = null;
            }
        }
        
        // 更新日志
        async function updateLogs() {
            try {
                const response = await fetch('/api/logs');
                const data = await response.json();
                
                // 清空日志容器
                logContainer.innerHTML = '';
                
                // 添加日志条目
                data.logs.forEach(log => {
                    const logEntry = document.createElement('div');
                    logEntry.className = 'log-entry';
                    logEntry.innerHTML = `<span class="log-timestamp">[${log.timestamp}]</span> ${log.message}`;
                    logContainer.appendChild(logEntry);
                });
                
                logContainer.scrollTop = logContainer.scrollHeight;
                
                // 检查发送状态
                const statusResponse = await fetch('/api/status');
                const statusData = await statusResponse.json();
                
                if (!statusData.sending && isSending) {
                    setSendingState(false);
                    stopLogUpdates();
                }
                
            } catch (error) {
                console.error('更新日志失败:', error);
            }
        }
        
        // 页面加载时检查状态
        window.addEventListener('load', async function() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                if (data.sending) {
                    setSendingState(true);
                    startLogUpdates();
                }
            } catch (error) {
                console.error('检查状态失败:', error);
            }
        });
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == '__main__':
    # 创建模板文件
    create_templates()
    
    # 启动Web服务器
    print("=== QQ消息发送器 - Web版本 ===")
    print("正在启动Web服务器...")
    print("请在浏览器中访问: http://localhost:5000")
    print("确保QQ窗口处于活动状态")
    print("按 Ctrl+C 停止服务器")
    
    app.run(host='0.0.0.0', port=5000, debug=False) 