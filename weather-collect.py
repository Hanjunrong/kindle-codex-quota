#!/usr/bin/env python3
"""采集 open-meteo 北京朝阳天气，生成 weather.json（供 collect.cjs 的 readWeather 读取）。

之前用 wttr.in，其上游偶尔返回过期/错位数据（北京 8 月午后显示 11°C）。
open-meteo 无需 key、数据可信，故改用之。
"""
import json, datetime, sys, os, urllib.request

LAT, LON = 39.9042, 116.4074  # 北京朝阳
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weather.json")

# WMO weather code -> 中文描述
WMO_DESC = {
    0: "晴", 1: "晴", 2: "多云", 3: "阴",
    45: "雾", 48: "冻雾",
    51: "毛毛雨", 53: "毛毛雨", 55: "毛毛雨",
    56: "冻毛毛雨", 57: "冻毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨",
    66: "冻雨", 67: "冻雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    77: "雪粒",
    80: "阵雨", 81: "阵雨", 82: "强阵雨",
    85: "阵雪", 86: "阵雪",
    95: "雷雨", 96: "雷雨伴冰雹", 99: "雷雨伴冰雹",
}


def fetch():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        "weather_code,wind_speed_10m,wind_direction_10m"
        "&timezone=Asia%2FShanghai"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "kindle-codex-quota/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"open-meteo 请求失败: {e}")

    cur = data.get("current") or {}
    code = int(cur.get("weather_code", -1))
    desc = WMO_DESC.get(code, "未知")

    # 风向（度）-> 16 方位中文
    deg = float(cur.get("wind_direction_10m", 0))
    dirs = ["北风", "北东北风", "东北风", "东东北风",
            "东风", "东东南风", "东南风", "南东南风",
            "南风", "南西南风", "西南风", "西西南风",
            "西风", "西西北风", "西北风", "北西北风"]
    wind = dirs[int(((deg % 360) + 11.25) // 22.5) % 16]

    return {
        "description": desc,
        "iconKey": "clear" if desc == "晴" else "cloudy",
        "tempC": round(cur["temperature_2m"]),
        "feelsLikeC": round(cur["apparent_temperature"]),
        "humidity": round(cur["relative_humidity_2m"]),
        "windKph": round(cur["wind_speed_10m"] * 3.6),
        "windDir": wind,
        "place": "北京朝阳",
        "observedAt": datetime.datetime.now().astimezone().isoformat(),
    }

if __name__ == "__main__":
    try:
        w = fetch()
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(w, f, ensure_ascii=False, indent=2)
        print(f"OK: {w['description']} {w['tempC']}°C 体感{w['feelsLikeC']}°C 湿度{w['humidity']}% {w['windDir']}{w['windKph']}km/h")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
