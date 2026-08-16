#!/bin/sh
# 恢复锁屏/休眠（退出长时间显示后运行；或手动: lipc-set-prop com.lab126.powerd preventScreenSaver 0; ...Sleep 0）
lipc-set-prop com.lab126.powerd preventScreenSaver 0 2>/dev/null || true
lipc-set-prop com.lab126.powerd preventSleep 0 2>/dev/null || true
exit 0
