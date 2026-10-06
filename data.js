window.DASH_DATA = {
  "updatedAt": "2026-10-06T21:47:19.588+08:00",
  "weather": {
    "ok": true,
    "description": "晴",
    "iconKey": "clear",
    "tempC": 20,
    "feelsLikeC": 16,
    "humidity": 30,
    "windKph": 39,
    "windDir": "西南风",
    "place": "北京朝阳",
    "observedAt": "2026-10-06T21:45:30.948+08:00",
    "fetchedAt": "2026-10-06T21:47:19.589+08:00",
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
      "fetchedAt": "2026-10-06T21:47:02.724+08:00",
      "error": "未启用",
      "disabled": true
    },
    "codex": {
      "ok": true,
      "label": "Codex",
      "windows": [
        {
          "name": "5小时",
          "usedPct": 1,
          "resetAt": "2026-10-07T02:16:42.000+08:00"
        },
        {
          "name": "周",
          "usedPct": 55,
          "resetAt": "2026-10-10T09:01:14.000+08:00"
        }
      ],
      "fetchedAt": "2026-10-06T21:45:31.312+08:00",
      "error": "failed to fetch codex rate limits: error sending request for url (https://chatgpt.com/backend-api/wham/usage)",
      "stale": true,
      "lastAttemptAt": "2026-10-06T21:47:02.725+08:00"
    },
    "kimi": {
      "ok": false,
      "label": "Kimi",
      "windows": [],
      "fetchedAt": "2026-10-06T21:47:02.730+08:00",
      "error": "未启用",
      "disabled": true
    },
    "deepseek": {
      "ok": false,
      "label": "DeepSeek",
      "balance": null,
      "currency": "CNY",
      "detail": null,
      "fetchedAt": "2026-10-06T21:47:02.730+08:00",
      "error": "未启用",
      "disabled": true
    }
  }
};
