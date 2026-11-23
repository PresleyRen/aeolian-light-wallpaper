# Aeolian Light Wallpaper

Windows Wallpaper Engine / macOS Muro 动态壁纸：视频背景、时钟、日期与音乐半圆频谱。提供省电版、雪花版，以及没有网页叠加层的纯视频方式。

## 先选平台和版本

| 平台 | 省电互动版 | 雪花互动版 | 纯视频版 |
| --- | --- | --- | --- |
| Windows / Wallpaper Engine | `dist/windows/lite-v1` | `dist/windows/snow-v2` | `dist/windows/video-eco` |
| Mac / Muro | `dist/muro/lite-v1` | `dist/muro/snow-v2` | `dist/muro/video-eco` |

- **省电互动版**：0片额外雪花，保留时钟、日期、音乐频谱。原视频自身有雪花。
- **雪花互动版**：默认24片额外雪花，保留时钟、日期、音乐频谱。
- **纯视频版**：原片动态和原片雪花，没有实时时钟、日期、歌名或频谱，适合优先减少网页开销。

两平台互动版现统一默认 **720p / 24fps 视频、12fps 特效**。此前Mac默认1080p，本次改为省电默认值；需要更清晰时可构建1080p选项。

Windows网页版使用WebM；Mac互动版和两平台纯视频版使用H.264 MP4。Windows可显示系统媒体歌名；Muro当前桥接接口没有歌名事件，只提供频谱。互动壁纸用于桌面，Mac锁屏/屏保请使用宿主支持的纯视频方式。

## 获得可安装文件

仓库保存源码、配置和构建工具。原视频、原画、预览图需要使用自己已有的本地资源准备，不在Git中分发。原 WLOP/Aeolian 素材仍归原作者所有。

需要Python 3与FFmpeg；没有FFmpeg命令时可安装 `imageio-ffmpeg`。

```sh
python -m pip install imageio-ffmpeg
python tools/prepare_media.py --source "/path/to/original.webm"
python tools/build.py --zip
```

默认生成上表六个可独立导入的文件夹，ZIP在 `dist/packages/`。只准备和打包720p资源，避免每个包都携带不使用的1080p视频。

例如只生成Windows雪花版：

```sh
python tools/build.py --platform windows --version snow-v2 --mode interactive --zip
```

[完整构建参数与目录说明](docs/build.md)包含单平台、纯视频、720p/1080p双画质和复用已有资源的方法。已构建的壁纸运行时不需要开发工具。

## 安装和“只在桌面时动画”

**Windows**：把所选完整文件夹放进 Wallpaper Engine 的 `projects/myprojects/`，设置 → 性能 → **其他应用获得焦点：暂停**。详见 [Windows安装说明](docs/windows.md)。

**Mac**：在支持互动壁纸的Muro中导入完整文件夹，开启 **Play only on desktop / 仅在桌面播放**；按系统提示授予Muro音频权限。详见 [Mac安装说明](docs/muro.md)。

暂停规则由宿主判断；切到其他应用时，背景视频、雪花和频谱一起暂停，回到桌面恢复并刷新时间。代码响应宿主事件，不扫描进程、不轮询其他窗口，也不把网页焦点当成桌面可见性。

## 代码与文件组织

```text
src/                     # 唯一一份核心JS、HTML、CSS和默认配置
  adapters/              # Windows / Muro各自的宿主事件适配
versions/
  lite-v1/profile.json   # 省电版配置
  snow-v2/profile.json   # 雪花版配置
tools/                   # 本地资源准备、构建与性能采样
tests/                   # 四个互动目标的回归检查
docs/                    # 平台安装、配置、构建和性能说明
assets/                  # 自行准备的本地媒体，不提交Git
dist/                    # 生成的独立安装包，不提交Git
```

两个版本各自保留配置和独立安装输出，共享已优化的核心逻辑；旧版完整源码可在Git历史中查看。[配置参数说明](docs/configuration.md)

## 性能优化和验证

高开销候选首先是视频解码/缩放、全屏合成和宿主进程；不应把几MiB的JS堆当成整个壁纸内存。已减少重复代码、按需分配画布、批量绘制雪花、跳过静态频谱计算，并在暂停时停止全部页面计时器。

[性能说明与实测范围](docs/performance.md)记录开销判断、前后采样、CPU/内存/GPU指标的区别及限制。

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/smoke.py --root dist
python tools/profile.py --root dist/windows/snow-v2 --out performance.json
```

测试覆盖Windows/Mac × 省电/雪花四个目标，包括雪花、静音、音频过期、画布释放、暂停/恢复和本地资源。浏览器模拟通过不等于真实Mac/Muro性能实测，不承诺固定GPU下降比例。

## 宿主接口

- [Wallpaper Engine 网页格式](https://docs.wallpaperengine.io/en/web/overview.html)、[音频](https://docs.wallpaperengine.io/en/web/audio/visualizer.html)、[暂停和属性](https://docs.wallpaperengine.io/en/web/api/propertylistener.html)
- [Muro](https://github.com/MrRockySL/Muro)
