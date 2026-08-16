---
name: kindle-quota-skill
description: Kindle PW3 越狱下把 kindle-ai-quota-dashboard 部署到电子墨水屏（当前唯一走通的方案）。
---

# Kindle AI Quota Dashboard — 部署 Skill

## 目标
越狱 Kindle PW3（WinterBreak + KPM 0.2.x），把一个自托管的"AI 额度 + 天气 + 每日一句"面板显示到墨水屏上。本 skill 只记录 **当前跑通** 的路径与真实踩坑。

## 核心架构（当前唯一方案）
不走浏览器渲染复杂网页，也不走 GitHub。链路：

```
Mac 端 lived server (:8000，请求时实时采集 + 上次数据回退)
   │  HTTP /data.js  (JSONP window.DASH_DATA)
Kindle WAF app (file:/// 一个精简单页)  -- 通过 192.168.0.100-110 依次重试找到 Mac
   │  用 trick: 覆盖 store 缓存 → 重启 store → 打开 store 入口
```

## 部署文件（/Volumes/Kindle 挂载视角）
- 应用目录：`/mnt/us/apps/kindle-ai-quota-dashboard/`
  - `index.html` —— 精简块布局单页（勿用 grid/flex，见踩坑）
  - `dashboard-runtime.js` —— 渲染逻辑 + IP 依次重试 + 记住成功 IP
  - `live-endpoint.js` —— 定义候选 IP 段 `192.168.0.100-110`
  - `data.js` —— 本地回退数据（服务不可达时仍能显示）
  - `manifest.json` —— `{"waf": true, "id":..., "version": 1}`
- 跳转页：`/mnt/us/dashboard-redirect.html`
- 入口包：`/mnt/us/kmc/kpm/packages/q/launch.sh`（store 缓存覆盖方案）
- 图书馆入口：`/mnt/us/documents/AIQuota.sh`（`#DontUseFBInk` 头 → `kpm launch q --asap`）

## Launch 机制（关键 trick）
`launch.sh` 逐行（set -e）：
```sh
#!/bin/sh
set -e
REDIRECT=/mnt/us/dashboard-redirect.html
CACHE=/mnt/us/.active_content_sandbox/store/resource/cachedResources
cp "$REDIRECT" "$CACHE/index.html" 2>/dev/null || true
cp "$REDIRECT" "$CACHE/secondaryStore.html" 2>/dev/null || true
restart stored 2>/dev/null || { stop stored 2>/dev/null; start stored 2>/dev/null; }
sleep 3
lipc-set-prop com.lab126.appmgrd start "app://com.lab126.store" 2>/dev/null || true
exit 0
```

跳转页 `dashboard-redirect.html` 必须做三件事：
1. 伪装 `window.storeContext.isStoreLoaded = true`（否则 store 弹"暂不可用"）。
2. `kindle.net.setWirelessPrompt('never')` 关掉无线提示。
3. `top.location.href = "file:///mnt/us/apps/kindle-ai-quota-dashboard/index.html"` 跳到 WAF app。

## 数据链路（Mac 端 serve.py）
- 每次收到 `/data.js`（或 `/data.txt`）请求时**实时采集**（天气 wttr + Codex 额度），采集失败/超时自动用磁盘上**上一次**的 data.js 回退。
- 完全不走外网 / GitHub。
- 天气中文：wttr 英文描述做**忽略大小写/空白**的查表（见踩坑）。
- 每日一句：`quotes.json` 池 + 按"天数 mod 池长"每天换一条，同日稳定。

## 永久坑清单（别再踩）
- **PW3 浏览器是旧 mesquite/WebKit，渲染不了 `grid`/`flex`/`@media`**。用 `display:grid` 的"好看"页面到 Kindle 上直接空白/碎裂。必须用最朴素的 `block` + `float` + 固定 px 布局。
- **fbink 全屏纯文字面板 = 走不通的死路**（曾尝试用 `libkh/bin/fbink` 直接写 framebuffer、`wfb` 停 framework）。停 framework 极易白屏只能长按电源 40 秒硬重启。见 `macos/kindle-winterbreak-display` 残留，勿再复活。删掉的"商店/WAF/file://"被当过废弃，实为**正确**——是 fbink 路线被废弃。
- **GitHub Pages 每 3 分钟推送方案已废弃**：Mac IP/数据是本地 + 局域网，不走 github。不必再为它落盘/推送。
- **IP 写死必坏**：Mac 的局域网 IP 会变。设备侧要把 `192.168.0.100-110` 依次重试、成功记住（cookie `dash_idx`）复用。
- **天气英文**：wttr 返回 `"Partly Cloudy "`（带空格/大小写），精确查表会漏 → 转小写+strip 再查。
- **每日一句写死**会被认为偷懒；本地用池子按日期轮换。
- **KPM 平台串没有 `kindlepw3`**，PW3 用 `kindlepw2`。
- **`kpm launch <id>` 读 packages 表**（PK `repository,id`），手摆包要两表都 INSERT，否则崩。
- 库图标入口 `#DontUseFBInk` 头要保留在 `documents/*.sh` 首行，否则图书馆不显示为可点。
- KPM 真实安装/打包（`kpm install file://`、手打 tar.gz、库图标注册）细节见 `references/kpm-install.md`；
  手动解包+只 INSERT db 行那种"伪注册"是死的，别用。