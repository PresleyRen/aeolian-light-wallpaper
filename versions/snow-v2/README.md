# snow-v2 / 雪花版

额外雪花默认24片，保留时钟、日期与音乐频谱。Windows和Mac统一默认720p24视频、12fps特效。

雪花采用三组透明度批量绘制；静止频谱跳过计算和绘制；宿主暂停时停止视频、时钟、绘制与音频计时器。核心代码共享 `src/`。

构建：`python tools/build.py --version snow-v2 --mode interactive --zip`

生成 `dist/windows/snow-v2/` 与 `dist/muro/snow-v2/`；桌面前台播放规则需要按平台文档在宿主开启。
