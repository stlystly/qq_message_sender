# Windows平台窗口管理技术调研

## 📋 调研目标

在Windows平台下实现：
1. 获取当前最上层窗口信息
2. 切换到指定程序窗口
3. 自动定位QQ窗口并激活

## 🔍 技术方案对比

### 1. pyautogui (推荐度: ⭐⭐⭐⭐)

**优点:**
- 简单易用，API友好
- 与现有代码集成度高
- 支持窗口标题搜索和激活

**缺点:**
- 功能相对简单
- 某些版本可能缺少窗口管理功能

**关键方法:**
```python
# 查找窗口
windows = pyautogui.getWindowsWithTitle("QQ")

# 激活窗口
window.activate()

# 获取活动窗口
active_window = pyautogui.getActiveWindow()
```

### 2. win32gui (推荐度: ⭐⭐⭐⭐⭐)

**优点:**
- 功能最强大
- 底层Windows API封装
- 支持所有窗口操作

**缺点:**
- 学习曲线较陡
- 需要额外安装pywin32

**关键方法:**
```python
# 获取前台窗口
hwnd = win32gui.GetForegroundWindow()
title = win32gui.GetWindowText(hwnd)

# 枚举所有窗口
win32gui.EnumWindows(callback, windows)

# 激活窗口
win32gui.SetForegroundWindow(hwnd)
```

### 3. pywinauto (推荐度: ⭐⭐⭐⭐)

**优点:**
- 现代化API设计
- 支持UI自动化
- 功能丰富

**缺点:**
- 依赖较多
- 可能过于复杂

**关键方法:**
```python
# 连接到应用
app = Application().connect(title_re=".*QQ.*")

# 获取窗口
window = app.window()
```

### 4. psutil (推荐度: ⭐⭐⭐)

**优点:**
- 进程管理功能强大
- 跨平台兼容性好

**缺点:**
- 主要用于进程管理
- 窗口操作功能有限

### 5. ctypes (推荐度: ⭐⭐)

**优点:**
- 直接调用Windows API
- 性能最好

**缺点:**
- 代码复杂
- 维护困难

## 🎯 推荐方案

### 方案一：pyautogui + win32gui (推荐)

**适用场景:** 需要简单易用且功能强大
```python
# 主要使用pyautogui
windows = pyautogui.getWindowsWithTitle("QQ")
if windows:
    windows[0].activate()

# 复杂操作使用win32gui
import win32gui
hwnd = win32gui.FindWindow(None, "QQ")
win32gui.SetForegroundWindow(hwnd)
```

### 方案二：纯win32gui

**适用场景:** 需要最大控制权和功能
```python
import win32gui
import win32con

def find_qq_window():
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "QQ" in title:
                windows.append((hwnd, title))
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def activate_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
```

## 📦 依赖包

```bash
# 基础依赖
pip install pyautogui==0.9.54
pip install pywin32==306

# 可选依赖
pip install psutil==5.9.5
pip install pywinauto==0.6.8
```

## 🧪 测试方法

运行调研脚本：
```bash
python windows_window_research.py
```

该脚本会测试所有方案的可用性和功能。

## 💡 实现建议

1. **优先使用pyautogui**: 简单易用，满足大部分需求
2. **win32gui作为备选**: 处理复杂场景
3. **渐进式实现**: 先实现基础功能，再添加高级特性
4. **错误处理**: 添加完善的异常处理机制

## 🔧 示例代码

### 获取当前活动窗口
```python
def get_active_window():
    try:
        # 方法1: pyautogui
        window = pyautogui.getActiveWindow()
        if window:
            return window.title
    except:
        pass
    
    try:
        # 方法2: win32gui
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except:
        pass
    
    return None
```

### 切换到QQ窗口
```python
def switch_to_qq():
    try:
        # 方法1: pyautogui
        qq_windows = pyautogui.getWindowsWithTitle("QQ")
        if qq_windows:
            qq_windows[0].activate()
            return True
    except:
        pass
    
    try:
        # 方法2: win32gui
        def find_qq(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "QQ" in title:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(find_qq, windows)
        
        if windows:
            win32gui.SetForegroundWindow(windows[0])
            return True
    except:
        pass
    
    return False
```

## 📝 总结

- **pyautogui**: 适合快速实现，代码简洁
- **win32gui**: 适合复杂需求，功能最全
- **组合使用**: 最佳方案，兼顾易用性和功能性

建议先使用pyautogui实现基础功能，需要时再集成win32gui处理复杂场景。 