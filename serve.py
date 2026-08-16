#!/usr/bin/env python3
"""Kindle AI Quota — 局域网数据服务器（替代 GitHub 定时推送方案）。

设计：
- 监听 0.0.0.0:8000，静态文件走本仓库的 gh-pages。
- 每次收到 /data.txt 请求时【实时采集】一次（天气 + Codex 额度），
  生成最新的 data.txt 返回；采集失败/超时则用磁盘上【上次】的 data.txt。
- 完全不依赖外网 / GitHub。
- 合并了原两个 launchd 任务（定时推送 + http.server）为一个。

采集链：weather-collect.py -> npm run collect -> generate-txt.py
（generate-txt.py 从 app/state/data.json 生成 gh-pages/data.txt）
"""
import os
import subprocess
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PROJECT = os.path.dirname(os.path.abspath(__file__))
GH_PAGES = os.path.join(PROJECT, "gh-pages")
APP_DIR = os.path.join(PROJECT, "app")
WEATHER = os.path.join(PROJECT, "weather-collect.py")
GEN = os.path.join(PROJECT, "generate-txt.py")
PICK = os.path.join(PROJECT, "pick-quote.py")

LOCK = threading.Lock()


def collect() -> bool:
    """实时采集。返回 True 表示 data.txt/data.js 已就绪（无论新生成还是上次残留）。"""
    try:
        subprocess.run(
            ["python3", PICK],
            timeout=15, check=False,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["/bin/bash", "-lc", f"python3 {WEATHER}"],
            timeout=30, check=False,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["/bin/bash", "-lc", f"cd {APP_DIR} && npm run collect"],
            timeout=60, check=False,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["python3", GEN],
            timeout=30, check=False,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            ["python3", os.path.join(PROJECT, "generate-js.py")],
            timeout=30, check=False,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass
    return os.path.exists(os.path.join(GH_PAGES, "data.txt"))


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/data.txt", "/data"):
            with LOCK:
                collect()
                fp = os.path.join(GH_PAGES, "data.txt")
            if os.path.exists(fp):
                self._send_file(fp, "text/plain; charset=utf-8")
            else:
                self.send_error(503, "no data available")
        elif path == "/data.js":
            with LOCK:
                collect()
                fp = os.path.join(GH_PAGES, "data.js")
            if os.path.exists(fp):
                self._send_file(fp, "application/javascript; charset=utf-8")
            else:
                self.send_error(503, "no data available")
        else:
            super().do_GET()

    def _send_file(self, fp, ctype):
        try:
            with open(fp, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        except Exception:
            self.send_error(500)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    os.chdir(GH_PAGES)
    srv = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    srv.serve_forever()
