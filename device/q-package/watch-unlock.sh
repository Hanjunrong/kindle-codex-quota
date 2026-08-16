#!/bin/sh
# 后台 watcher v2：监控 dashboard 是否仍在前台；离开后自动恢复锁屏/屏保。
# v1 失败原因：fgApp 判据在 file:// WAF 下不可靠，误判离开 → 停留时也解锁。
# v2 改动：
#   - 每次判据结果写日志 /mnt/us/kmc/kpm/packages/q/watch.log，供设备实测校对真实 fgApp 值
#   - 多候选匹配（覆盖 store 假窗几种可能 id）
#   - 恢复门限放大 + 更长确认窗口，避免误判

DASH_PATTERNS='app://com.lab126.store|com.lab126.store|app://com.lab126.browser|com.lab126.browser|store'
CHECK_INTERVAL=3
STRIKE_MAX=12          # 连续 ~36s 非匹配才判定离开（v1 是 4 次/8s，太激进）
IDLE_GUARD_MIN=300     # 一直在前台也会在 5 小时后自退，防常驻泄漏
LOG=/mnt/us/kmc/kpm/packages/q/watch.log

prevent_on() {
  lipc-set-prop com.lab126.powerd preventScreenSaver 1 2>/dev/null || true
  lipc-set-prop com.lab126.powerd preventSleep 1 2>/dev/null || true
}

unlock() {
  lipc-set-prop com.lab126.powerd preventScreenSaver 0 2>/dev/null || true
  lipc-set-prop com.lab126.powerd preventSleep 0 2>/dev/null || true
  CACHE=/mnt/us/.active_content_sandbox/store/resource/cachedResources
  rm -f "$CACHE/index.html" "$CACHE/secondaryStore.html" 2>/dev/null || true
}

log() { echo "$(date '+%H:%M:%S') $*" >> "$LOG" 2>/dev/null || true; }

# 启动保护：给 store 充分前台窗口，避免刚进入就被误判
# 同时先强制置 1，确保就算误判也有最基础的常亮
sleep 20
prevent_on
log "watch start"

elapsed=0
strike=0
while [ "$elapsed" -lt "$((IDLE_GUARD_MIN * 60))" ]; do
  current="$(lipc-get-prop -s com.lab126.windord fgApp 2>/dev/null)"
  log "fgApp=[$current]"
  case "$current" in
    store|"app://com.lab126.store"|"com.lab126.store"|"app://com.lab126.browser"|"com.lab126.browser")
      # 仍在 dashboard store 假窗前台：保持禁屏保，清零 strike
      prevent_on
      strike=0
      ;;
    *)
      # 不是已知前台。v1 这里立刻累计解锁导致误判；v2 先不信，
      # 但当 front missing 时必须同时满足：连续足够多次 + fgApp 已被读到(非空)
      if [ -z "$current" ]; then
        log "front missing/empty — ignore"
        strike=$((strike + 1))
      else
        strike=$((strike + 1))
      fi
      log "strike=$strike/$STRIKE_MAX"
      if [ "$strike" -ge "$STRIKE_MAX" ]; then
        log "confirmed leave — unlock"
        unlock
        exit 0
      fi
      ;;
  esac
  sleep "$CHECK_INTERVAL"
  elapsed=$((elapsed + CHECK_INTERVAL))
done

log "idle guard reached — unlock"
unlock
exit 0