# QQ消息发送器

一个跨平台的QQ消息自动发送工具，支持命令行、Web界面和AppleScript（macOS专用）等多种使用方式。

## 功能特性

- 🚀 **跨平台支持**: Windows、macOS、Linux
- 🌐 **Web界面**: 现代化的浏览器操作界面
- 📱 **多种模式**: 单条消息、多条消息、定时发送
- ⚙️ **灵活配置**: 可调节延迟、间隔时间
- 🔧 **多种实现**: pyautogui、AppleScript（macOS）
- 📦 **一键打包**: 支持打包成exe文件
- 🎯 **自动选中**: 自动定位和选中QQ输入框（Windows优化）

## 文件说明

### 核心文件
- `qq_message_sender_web.py` - Web版本主程序
- `qq_message_sender.py` - 命令行版本
- `requirements.txt` - Python依赖包列表

### 打包工具
- `direct_build.py` - 直接调用PyInstaller的打包脚本（推荐）
- `simple_build.py` - 简化的exe打包脚本
- `build_exe.py` - 完整的exe打包脚本
- `build_windows.bat` - Windows批处理打包脚本
- `debug_build.py` - 打包问题诊断工具
- `build_comparison.py` - PyInstaller调用方式对比测试

### 测试工具
- `test_pyautogui.py` - pyautogui功能测试
- `test_auto_select.py` - 自动选中输入框功能测试

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行程序

#### Web版本（推荐）
```bash
python qq_message_sender_web.py
```
然后在浏览器中访问 `http://localhost:5000`

#### 命令行版本
```bash
python qq_message_sender.py
```

## 打包成exe

### 方法一：使用直接调用脚本（推荐）

```bash
python direct_build.py
```

### 方法二：使用简化脚本

```bash
python simple_build.py
```

### 方法三：使用批处理脚本（Windows）

```bash
build_windows.bat
```

### 方法四：使用完整脚本

```bash
python build_exe.py
```

### 对比测试

如果你想了解不同调用方式的差异，可以运行对比测试：

```bash
python build_comparison.py
```

这将测试三种PyInstaller调用方式：
1. 直接调用 `PyInstaller.__main__.run()`
2. subprocess调用 `pyinstaller` 命令
3. Python模块调用 `python -m PyInstaller`

### 打包问题诊断

如果打包过程中遇到问题，请先运行诊断工具：

```bash
python debug_build.py
```

诊断工具会检查：
- Python环境
- 依赖包安装状态
- 文件完整性
- PyInstaller功能
- 磁盘空间
- 杀毒软件干扰

## 使用说明

### Web版本功能

1. **单条消息发送**
   - 输入联系人名称
   - 输入消息内容
   - 设置延迟时间
   - 选择输入框模式（自动/手动）
   - 点击发送

2. **多条消息发送**
   - 输入联系人名称
   - 输入多条消息（每行一条）
   - 设置延迟和间隔
   - 选择输入框模式（自动/手动）
   - 点击发送

3. **自动选中功能**
   - **自动选中模式**（推荐）：程序会自动尝试定位和选中QQ输入框
   - **手动选中模式**：需要用户手动点击QQ输入框
   - Windows下使用多种方法确保输入框被正确选中
   - 支持Tab键导航、Ctrl+A全选、Home/End键定位等

4. **实时日志**
   - 显示发送进度
   - 错误信息提示
   - 操作状态反馈

### 注意事项

#### Windows用户
- 确保QQ窗口处于活动状态
- 首次运行可能需要授予防火墙权限
- 如果打包失败，请运行 `debug_build.py` 诊断问题

#### macOS用户
- 需要授予辅助功能权限
- 建议使用AppleScript版本（已删除）
- 系统完整性保护可能影响自动化操作

#### 通用注意事项
- 确保端口5000未被占用
- 建议在测试环境中先试用
- 遵守相关法律法规和平台规则

## 常见问题

### 打包问题

**Q: 打包时窗口一闪而过，没有生成dist文件夹**
A: 请运行 `python debug_build.py` 诊断问题，常见原因：
- Python版本过低（需要3.6+）
- 依赖包安装失败
- 磁盘空间不足
- 杀毒软件拦截

**Q: PyInstaller命令找不到**
A: 这是常见问题，有几种解决方案：

1. **使用Python模块方式**（推荐）：
   ```bash
   python -m PyInstaller --onefile your_script.py
   ```

2. **运行修复脚本**：
   ```bash
   python fix_pyinstaller.py
   ```

3. **手动修复**：
   - 重新安装PyInstaller：`pip install --upgrade pyinstaller`
   - 将Python Scripts目录添加到PATH环境变量
   - 使用批处理文件：`pyinstaller.bat`

4. **检查PATH**：
   - 找到Python安装目录下的Scripts文件夹
   - 将其添加到系统PATH环境变量
   - 重启命令提示符

**Q: import PyInstaller成功但pyinstaller命令找不到**
A: 这是因为PyInstaller安装后没有正确添加到PATH。解决方案：

1. **运行诊断脚本**：
   ```bash
   python debug_build.py
   ```

2. **运行修复脚本**：
   ```bash
   python fix_pyinstaller.py
   ```

3. **使用Python模块方式**：
   ```bash
   python -m PyInstaller --onefile qq_message_sender_web.py
   ```

4. **手动添加PATH**：
   - 找到Python安装目录（通常在 `C:\Users\用户名\AppData\Local\Programs\Python\Python3x\Scripts`）
   - 将此路径添加到系统环境变量PATH中
   - 重启命令提示符

**Q: 打包后的exe文件很大**
A: 这是正常现象，包含了Python运行环境和所有依赖

### 运行问题

**Q: Web界面无法访问**
A: 检查：
- 端口5000是否被占用
- 防火墙是否阻止
- 浏览器地址是否正确

**Q: 消息发送失败**
A: 检查：
- QQ是否已启动
- QQ窗口是否处于活动状态
- 联系人名称是否正确

## 技术架构

- **后端**: Flask Web框架
- **前端**: HTML + CSS + JavaScript
- **自动化**: pyautogui（跨平台）
- **打包**: PyInstaller
- **依赖管理**: pip + requirements.txt

## 开发说明

### 添加新功能
1. 修改 `qq_message_sender_web.py`
2. 更新Web界面模板
3. 测试功能
4. 更新文档

### 调试技巧
- 使用 `debug_build.py` 诊断打包问题
- 查看控制台日志输出
- 检查浏览器开发者工具
- 使用 `test_pyautogui.py` 测试自动化功能

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和平台规则。

## 更新日志

- v1.0.0: 初始版本，支持命令行操作
- v1.1.0: 添加Web界面
- v1.2.0: 添加exe打包功能
- v1.3.0: 添加调试工具和详细日志 