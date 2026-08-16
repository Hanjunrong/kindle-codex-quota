#!/usr/bin/env python3
"""从 state/data.json 生成 data.js（window.DASH_DATA 结构，供 Kindle WebKit 浏览器加载）。"""
import json
import os

HOME = "/Users/han/temp/workspace/kindle-quota"
SRC = f"{HOME}/app/state/data.json"
OUT = f"{HOME}/gh-pages/data.js"

def main():
    data = json.load(open(SRC, encoding="utf-8"))
    
    # 保持原有结构，直接写入
    js_content = f"window.DASH_DATA = {json.dumps(data, ensure_ascii=False)};\n"
    
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Generated {OUT}")

if __name__ == "__main__":
    main()