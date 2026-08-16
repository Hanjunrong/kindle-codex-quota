#!/usr/bin/env python3
"""按日期从 quotes.json 挑一条，写入 quote.json（供 collect.cjs 的 readQuote 读取）。

选择规则：以"从 epoch 起的天数"模池子长度，保证同一天内稳定、每天切换一条。
"""
import datetime
import json
import os

HOME = "/Users/han/temp/workspace/kindle-quota"
POOL = os.path.join(HOME, "quotes.json")
OUT = os.path.join(HOME, "quote.json")


def main():
    pool = json.load(open(POOL, encoding="utf-8"))
    if not pool:
        pool = [{"text": "重要的东西，用眼睛是看不见的。", "source": "圣·埃克苏佩里《小王子》"}]
    days = (datetime.date.today() - datetime.date(1970, 1, 1)).days
    quote = pool[days % len(pool)]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(quote, f, ensure_ascii=False, indent=2)
    print(f"OK: {quote['text']} — {quote['source']}")


if __name__ == "__main__":
    main()