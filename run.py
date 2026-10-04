# -*- coding: utf-8 -*-
"""
Antigravity Skill Manager 启动入口
支持单实例复用检测、强韧 Windows 原生浏览器唤起、无控制台静默运行与自适应就绪探针
"""

import sys
import os
import io
import time
import logging
import threading
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# 获取用户数据目录用于存放运行日志
LOG_DIR = Path.home() / ".gemini" / "config" / "skill_manager_data"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

class SafeWriter:
    """安全的流包装器，当 sys.stdout/stderr 为 None 或已关闭时安全写入日志文件"""
    def __init__(self, log_path: Path):
        self.log_path = log_path

    def write(self, message):
        if not message:
            return
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(message)
        except Exception:
            pass

    def flush(self):
        pass

# 处理 PyInstaller console=False 导致 sys.stdout/sys.stderr 为 None 的问题
if sys.stdout is None:
    sys.stdout = SafeWriter(LOG_FILE)
else:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

if sys.stderr is None:
    sys.stderr = SafeWriter(LOG_FILE)
else:
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 配置根日志器
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

def log(msg: str):
    try:
        print(msg)
    except Exception:
        pass
    logging.info(msg)

def launch_browser(url: str):
    """使用 Windows 原生 ShellExecute 强韧唤起系统默认浏览器"""
    log(f"正在唤起系统默认浏览器: {url}")
    # 策略 1: Windows 原生 os.startfile (最稳定、最兼容)
    if hasattr(os, "startfile"):
        try:
            os.startfile(url)
            log("通过 os.startfile 成功唤起默认浏览器")
            return True
        except Exception as e:
            log(f"os.startfile 唤起失败: {e}，尝试备用方案")
    
    # 策略 2: cmd start
    try:
        subprocess.Popen(f'explorer "{url}"', shell=True)
        log("通过 explorer 唤起成功")
        return True
    except Exception as e:
        log(f"explorer 唤起失败: {e}")

    # 策略 3: Python webbrowser
    try:
        import webbrowser
        webbrowser.open(url)
        log("通过 webbrowser.open 唤起")
        return True
    except Exception as e:
        log(f"webbrowser.open 唤起失败: {e}")
    return False

def is_server_already_running(url: str, timeout: float = 0.8) -> bool:
    """探测服务是否已经在后台运行"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AntigravityLauncher"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False

def wait_and_open_browser(url: str, max_wait: float = 12.0):
    """在后台轮询检测服务就绪状态，一旦端口就绪立刻打开浏览器"""
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if is_server_already_running(url, timeout=0.5):
            log(f"服务器已成功就绪 (耗时 {round(time.time() - start_time, 2)}s)，正在打开网页...")
            launch_browser(url)
            return
        time.sleep(0.2)
    # 如果超时仍未探测成功，依然尝试打开一次
    log("服务就绪探测超时，尝试强行唤起浏览器")
    launch_browser(url)

if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:8765"

    log("=" * 60)
    log(" [*] AI Coding Skill Manager (AI Coding 技能管理器) 启动器激活")

    # 1. 单实例与端口复用检测：如果已有服务在后台运行，直接打开网页并退出新进程
    if is_server_already_running(SERVER_URL):
        log(" [√] 检测到服务已在后台运行中，直接激活并打开浏览器界面！")
        launch_browser(SERVER_URL)
        sys.exit(0)

    try:
        from backend.server import app
        import uvicorn

        log(f" [*] 正在启动后台服务引擎并监听 8765 端口...")

        # 2. 异步监控就绪线程，一旦端口可访问立即打开浏览器
        threading.Thread(target=wait_and_open_browser, args=(SERVER_URL,), daemon=True).start()

        # 3. 运行 uvicorn 服务器
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8765,
            reload=False,
            log_config=None,  # 避免重设标准输出
            access_log=False
        )
    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        log(f"应用致命错误启动失败:\n{err_msg}")
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, f"AI Coding Skill Manager 启动异常：\n{e}\n日志文件：\n{LOG_FILE}", "启动错误", 0x10)
        except Exception:
            pass
        sys.exit(1)
