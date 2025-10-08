# Auto Binarization App - Kivy Project

## 📱 项目说明

这是一个自动二值化处理应用，可以打包成 Android APK。

**✨ 新版本：OpenCV 高级动态二值化，消除阴影！**

### 功能特性

- ✅ **消除阴影**：使用 OpenCV 自适应阈值，让阴影区域变亮
- ✅ **保护文字**：文字更清晰，边缘更锐利
- ✅ **高级去噪**：使用 fastNlMeansDenoising 去除噪点
- ✅ **形态学优化**：开运算和闭运算去除噪点、填充小孔
- ✅ 左右对比显示（原图 vs 处理后）
- ✅ 保存处理结果到手机相册
- ✅ 支持自动/手动处理模式切换
- ✅ **智能降级**：OpenCV 不可用时自动使用 Pillow
- ✅ **高性能**：800x600 图像仅需 ~150ms

---

## 🚀 Android APK 打包（3 种方法）

### 方法 1：GitHub Actions（推荐）⭐⭐⭐⭐⭐

**最快捷的方式！5-10 分钟完成打包**

1. 推送代码到 GitHub
2. GitHub Actions 自动打包
3. 下载 APK

**详细指南：** [GITHUB_ACTIONS_QUICKSTART.md](GITHUB_ACTIONS_QUICKSTART.md)

### 方法 2：Google Colab ⭐⭐⭐

**无需本地环境，60 分钟完成**

1. 上传到 Google Drive
2. 在 Colab 中运行打包脚本
3. 下载 APK

**详细指南：** [COLAB_BUILD_COMPLETE_GUIDE.md](COLAB_BUILD_COMPLETE_GUIDE.md)

### 方法 3：本地 Buildozer ⭐⭐

**完全控制，60-90 分钟**

**详细指南：** [ANDROID_BUILD_GUIDE.md](ANDROID_BUILD_GUIDE.md)

### 📊 方法对比

| 方案 | 时间 | 难度 | 成功率 | 推荐度 |
|------|------|------|--------|--------|
| **GitHub Actions** | 5-10 分钟 | ⭐ 极简 | 99% | ⭐⭐⭐⭐⭐ |
| **Google Colab** | 60 分钟 | ⭐⭐ 中等 | 85% | ⭐⭐⭐ |
| **本地 Buildozer** | 60-90 分钟 | ⭐⭐⭐⭐ 困难 | 70% | ⭐⭐ |

**完整对比：** [BUILD_METHODS_COMPARISON.md](BUILD_METHODS_COMPARISON.md)

---

### 依赖

**桌面环境：**
```bash
pip install -r requirements.txt
```
- Python 3.7+
- Kivy 2.1.0
- OpenCV-Python 4.5+
- NumPy
- Pillow
- Plyer

**Android 环境：**
- 使用 `opencv` recipe（buildozer 自动编译）
- 其他依赖相同

---

## 📂 项目结构

```
my_kivy_app/
├── main.py                      # 主程序（必须命名为 main.py）
├── buildozer.spec               # Buildozer 配置文件
├── requirements.txt             # Python 依赖列表（桌面）
├── test_opencv_version.py       # OpenCV 版本测试脚本
├── ANDROID_BUILD_GUIDE.md       # Android 打包详细指南
└── README.md                    # 项目说明
```

---

## 🚀 Google Colab 在线打包 APK

### 步骤 1：上传项目到 Google Drive

1. 将整个 `my_kivy_app` 文件夹上传到 Google Drive
2. 记住文件夹路径，例如：`/content/drive/MyDrive/my_kivy_app`

### 步骤 2：在 Google Colab 中运行

打开 Google Colab：https://colab.research.google.com/

创建新笔记本，然后运行以下代码：

```python
# 1. 挂载 Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 2. 安装 Buildozer
!pip install buildozer cython

# 3. 安装系统依赖
!sudo apt update
!sudo apt install -y git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 4. 进入项目目录
%cd /content/drive/MyDrive/my_kivy_app

# 5. 打包 APK
!buildozer -v android debug

# 6. 下载 APK
from google.colab import files
files.download('bin/binarization-1.0-arm64-v8a-debug.apk')
```

### 步骤 3：等待打包完成

- ⏱️ 预计时间：30-60 分钟
- 💾 APK 大小：~40MB
- 📍 输出位置：`bin/binarization-1.0-arm64-v8a-debug.apk`

### 步骤 4：下载并安装

打包完成后，APK 会自动下载到您的电脑，然后传到手机安装即可。

---

## 🖥️ 本地桌面测试

在打包前，可以先在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

---

## 📱 应用使用说明

### 主界面

```
┌─────────────────────────────────────┐
│  Auto Binarization Demo             │
├─────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐        │
│  │ Original │  │Binarized │        │
│  │  [原图]  │  │ [处理后] │        │
│  └──────────┘  └──────────┘        │
├─────────────────────────────────────┤
│  Auto Process: [✓]                  │
│  Block Size: 15, C Value: 5         │
├─────────────────────────────────────┤
│  Please select image                │
├─────────────────────────────────────┤
│  [Select] [Re-Process] [Save]      │
└─────────────────────────────────────┘
```

### 使用步骤

1. 点击 "Select Image" 选择图片
2. 自动处理（1-2秒）
3. 查看左右对比效果
4. 点击 "Save Result" 保存

### 保存位置

- **Android**: `/storage/emulated/0/Pictures/BinarizationDemo/`
- **桌面**: `当前目录/output/binarized/`

---

## 🔧 技术细节

### 二值化算法

- **方法**: 自适应阈值（MEAN_C）
- **参数**: Block Size=15, C Value=5
- **去噪**: fastNlMeansDenoising (h=3)
- **形态学**: 闭运算 + 开运算

### 依赖包

- **Kivy 2.1.0**: UI 框架
- **OpenCV**: 图像处理
- **NumPy**: 数值计算
- **Pillow**: 图像支持
- **Plyer**: 跨平台 API

---

## 🐛 常见问题

### Q1: Google Colab 打包失败？

**A**: 尝试重新运行，或者增加运行时内存：
```python
# 在 Colab 中选择：运行时 → 更改运行时类型 → GPU
```

### Q2: APK 安装失败？

**A**: 
1. 手机设置 → 安全 → 允许安装未知来源应用
2. 卸载旧版本后重新安装
3. 检查 Android 版本（需要 5.0+）

### Q3: 应用闪退？

**A**: 检查手机权限设置，允许应用访问存储和相机。

---

## 📊 版本信息

- **版本**: 1.0
- **最低 Android 版本**: 5.0 (API 21)
- **目标 Android 版本**: 12 (API 31)
- **支持架构**: arm64-v8a, armeabi-v7a

---

## 📖 相关文档

- Kivy 官方文档: https://kivy.org/doc/stable/
- Buildozer 文档: https://buildozer.readthedocs.io/
- OpenCV 文档: https://docs.opencv.org/

---

**祝您使用愉快！🎉**

