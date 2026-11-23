# Mac：下载后添加到 Muro

## 1. 下载Mac包并解压

| 想要的效果 | 完整安装包 | 解压后的文件夹 |
| --- | --- | --- |
| 省电，保留时钟/日期/频谱 | `muro-lite-v1.zip` | `muro-lite-v1` |
| 雪花、时钟/日期/频谱 | `muro-snow-v2.zip` | `muro-snow-v2` |
| 优先续航的纯视频 | `muro-video-eco.zip` | `muro-video-eco` |

在Finder中双击ZIP解压。Safari有时会自动解压；看到上述文件夹就可以继续。不要用Windows包代替Mac包。

GitHub的Code → Download ZIP是源码，通常名为 `aeolian-light-wallpaper-main.zip`，不包含视频。仓库目前未发布Release安装附件；请使用项目交付的完整安装包，或按[构建教程](build.md)生成。

以雪花版为例，应看到：

```text
muro-snow-v2/
  index.html
  app.js
  adapter.js
  config.js
  style.css
  still.jpg
  使用说明.txt
  assets/
    eco.mp4
```

## 2. 打开支持互动壁纸的Muro

先安装并打开 [Muro](https://github.com/MrRockySL/Muro)。需要支持 **Interactive Wallpapers / 互动壁纸** 的版本；如果添加窗口只能选视频，请更新到支持HTML导入的版本。

进入 **Library / 资料库**，找到添加/导入入口。界面语言和版本不同，按钮可能显示Add、Import或加号。

## 3. 导入整个文件夹

选择 `muro-snow-v2` 整个文件夹导入；也可把完整文件夹拖入资料库。

如果文件选择窗口让你选择网页，就选该文件夹内的 `index.html`。`index.html` 必须和脚本、still.jpg、assets一起保留；不要把HTML单独移到“下载”文件夹再导入，也不要选源码仓库根目录。

导入后选中标题包含 **Aeolian Light · snow-v2 · 雪花版 · Muro** 的项目，应用到Desktop / 桌面。省电版标题包含 `lite-v1 · 省电版`，便于区分。

互动版保留实时钟表、日期和频谱，用于桌面；锁屏/屏保请选择纯视频方式。[Muro导入说明](https://github.com/MrRockySL/Muro#wallpapers-that-react-to-you)

## 4. 开启仅桌面播放和音频

在Muro设置中开启 **Play only on desktop / 仅在桌面播放**。切到应用后由Muro暂停背景、雪花与频谱，回到桌面后恢复并刷新时间。

系统提示Muro需要音频权限时，由你允许相应系统音频权限。然后播放音乐并回到桌面检查频谱。页面不采集麦克风，不需要Spotify令牌或联网。

Mac版目前没有实时歌名/歌手，因为Muro桥接接口不提供这些信息；半圆音乐频谱仍可响应系统声音。没有声音时，频谱保持静态。

## 5. 调整雪花、日期和时间

用纯文本编辑器打开完整文件夹内的 `config.js`：

- `particles: 24`：24片额外雪花，可改成12或0。
- `hour24: true`：24小时制。
- `englishDate: false`：中文日期。
- `spectrum: true`：显示频谱。

保存时保留 `.js` 后缀和纯文本格式。Muro导入时会复制文件；修改源文件夹后，需要删除旧的导入条目，再导入修改后的完整文件夹。只修改下载文件夹中的配置，不会自动更新已导入副本。

默认包只有720p24视频；不要直接把quality改为不存在的1080p文件。需要双画质时，用构建工具的 `--quality both` 生成完整资源。

## 纯视频版怎么添加

解压 `muro-video-eco.zip`，在Muro的资料库添加/导入 `wallpaper.mp4`，或直接拖入该MP4。Muro会按自己的视频流程处理。

纯视频保留原片动态与原片里的雪，不带实时钟表、日期和频谱。可使用Muro支持的锁屏/屏保功能，具体依宿主和macOS版本而定。

## 可以清理什么

- 确认Muro导入并正常显示后，可以删除下载ZIP；Muro保存的是导入副本。
- 后续若想修改配置，建议保留一份完整解压目录作为编辑副本。
- `使用说明.txt` 可删；`index.html`、JS、CSS、still.jpg和assets视频应一起保留。
- 不要进入Muro管理的库目录手工删视频，也不要删除你原来的素材。

黑屏或只显示时间时，确认 `assets/eco.mp4` 存在、使用的是Mac包，并且导入的是完整文件夹。默认已是720p24视频、12fps特效；无需安装开发工具运行完整包。代码尚未在真实Mac/Muro硬件上做性能实测。
