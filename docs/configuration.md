# 配置

共享默认值在 `src/defaults.json`，两个版本只在 `versions/<版本>/profile.json` 覆盖差异。构建工具生成每个平台独立的 `config.js`；修改生成文件只影响该包，下次构建会覆盖。

| 参数 | 默认值 | 作用 / 开销 |
| --- | --- | --- |
| `quality` | `eco` | 720p24；仅能选择包中存在的视频 |
| `fps` | 12 | 雪花和频谱共用帧率；eco档最高12 |
| `particles` | lite=0，snow=24 | 额外雪花，0–80；0时释放雪花画布主体 |
| `spectrum` | true | 半圆音频频谱；关闭后不处理音频和绘制频谱 |
| `sensitivity` | 1.5 | 音频灵敏度，0.1–5 |
| `clock` / `date` | true | 时钟和日期，默认每分钟刷新 |
| `seconds` | false | true时每秒更新时间，多一次定时唤醒 |
| `hour24` | false | true为24小时制 |
| `englishDate` | true | false为中文日期 |
| `hudX` / `hudY` | 50 | 文字和半圆位置，百分比 |
| `hudScale` | 1 | 0.5–1.5倍大小 |
| `dim` | 0.08 | 背景压暗程度，0–0.6 |
| `color` | 白色 | 文字、雪花和频谱颜色 |
| `media` | true | Windows系统媒体标题；Mac没有歌名接口 |
| `caption` / `captionArtist` | 空 | 没有媒体标题时使用的静态文字 |

Windows可直接在壁纸属性中调整大部分参数；Mac通过编辑生成的 `config.js` 后重新导入。`videoSources` 由构建工具维护，指向包内的实际视频，不需要自行设置。

“仅桌面动画”是宿主的播放规则，不能靠某个JS布尔值独立实现。详见平台安装文档。
