#!/bin/sh
# Name: 恢复锁屏与屏保
# Author: Community contributors
# Icon: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==
# DontUseFBInk

if [ -f /mnt/us/kmc/kpm/packages/q/unlock.sh ]; then
  /bin/sh /mnt/us/kmc/kpm/packages/q/unlock.sh
else
  lipc-set-prop com.lab126.powerd preventScreenSaver 0 2>/dev/null || true
  lipc-set-prop com.lab126.powerd preventSleep 0 2>/dev/null || true
fi

# 回到书架刷新（确保 GUI 回到首页）
killall kindle_browser >/dev/null 2>&1 || true
if [ -d /etc/upstart ]; then
  status lab126_gui 2>/dev/null | grep -q running || start lab126_gui >/dev/null 2>&1 || true
else
  /etc/init.d/framework start >/dev/null 2>&1 || true
fi
sync
exit 0