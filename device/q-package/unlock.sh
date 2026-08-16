#!/bin/sh
# 恢复锁屏与屏保（退出长时间显示后运行）。
# 等价手动操作：lipc-set-prop com.lab126.powerd preventScreenSaver 0
#               lipc-set-prop com.lab126.powerd preventSleep 0

# 1. 恢复屏保与休眠
lipc-set-prop com.lab126.powerd preventScreenSaver 0 2>/dev/null || true
lipc-set-prop com.lab126.powerd preventSleep 0 2>/dev/null || true

# 2. 清掉被覆盖的 store 缓存（防止下次进 dashboard 前 store 还指向跳转页）
CACHE=/mnt/us/.active_content_sandbox/store/resource/cachedResources
rm -f "$CACHE/index.html" "$CACHE/secondaryStore.html" 2>/dev/null || true

# 3. 回到书架/首页（若 framework 被停过则拉起 GUI）
if [ -d /etc/upstart ]; then
  status lab126_gui 2>/dev/null | grep -q running || start lab126_gui >/dev/null 2>&1 || true
else
  /etc/init.d/framework start >/dev/null 2>&1 || true
fi

exit 0