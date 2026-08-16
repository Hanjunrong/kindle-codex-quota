# KPM 本地安装事实（source-verified，合并自 kindle-kpm-modding）

## kpkg 打包（本项目用商店缓存方案时一般不需要，但若走真实安装要用）
- 官方打包：`python kpm-helper.py package pack . ..`（manifest_version>=2 打成 tar.gz，顶层放 manifest.json）。
- 手打 tar.gz 也可（不依赖 Python/helper）：
  ```sh
  cd /path/to/package_src   # 含 manifest.json, launch.sh, install.sh, uninstall.sh, payload/
  tar -czf ../q.kpkg --exclude='._*' manifest.json launch.sh install.sh uninstall.sh payload
  tar -tzf ../q.kpkg        # 必须能在顶层看到 manifest.json，否则安装失败
  ```
- `Internal_GetManifest` 只认顶层名为 `manifest.json` 的文件；截断/残缺的 kpkg 会安装失败。
- 不要命名保留名：`rootfs`、`startup.sh`。

## 安装命令（三选一）
- **`;kpm install file:///mnt/us/q.kpkg`** —— 本地文件安装，KPM 直接读 manifest 安装，**正确**。
- `;kpm install /mnt/us/q.kpkg`（裸路径，无 scheme）—— 被当作仓库 artifact id → 报 "Could not find artifact"，**失败**。
- `;kpm install q`（裸 id）—— 查 KMC 官方仓库索引，仓库里没有 `q` → **失败**。

> 本项目设备上的路线其实是「手动放置包 `q` 的 launch.sh + 覆盖 store 缓存」，
> 并不依赖 `kpm install file://`。此文件仅保留真实安装/打包的可用事实，供将来需要时参考。

## 库图标注册
- `install.sh`/`uninstall.sh` 用 KPM 官方模式：`cp scriptlets/X.sh /mnt/us/documents/` 后
  `lipc-set-prop com.lab126.scanner doFullScan 1` → contentpackd 把该 .sh 当 app 启动器，
  Library 显示为可点图标（不是书籍）。
- 库入口脚本首行要 `# DontUseFBInk`（或对应头）才被识别为启动器。

## 已判死不用的（别再走）
- 手动解包 + 只 INSERT db 行来"注册"应用 —— 只伪造了数据层，没跑 KMC 真实安装，
  app 注册缺失，`kpm launch` 会崩/挂。真实安装（`kpm install file://`）才会做注册。
- 项目自带 `scripts/build-kpkg.cjs` 要求 `DASHBOARD_URL` 且拒绝 `file://`/本地 URL，离线局部测试不可用，别用它。