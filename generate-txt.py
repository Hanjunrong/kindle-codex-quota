#!/usr/bin/env python3
"""从 state/data.json 生成纯文本 data.txt（固定 8 行，供 Kindle 固定字号显示）。

行结构（对应 launch.sh 的字号映射）：
  1 时间  2 日期  3 温度  4 描述  5 体感湿度  6 风  7 Codex额度  8 重置
"""
import json, datetime, os

HOME = "/Users/han/temp/workspace/kindle-quota"
SRC = f"{HOME}/app/state/data.json"
OUT = f"{HOME}/gh-pages/data.txt"

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

def fmt_reset(iso):
    try:
        dt = datetime.datetime.fromisoformat(iso)
        return f"{dt.month}-{dt.day} {dt:%H:%M}"
    except Exception:
        return iso

def main():
    data = json.load(open(SRC, encoding="utf-8"))
    codex = data.get("sources", {}).get("codex", {})
    weather = data.get("weather", {})
    now = datetime.datetime.now().astimezone()

    lines = []
    lines.append(f"{now:%H:%M}")                       # 1 时间
    lines.append(f"{now.month}月{now.day}日 {WEEKDAYS[now.weekday()]}")  # 2 日期

    if weather.get("ok"):
        lines.append(f"北京 {weather.get('tempC', '?')}°")            # 3 温度
        lines.append(weather.get('description', ''))                   # 4 描述
        lines.append(f"体感{weather.get('feelsLikeC', '?')}° 湿度{weather.get('humidity', '?')}%")  # 5
        lines.append(f"{weather.get('windDir', '')}{weather.get('windKph', '?')}km/h")  # 6 风
    else:
        lines.extend(["天气：暂无", "", "", ""])

    if codex.get("ok") and codex.get("windows"):
        w = codex["windows"][0]
        lines.append(f"Codex 周额度 {w.get('usedPct', '?')}%")      # 7 额度
        lines.append(f"重置 {fmt_reset(w.get('resetAt', ''))}")     # 8 重置
    else:
        lines.extend(["Codex：暂无", ""])

    text = "\n".join(lines)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)

if __name__ == "__main__":
    main()
