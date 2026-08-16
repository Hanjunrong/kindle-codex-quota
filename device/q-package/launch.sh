#!/bin/sh
# AIQuota 入口：覆盖 store 缓存 → 重启 store → 打开 store
set -e

# 0. 持续显示：禁屏保 / 禁睡眠（长时间显示 AI Quota）
lipc-set-prop com.lab126.powerd preventScreenSaver 1 2>/dev/null || true
lipc-set-prop com.lab126.powerd preventSleep 1 2>/dev/null || true

REDIRECT=/mnt/us/dashboard-redirect.html
CACHE=/mnt/us/.active_content_sandbox/store/resource/cachedResources

# 1. 覆盖 store 缓存（跳转页）
cp "$REDIRECT" "$CACHE/index.html" 2>/dev/null || true
cp "$REDIRECT" "$CACHE/secondaryStore.html" 2>/dev/null || true

# 2. 重启 store（强制重新加载缓存）
restart stored 2>/dev/null || { stop stored 2>/dev/null; start stored 2>/dev/null; }
sleep 3

# 3. 打开 store
lipc-set-prop com.lab126.appmgrd start "app://com.lab126.store" 2>/dev/null || true

exit 0