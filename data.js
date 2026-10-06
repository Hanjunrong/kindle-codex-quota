window.DASH_DATA = {
  "updatedAt": "2026-10-06T14:05:16.441+08:00",
  "weather": {
    "ok": true,
    "description": "晴",
    "iconKey": "clear",
    "tempC": 25,
    "feelsLikeC": 22,
    "humidity": 14,
    "windKph": 23,
    "windDir": "北风",
    "place": "北京朝阳",
    "observedAt": "2026-10-06T14:03:41.943+08:00",
    "fetchedAt": "2026-10-06T14:05:16.441+08:00",
    "error": null
  },
  "quote": {
    "text": "锲而不舍，金石可镂。",
    "source": "荀子《劝学》"
  },
  "sources": {
    "claude": {
      "ok": false,
      "label": "Claude",
      "windows": [],
      "fetchedAt": "2026-10-06T14:05:13.031+08:00",
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
          "resetAt": "2026-10-06T19:03:43.000+08:00"
        },
        {
          "name": "周",
          "usedPct": 44,
          "resetAt": "2026-10-10T09:01:14.000+08:00"
        }
      ],
      "fetchedAt": "2026-10-06T14:03:42.247+08:00",
      "error": "failed to fetch codex rate limits: error sending request for url (https://chatgpt.com/backend-api/wham/usage)",
      "stale": true,
      "lastAttemptAt": "2026-10-06T14:05:13.032+08:00"
    },
    "kimi": {
      "ok": false,
      "label": "Kimi",
      "windows": [],
      "fetchedAt": "2026-10-06T14:05:13.036+08:00",
      "error": "未启用",
      "disabled": true
    },
    "deepseek": {
      "ok": false,
      "label": "DeepSeek",
      "balance": null,
      "currency": "CNY",
      "detail": null,
      "fetchedAt": "2026-10-06T14:05:13.036+08:00",
      "error": "未启用",
      "disabled": true
    }
  }
};
