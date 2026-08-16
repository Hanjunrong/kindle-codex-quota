# Kindle Codex Quota

把吃灰的 Kindle 变成一块**电子墨水屏 AI 额度监控屏**：实时显示 Codex 用量，外加天气和每日一句，全屏长期常亮放在桌上。

本项目是在 `kindle-ai-quota-dashboard`（见 `app/`）基础上的**局域网自托管部署**，目标是「当前真正跑通」的路径：不走 GitHub Pages 中转，Mac 与服务机在同一局域网内通过 HTTP 实时采集并回退到上次数据。

## 项目用途

- 把一块越狱 Kindle 变成常亮的 AI 额度 + 天气 + 每日一句看板
- **Codex 额度实时监控**：走 `codex app-server --listen stdio://` 的 JSON-RPC，读取 `account/rateLimits/read` 窗口（周 / 5 小时档），当前账号为 Plus 计划，只有周额度档
- 天气（wttr 中文查表）+ 每日一句（本地池轮换，同日稳定）
- **局域网实时采集**：请求时采集、失败自动回退磁盘上次数据，完全不依赖外网 / GitHub Pages
- 电子墨水屏友好：最朴素的 `block` 布局（不适配 grid/flex），禁锁屏/禁休眠长时间常亮显示

## 架构一图流

```
Mac 端 serve.py (:8000，请求时实时采集 + 上次数据回退)
   │  HTTP /data.js  (JSONP window.DASH_DATA)   /data.txt
Kindle WAF app (file:/// 精简单页)
   │  通过 192.168.0.100-110 依次重试找 Mac，成功 IP 记 cookie 复用
   │  覆盖 store 缓存 → 重启 store → 打开 store 入口
```

数据链路：`weather-collect.py` → `pick-quote.py` → `npm run collect` → `generate-txt.py` / `generate-js.py` → `gh-pages/data.txt` / `data.js`。

> 注：`app/` 是上游 `kindle-ai-quota-dashboard` 子项目（支持多平台、GitHub Pages 跨网络方案），本项目用其中的采集器 + 自己这套局域网 serve 链路。部署细节与全部踩坑见 `SKILL.md`。

## 使用

1. **服务机**（Mac）常开：`python3 serve.py` 监听 `0.0.0.0:8000`
   - 已配置为 launchd 服务 `com.hanjunrong.kindle-codex-quota-http`，开机自启 + KeepAlive
2. **Kindle**：越狱（WinterBreak + KPM 0.2.x），安装 `device/` 部署包到设备端
   - 图书馆入口 `documents/AIQuota.sh` 触发；WAF app 依次重试局域网 IP 找到 Mac
3. 浏览器/设备打开 `http://<mac-ip>:8000/` 即可看到 `data.js` 数据

设备端部署文件（`/Volumes/Kindle` 挂载视角）见 `SKILL.md`「部署文件」一节。

## 设备信息（脱敏）

以下为本项目实际连接的 Kindle 设备信息（来自 IORegistry / diskutil 实读，脱敏后）：

| 项目 | 值 |
|---|---|
| 厂商 | Amazon |
| 产品 | Kindle |
| 型号推断 | Kindle Paperwhite 2（第 7 代，2013 款，内部型号 DP75SDI）— 依据序列号 `G090` 前缀 |
| 固件版本 | 5.16.2.1.1（build 409747 002） |
| 存储 | 约 3.3 GB，FAT32，挂载 `/Volumes/Kindle` |
| 接口 | USB（经 USB hub 接入，设备节点 `/dev/disk4s1`） |
| 越狱 | WinterBreak + KPM 0.2.x |

> 脱敏：厂商/产品/型号/容量/固件为公开信息保留；序列号等本机唯一标识未公开，仅用于内部定位。

## 目录结构

```
app/               # 上游 kindle-ai-quota-dashboard 子项目（采集器 + 前端）
device/            # 部署到 Kindle 设备端的精简单页应用
gh-pages/          # 生成的数据页面（data.txt / data.js）
serve.py           # 局域网 HTTP 数据服务器（实时采集 + 回退）
generate-txt.py    # app/state/data.json → gh-pages/data.txt
generate-js.py     # → gh-pages/data.js（JSONP）
pick-quote.py      # 每日一句（池按日期轮换）
weather-collect.py # wttr 天气采集
SKILL.md           # 完整部署过程 / 架构 / 永久踩坑清单
```

## License

- 本项目主体脚本：随 GitHub 仓库发布
- `app/` 子项目沿用其自身 `LICENSE`