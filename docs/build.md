# 构建、资源与打包

## 资源边界

仓库保存共享代码、版本配置和构建工具。原视频、原画和预览图由使用者从自己的本地资源准备，不在Git中分发，也不自动联网下载。

已构建文件夹可以直接导入宿主，开发工具只在构建时需要。

## 默认一条构建路径

安装Python 3和FFmpeg，或者使用 `python -m pip install imageio-ffmpeg` 提供FFmpeg。将已有视频转成省电资源：

```sh
python tools/prepare_media.py --source "/path/to/original.webm"
python tools/build.py --zip
```

默认只准备720p24资源；生成两个平台、两个互动版本和各自的纯视频版。独立ZIP位于 `dist/packages/`，每个ZIP都有完整的本地资源和说明。

ZIP解压后的第一层名称带平台前缀，例如 `windows-snow-v2/` 和 `muro-snow-v2/`。代码文件、配置、视频和说明都在该目录内，导入这一层即可。

打包使用明确的必需文件列表：不包含源码目录、测试、缓存、临时文件或未引用的图片。Windows复用 `preview.jpg` 作为视频静态封面；Mac复用 `still.jpg` 作为封面和宿主静态背景。只保留一份必需的封面图，不额外复制到assets。

```text
dist/
  windows/
    lite-v1/       # 网页省电版，0额外雪花
    snow-v2/       # 网页雪花版，24片雪花
    video-eco/     # 原生H.264纯视频
  muro/
    lite-v1/       # HTML省电版
    snow-v2/       # HTML雪花版
    video-eco/     # 直接导入MP4
  packages/        # 六个独立ZIP
```

## 只构建需要的部分

```sh
# 仅Windows雪花互动版；只需要eco.webm和still.jpg
python tools/prepare_media.py --source "/path/to/original.webm" --format webm
python tools/build.py --platform windows --version snow-v2 --mode interactive --zip

# 仅Mac省电互动版
python tools/build.py --platform muro --version lite-v1 --mode interactive

# 仅Windows纯视频版，避免网页渲染层
python tools/build.py --platform windows --mode video

# 保留720p/1080p两个画质选项
python tools/prepare_media.py --source "/path/to/original.webm" --quality both
python tools/build.py --quality both --zip

# 复用已经准备好的资源，跳过重新编码
python tools/build.py --assets "/path/to/prepared-assets" --zip
```

支持 `--quality eco|balanced|both`、`--platform windows|muro|all`、`--version lite-v1|snow-v2|all` 和 `--mode interactive|video|all`。只校验当前目标需要的格式，Windows互动版不要求Mac视频资源。

资源文件名为 `eco.webm` / `eco.mp4`（720p24），`background.webm` / `background.mp4`（清晰档）和 `still.jpg`。清晰档保持输入尺寸并使用约30fps；以本项目原1080p输入构建时就是1080p。视频静音，完整保留原片长度，不新增首尾过渡。

构建目录会按所选画质移除该目标中已知的旧可选视频，防止eco-only包误带大文件。其他旧版本目录和ZIP不会自动删除；`dist/` 是生成结果，不提交Git。

构建只复制已经准备好的媒体，不会重编码或裁剪视频。只有显式运行 `prepare_media.py` 才进行转码；清理不会删除输入视频或宿主管理的原始壁纸。
