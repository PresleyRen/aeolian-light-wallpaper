# Windows：下载后添加到 Wallpaper Engine

## 1. 下载和解压正确的包

| 想要的效果 | 完整安装包 | 解压后的文件夹 |
| --- | --- | --- |
| 省电，保留日期/时钟/频谱 | `windows-lite-v1.zip` | `windows-lite-v1` |
| 雪花、日期/时钟/频谱 | `windows-snow-v2.zip` | `windows-snow-v2` |
| 原片动态，尽量减少网页开销 | `windows-video-eco.zip` | `windows-video-eco` |

右键ZIP → 全部解压。不要在压缩软件内直接打开壁纸，也不要只取出HTML。

GitHub的绿色Code → Download ZIP下载的是**源码**，通常名为 `aeolian-light-wallpaper-main.zip`，不带视频，不能直接导入使用。仓库目前未发布Release安装附件；使用项目交付的完整安装ZIP，或按[构建教程](build.md)自行生成。

以雪花版为例，解压后确认这一层同时有：

```text
windows-snow-v2/
  index.html
  project.json
  app.js
  adapter.js
  config.js
  style.css
  preview.jpg
  使用说明.txt
  assets/
    eco.webm
```

## 2. 找到 Wallpaper Engine 的安装目录

打开Steam → 库 → 右键Wallpaper Engine → 管理 → 浏览本地文件。

打开的位置应包含 `wallpaper32.exe` 或 `wallpaper64.exe`。进入 `projects`，再进入 `myprojects`；没有 `myprojects` 时创建一个同名文件夹。

常见位置示例：

```text
D:\Steam\steamapps\common\wallpaper_engine\projects\myprojects\
```

以你的实际Steam安装位置为准，不需要重新安装程序。

## 3. 复制整个文件夹并应用

把解压得到的 `windows-snow-v2` 整个文件夹复制进去。最终层级应为：

```text
wallpaper_engine/projects/myprojects/windows-snow-v2/project.json
wallpaper_engine/projects/myprojects/windows-snow-v2/index.html
wallpaper_engine/projects/myprojects/windows-snow-v2/assets/eco.webm
```

`project.json` 和 `index.html` 应在版本文件夹的第一层，避免又多套一个 `windows-snow-v2/windows-snow-v2/`。

重新打开Wallpaper Engine的壁纸选择窗口，找到 **Aeolian Light | snow-v2 | 雪花版**，选中并应用。省电版同理，选择 `lite-v1`。两个文件夹可并存，切换版本不需要覆盖原版。

如果列表暂时没更新，关闭并重新打开壁纸选择窗口。备用导入方式：打开壁纸编辑器，将专用文件夹内的 `index.html` 拖到“创建壁纸 / Create Wallpaper”入口；编辑器会复制该文件夹。不要导入整个下载目录或源码仓库根目录。[官方网页壁纸导入说明](https://docs.wallpaperengine.io/en/web/first/gettingstarted.html)

## 4. 设置只在桌面时动画

Wallpaper Engine → 设置 → 性能 → **其他应用获得焦点：暂停**。其他应用最大化/全屏也可设为暂停或停止。

打开一个应用时，背景、雪花和频谱一起暂停；最小化窗口或点回桌面后恢复，日期时间刷新。此规则按应用焦点判断，并非逐像素检测遮挡；点击桌面后，小窗口仍存在时也可能恢复。

右侧壁纸属性可调雪花数量、24小时制、中文日期、频谱和位置。默认720p24视频、12fps特效；省电版额外雪花0，雪花版24。原视频自身也有雪。

## 5. 播放音乐并检查

播放电脑上的音乐，回到桌面。系统输出有声音时，半圆频谱应变化；没有声音时保持静态。播放器提供Windows系统媒体会话信息时才会显示歌名/歌手。壁纸本身静音，不改变音乐播放。

若频谱不动，先检查是否仍在其他应用里、系统是否有输出声音、频谱开关是否打开，以及Wallpaper Engine音频响应是否启用。

## 纯视频版怎么添加

解压 `windows-video-eco.zip`，将 `wallpaper.mp4` 拖到Wallpaper Engine，或按上面的方式把整个文件夹复制进 `myprojects`。纯视频保留原片动态和原片里的雪，没有实时时钟、日期和音乐频谱。

## 可以清理什么

- 已复制到 `myprojects` 并确认能用后，可以删除原下载ZIP和下载目录里重复的解压副本。
- `使用说明.txt` 看完后可删；它不影响壁纸。
- **保留安装目录中的HTML、JS、CSS、project.json、preview.jpg和assets视频。** 它们用于加载、配置或预览。
- 不要删除原创意工坊目录、原视频，或其他壁纸的文件。更新版复制到专用文件夹即可。

已构建壁纸运行时不需要Python、Node或FFmpeg。黑屏或只有时钟时，检查 `assets/eco.webm` 是否跟随整个文件夹复制，以及是否误用了Mac版。
