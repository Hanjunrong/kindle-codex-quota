window.DASH_DATA = {
  "updatedAt": "2026-11-06T16:27:12.249+08:00",
  "weather": {
    "ok": true,
    "description": "晴",
    "iconKey": "clear",
    "tempC": 12,
    "feelsLikeC": 8,
    "humidity": 20,
    "windKph": 19,
    "windDir": "南东南风",
    "place": "北京朝阳",
    "observedAt": "2026-11-06T16:21:13.384+08:00",
    "fetchedAt": "2026-11-06T16:27:12.250+08:00",
    "error": null
  },
  "quote": {
    "text": "路虽远，行则将至；事虽难，做则必成。",
    "source": "《荀子》"
  },
  "sources": {
    "claude": {
      "ok": false,
      "label": "Claude",
      "windows": [],
      "fetchedAt": "2026-11-06T16:27:04.142+08:00",
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
          "resetAt": "2026-11-06T18:17:28.000+08:00"
        },
        {
          "name": "周",
          "usedPct": 5,
          "resetAt": "2026-11-12T08:03:21.000+08:00"
        }
      ],
      "fetchedAt": "2026-11-06T16:24:27.792+08:00",
      "error": "failed to fetch codex rate limits: error sending request for url (https://chatgpt.com/backend-api/wham/usage)",
      "stale": true,
      "lastAttemptAt": "2026-11-06T16:27:04.143+08:00"
    },
    "kimi": {
      "ok": false,
      "label": "Kimi",
      "windows": [],
      "fetchedAt": "2026-11-06T16:27:04.148+08:00",
      "error": "未启用",
      "disabled": true
    },
    "deepseek": {
      "ok": false,
      "label": "DeepSeek",
      "balance": null,
      "currency": "CNY",
      "detail": null,
      "fetchedAt": "2026-11-06T16:27:04.148+08:00",
      "error": "未启用",
      "disabled": true
    }
  }
};
