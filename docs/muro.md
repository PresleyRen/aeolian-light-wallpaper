# macOS / Muro

## 选择版本

| 构建目录 | 用途 | 默认视频 | 额外雪花 |
| --- | --- | --- | --- |
| `dist/muro/lite-v1` | 优先省电的互动版 | 720p24 H.264 | 0 |
| `dist/muro/snow-v2` | 雪花、时钟、日期、频谱 | 720p24 H.264 | 24 |
| `dist/muro/video-eco` | 原生纯视频方式 | 720p24 H.264 | 仅原视频里的雪 |

互动版默认特效12fps。此前Mac默认1080p；本次统一改为720p省电档。需要清晰档可用 `--quality both` 或 `--quality balanced` 构建。

## 导入与设置

1. 使用支持 Interactive Wallpapers 的 Muro 版本。
2. 在资料库导入完整的 `lite-v1` 或 `snow-v2` 文件夹；也可导入其中的 `index.html`，但脚本和assets必须一起保留。
3. 开启 **Play only on desktop / 仅在桌面播放**。
4. 允许Muro的系统音频权限后，频谱才会响应系统声音。页面不直接采集麦克风，也不需要联网。

Muro通过 `muro:audio` 提供音频频段，用 `muro:pause` / `muro:resume` 暂停和恢复背景视频、雪花及频谱。网页本身无法识别桌面前方所有应用窗口。

Muro当前桥接接口不提供歌名/歌手，因此Mac版保留音频频谱，歌名区域默认隐藏。`caption` 和 `captionArtist` 可放静态文字。

## 调整配置

用纯文本编辑器修改构建文件夹内的 `config.js`，例如雪花数量、中文日期、24小时制。Muro导入时会复制文件；修改源文件后，需要删除旧导入条目并重新导入完整文件夹。

默认eco-only包只有720p视频，不要手改为不存在的1080p路径。使用构建工具的 `--quality both` 提供两种视频后，才可把 `quality` 改为 `balanced`。

## 纯视频和锁屏

优先续航时，直接导入 `video-eco/wallpaper.mp4`。Muro会按自身的视频导入流程处理，不运行本项目的网页、时钟、日期或频谱。

互动版用于桌面；纯视频可使用宿主支持的锁屏/屏保能力，具体取决于Muro与macOS版本。

代码已做Chrome及Windows WebKit的事件模拟验证，未在真实Mac/Muro硬件上做性能测试。Mac实际CPU、统一内存和GPU功耗需要在对应机器测量。
