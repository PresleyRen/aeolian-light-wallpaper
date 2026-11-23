// Mac: 修改后重新导入整个文件夹；Windows: 也可以直接在壁纸属性中调整。
// 不需要联网、不需要 Spotify 密钥。
window.AEOLIAN_CONFIG = {
  quality: 'balanced',  // balanced=1080p约30帧；eco=720p24帧
  fps: 12,             // 特效默认12帧，雪花/频谱共用一个调度器
  clock: true,
  date: true,
  hour24: false,
  seconds: false,
  englishDate: true,    // false=中文日期
  spectrum: true,       // 音乐停止时频谱回到静态半圆
  sensitivity: 1.5,
  particles: 24,        // 少量额外雪花；可设0–80，原视频也有雪花
  dim: 0.08,           // 背景压暗，范围0–0.6
  hudX: 50,            // 整组文字/半圆中心横坐标，百分比
  hudY: 50,            // 整组中心纵坐标，百分比
  hudScale: 1,
  color: '#ffffff',
  media: true,         // Windows系统媒体标题；Mac当前接口不提供歌名
  caption: '',         // Mac可填静态文字；不会伪装成实时歌曲
  captionArtist: ''
};
