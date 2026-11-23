# Aeolian Light Wallpaper

用于 Windows Wallpaper Engine 和 macOS Muro 的轻量网页壁纸代码：视频背景、时钟、日期与半圆音乐频谱。

## 两个独立版本

| 版本 | 位置 | 特点 |
| --- | --- | --- |
| 原省电版 | `versions/lite-v1` | 保留上一版代码；默认不额外叠加雪花，背景视频本身仍有雪花 |
| 雪花优化版 | `versions/snow-v2` | 默认24片额外雪花、12fps特效；持续静音不重绘频谱，响应宿主暂停 |

每个版本分别包含 `windows/` 与 `muro/`，可以独立构建、安装。Windows 默认使用720p24 WebM；Mac 默认1080p H.264，可在 `config.js` 中选择 `eco` 使用720p24。

仓库上传代码和构建工具；原画、视频、预览图不包含在Git中，也不自动下载。请使用自己已有的本地资源。原 WLOP/Aeolian 素材仍归原作者所有，代码与原画视频的权利分开。

## 准备视频并构建

需要 Python 3 和 FFmpeg。若没有FFmpeg命令，可安装提供本地FFmpeg的包：`python -m pip install imageio-ffmpeg`。

```sh
python tools/prepare_media.py --source "/path/to/original.webm"
python tools/build.py --version lite-v1
python tools/build.py --version snow-v2
```

已准备好 `background.webm`、`eco.webm`、`background.mp4`、`eco.mp4`、`still.jpg` 的资源目录时，可跳过转码：

```sh
python tools/build.py --version snow-v2 --assets "/path/to/prepared-assets"
```

构建结果在 `dist/<版本>/windows` 和 `dist/<版本>/muro`，包含所需的本地资源。原视频完整保留；本项目不修复原片首尾衔接。

## Windows：仅桌面时播放动画

1. 把构建后的 `windows` 整个文件夹放入 Wallpaper Engine 的 `projects/myprojects/`，使用独立文件夹名以便两个版本共存。
2. 选择对应壁纸；属性中可调整雪花数量、画质、日期和频谱。
3. Wallpaper Engine → 设置 → 性能 → **其他应用获得焦点：暂停**。其他应用最大化/全屏也可设为暂停或停止。

这项规则由宿主判断桌面是否处于前台；有其他应用获得焦点时，背景视频、雪花与频谱一起暂停，回到桌面后恢复，日期时间立即刷新。网页本身无法可靠知道桌面上方有哪些应用；不要把 `document.hasFocus()` 当作桌面可见性判断。

系统音频驱动频谱；支持系统媒体会话的播放器可以提供歌名和歌手。不需要Spotify令牌，壁纸不发网络请求。

## macOS：Muro

在支持互动壁纸的 Muro 中导入构建后的整个 `muro` 文件夹，开启 **Play only on desktop / 仅在桌面播放**。授予Muro系统音频权限后，频谱会响应声音。通过 `muro:pause`、`muro:resume` 和 `muro:audio` 适配宿主。

Muro当前桥接接口不提供歌名，故只有音乐频谱；`caption` 可显示静态文字。互动壁纸用于桌面；如需纯视频方式，可直接在Muro导入 `assets/eco.mp4` 或 `assets/background.mp4`。

## snow-v2 的优化

- 24片雪花共用一个低分辨率画布，最多640×360，不随Retina/4K翻倍；特效默认12fps。
- 频谱只画在640×320画布上。雪花持续运动时，静态频谱也不会被重复重画。
- 连续收到全零音频不会唤醒重绘；音频输入停止后通过单个看门狗归零。
- 复用64频段音频缓冲区；属性修改时仅在粒子数量变化后重建粒子。
- 宿主暂停时停止视频、绘制、时钟与音频看门狗。恢复时刷新时间，不积压旧音频。
- 时间默认每分钟更新；视频保持原生video播放，不逐帧复制至Canvas。

## 验证

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/smoke.py --root dist/snow-v2
```

测试使用浏览器模拟宿主事件，覆盖雪花运行、连续静音、暂停、过期音频、恢复与错误检查。模拟测试不是Wallpaper Engine或真实Mac/Muro实测；GPU改善幅度取决于硬件、屏幕、驱动和宿主设置，不承诺具体百分比。

## 接口文档

- [Wallpaper Engine 网页壁纸](https://docs.wallpaperengine.io/en/web/overview.html)
- [音频接口](https://docs.wallpaperengine.io/en/web/audio/visualizer.html)
- [暂停及属性事件](https://docs.wallpaperengine.io/en/web/api/propertylistener.html)
- [Muro](https://github.com/MrRockySL/Muro)
