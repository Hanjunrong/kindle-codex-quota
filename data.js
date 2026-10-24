window.DASH_DATA = {
  "updatedAt": "2026-10-24T23:19:37.168+08:00",
  "weather": {
    "ok": true,
    "description": "阴",
    "iconKey": "cloudy",
    "tempC": 13,
    "feelsLikeC": 13,
    "humidity": 84,
    "windKph": 14,
    "windDir": "北东北风",
    "place": "北京朝阳",
    "observedAt": "2026-10-24T23:18:14.364+08:00",
    "fetchedAt": "2026-10-24T23:19:37.168+08:00",
    "error": null
  },
  "quote": {
    "text": "志不求易者成，事不避难者进。",
    "source": "《后汉书》"
  },
  "sources": {
    "claude": {
      "ok": false,
      "label": "Claude",
      "windows": [],
      "fetchedAt": "2026-10-24T23:19:36.147+08:00",
      "error": "未启用",
      "disabled": true
    },
    "codex": {
      "ok": true,
      "label": "Codex",
      "windows": [
        {
          "name": "5小时",
          "usedPct": 0,
          "resetAt": "2026-10-25T02:48:54.000+08:00"
        },
        {
          "name": "周",
          "usedPct": 1,
          "resetAt": "2026-10-31T08:15:50.000+08:00"
        }
      ],
      "fetchedAt": "2026-10-24T23:18:14.759+08:00",
      "error": "failed to fetch codex rate limits: GET https://chatgpt.com/backend-api/wham/usage failed: 504 Gateway Timeout; content-type=text/plain; charset=UTF-8; body=error code: 504\n",
      "stale": true,
      "lastAttemptAt": "2026-10-24T23:19:36.148+08:00"
    },
    "kimi": {
      "ok": false,
      "label": "Kimi",
      "windows": [],
      "fetchedAt": "2026-10-24T23:19:36.152+08:00",
      "error": "未启用",
      "disabled": true
    },
    "deepseek": {
      "ok": false,
      "label": "DeepSeek",
      "balance": null,
      "currency": "CNY",
      "detail": null,
      "fetchedAt": "2026-10-24T23:19:36.152+08:00",
      "error": "未启用",
      "disabled": true
    }
  }
};
