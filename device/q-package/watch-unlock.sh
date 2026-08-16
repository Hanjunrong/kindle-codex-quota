#!/bin/sh
# 后台 watcher：监控 dashboard 是否还在前台；一旦离开即自动恢复锁屏/屏保后自退。
# 由 quit-dialoger.html 的 source_command 拉起（root shell 只在 pillow 对话框上下文可用）。
#
# 判据：Kindle 前台应用 prop fgApp
#   com.lab126.windord -> fgApp = "app://com.lab126.store" 表示 dashboard store 假窗在前台
# 持续 N 次非前台 → 判定已退出 → unlock。

DASH_APP="app://com.lab126.store"
STRIKE_MAX=4          # 连续检测次数（约 4 次 x 2s ≈ 8s）确认离开，避免误判
CHECK_INTERVAL=2
IDLE_GUARD_MIN=240    # 即使一直在前台，2 小时后也自退出 watcher，避免常驻泄漏

unlock() {
  lipc-set-prop com.lab126.powerd preventScreenSaver 0 2>/dev/null || true
  lipc-set-prop com.lab126.powerd preventSleep 0 2>/dev/null || true
  CACHE=/mnt/us/.active_content_sandbox/store/resource/cachedResources
  rm -f "$CACHE/index.html" "$CACHE/secondaryStore.html" 2>/dev/null || true
}

# 启动时给 store 一个充分的前台窗口，避免误判刚进入就恢复
sleep 12

elapsed=0
strike=0
while [ "$elapsed" -lt "$((IDLE_GUARD_MIN * 60))" ]; do
  current="$(lipc-get-prop -s com.lab126.windord fgApp 2>/dev/null)"
  case "$current" in
    "$DASH_APP")
      strike=0
      ;;
    *)
      strike=$((strike + 1))
      if [ "$strike" -ge "$STRIKE_MAX" ]; then
        unlock
        exit 0
      fi
      ;;
  esac
  sleep "$CHECK_INTERVAL"
  elapsed=$((elapsed + CHECK_INTERVAL))
done

unlock
exit 0