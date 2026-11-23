# lite-v1 / 省电版

额外雪花默认0；保留时钟、日期与音乐频谱。原视频里的雪花仍存在。

Windows和Mac统一默认720p24视频、12fps特效。核心代码共享 `src/`，此目录只保存版本配置，避免维护四份重复逻辑。此前的完整代码仍在Git历史中。

构建：`python tools/build.py --version lite-v1 --mode interactive --zip`

生成 `dist/windows/lite-v1/` 与 `dist/muro/lite-v1/`；按对应平台文档导入完整文件夹。
