#!/usr/bin/env python3
"""采集 wttr.in 北京朝阳天气，生成 weather.json（供 collect.cjs 的 readWeather 读取）。"""
import json, subprocess, datetime, sys, os

LOCATION = "Chaoyang,Beijing"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weather.json")

DESC_MAP = {
    "Sunny": "晴", "Clear": "晴", "Partly cloudy": "多云",
    "Cloudy": "阴", "Overcast": "阴", "Mist": "雾", "Fog": "雾",
    "Haze": "霾", "Patchy rain nearby": "零星小雨",
    "Light rain": "小雨", "Light drizzle": "毛毛雨",
    "Moderate rain": "中雨", "Heavy rain": "大雨",
    "Moderate or heavy rain shower": "阵雨",
    "Light rain shower": "阵雨",
    "Light snow": "小雪", "Snow": "雪", "Heavy snow": "大雪",
    "Thundery outbreaks possible": "可能有雷雨",
    "Freezing fog": "冻雾", "Blizzard": "暴风雪",
}

WIND_MAP = {
    "N": "北风", "NNE": "北东北风", "NE": "东北风", "ENE": "东东北风",
    "E": "东风", "ESE": "东东南风", "SE": "东南风", "SSE": "南东南风",
    "S": "南风", "SSW": "南西南风", "SW": "西南风", "WSW": "西西南风",
    "W": "西风", "WNW": "西西北风", "NW": "西北风", "NNW": "北西北风",
}

_DESC_LOWER = {k.strip().lower(): v for k, v in DESC_MAP.items()}
_WIND_LOWER = {k.strip().lower(): v for k, v in WIND_MAP.items()}


def fetch():
    url = f"wttr.in/{LOCATION}?format=j1"
    r = subprocess.run(["curl", "-s", "-m", "15", url],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"curl 失败: {r.stderr or 'empty'}")
    data = json.loads(r.stdout)
    cc = data["current_condition"][0]

    desc_en = (cc["weatherDesc"][0].get("value") or "").strip()
    desc = _DESC_LOWER.get(desc_en.lower(), desc_en) or desc_en
    wind_en = (cc.get("winddir16Point") or "").strip()
    wind = _WIND_LOWER.get(wind_en.lower(), wind_en) or wind_en

    return {
        "description": desc,
        "iconKey": "clear" if desc == "晴" else "cloudy",
        "tempC": int(cc["temp_C"]),
        "feelsLikeC": int(cc["FeelsLikeC"]),
        "humidity": int(cc["humidity"]),
        "windKph": int(cc["windspeedKmph"]),
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
