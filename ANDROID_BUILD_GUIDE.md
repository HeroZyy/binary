# Android APK 打包指南（OpenCV 版本）

## 📋 重要说明

### OpenCV 依赖处理

**问题：** 不能直接使用 `opencv-python`，会导致打包失败

**解决方案：** 使用 `python-for-android` 的 `opencv` recipe

### 配置文件

#### buildozer.spec
```ini
requirements = python3,kivy==2.1.0,numpy,opencv,pillow,plyer,pyjnius,android
```

**注意：**
- ✅ 使用 `opencv`（recipe）
- ❌ 不要使用 `opencv-python`（PyPI 包）

#### requirements.txt（桌面环境）
```
kivy==2.1.0
opencv-python>=4.5.0  # 桌面环境使用
numpy>=1.19.0
pillow>=8.0.0
plyer>=2.0.0
```

---

## 🚀 Google Colab 打包流程

### 步骤 1：准备项目

确保项目结构正确：

```
my_kivy_app/
├── main.py              # 主程序
├── buildozer.spec       # 配置文件
├── requirements.txt     # 桌面依赖
└── README.md           # 说明文档
```

### 步骤 2：上传到 Google Drive

1. 打开 Google Drive: https://drive.google.com/
2. 上传整个 `my_kivy_app` 文件夹
3. 记住路径，例如：`/content/drive/MyDrive/my_kivy_app`

### 步骤 3：在 Google Colab 中打包

打开 Google Colab：https://colab.research.google.com/

创建新笔记本，运行以下代码：

```python
# ========================================
# Google Colab APK 打包脚本（OpenCV 版本）
# ========================================

print("🚀 开始打包 APK（OpenCV 版本）...")

# 1. 挂载 Google Drive
print("\n📁 步骤 1/7: 挂载 Google Drive...")
import os
if not os.path.exists('/content/drive/MyDrive'):
    from google.colab import drive
    drive.mount('/content/drive')
    print("✅ Google Drive 已挂载")
else:
    print("✅ Google Drive 已经挂载")

# 2. 安装 Buildozer
print("\n📦 步骤 2/7: 安装 Buildozer...")
!pip install -q buildozer cython==0.29.33

# 3. 安装系统依赖
print("\n🔧 步骤 3/7: 安装系统依赖...")
!sudo apt update -qq
!sudo apt install -y -qq \
    git zip unzip openjdk-11-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev \
    libffi-dev libssl-dev \
    cmake

# 4. 进入项目目录
print("\n📂 步骤 4/7: 进入项目目录...")
project_path = '/content/drive/MyDrive/my_kivy_app'  # 修改为您的路径
%cd {project_path}

# 5. 验证文件
print("\n✅ 步骤 5/7: 验证项目文件...")
!ls -la main.py buildozer.spec

# 6. 清理旧的构建（可选）
print("\n🧹 步骤 6/7: 清理旧的构建...")
!rm -rf .buildozer bin

# 7. 打包 APK
print("\n🔨 步骤 7/7: 开始打包 APK...")
print("⏰ 预计时间：40-60 分钟")
print("📊 进度说明：")
print("  - 下载 Android SDK/NDK: 10-15 分钟")
print("  - 编译 Python: 5-10 分钟")
print("  - 编译 Kivy: 5-10 分钟")
print("  - 编译 OpenCV: 15-20 分钟 ⭐ 最耗时")
print("  - 编译 NumPy: 5-10 分钟")
print("  - 打包 APK: 3-5 分钟")
print("\n开始打包...\n")

!buildozer -v android debug

# 8. 下载 APK
print("\n📥 步骤 8/7: 下载 APK...")
from google.colab import files
import os

apk_files = []
if os.path.exists('bin'):
    apk_files = [f for f in os.listdir('bin') if f.endswith('.apk')]

if apk_files:
    apk_path = os.path.join('bin', apk_files[0])
    print(f"✅ 找到 APK: {apk_path}")
    print(f"📦 文件大小: {os.path.getsize(apk_path) / 1024 / 1024:.1f} MB")
    
    # 下载 APK
    files.download(apk_path)
    print("✅ APK 已开始下载！")
else:
    print("❌ 未找到 APK 文件")
    print("💡 检查 bin/ 目录：")
    !ls -lh bin/

print("\n🎊 打包完成！")
```

---

## ⚠️ 常见问题

### 问题 1：OpenCV 编译失败

**错误信息：**
```
[ERROR] Could not find opencv recipe
```

**解决方案：**

检查 `buildozer.spec` 中的 requirements：
```ini
# 正确
requirements = python3,kivy==2.1.0,numpy,opencv,pillow,plyer,pyjnius,android

# 错误
requirements = python3,kivy==2.1.0,opencv-python,numpy,pillow,plyer,pyjnius,android
```

### 问题 2：编译超时

**错误信息：**
```
Colab session timeout
```

**解决方案：**

1. 使用 Colab Pro（更长的运行时间）
2. 分步打包：
   ```python
   # 第一次运行：下载依赖
   !buildozer android debug 2>&1 | head -n 100
   
   # 第二次运行：继续打包
   !buildozer android debug
   ```

### 问题 3：内存不足

**错误信息：**
```
Killed (OOM)
```

**解决方案：**

减少并行编译：

在 `buildozer.spec` 中添加：
```ini
[app:android]
android.gradle_dependencies =
android.add_compile_options = -j1
```

### 问题 4：NDK 版本问题

**错误信息：**
```
NDK version mismatch
```

**解决方案：**

在 `buildozer.spec` 中指定 NDK 版本：
```ini
android.ndk = 25b
```

---

## 📊 打包时间估算

| 步骤 | 时间 | 说明 |
|------|------|------|
| 挂载 Drive | ~10s | 快速 |
| 安装 Buildozer | ~30s | 快速 |
| 安装系统依赖 | ~2min | 中等 |
| 下载 SDK/NDK | ~10min | 较慢 |
| 编译 Python | ~8min | 较慢 |
| 编译 Kivy | ~8min | 较慢 |
| **编译 OpenCV** | **~20min** | **最慢** ⭐ |
| 编译 NumPy | ~8min | 较慢 |
| 打包 APK | ~5min | 中等 |
| **总计** | **~60min** | |

---

## 🎯 优化建议

### 1. 使用缓存

第一次打包后，`.buildozer` 目录会缓存编译结果。

**保留缓存：**
```python
# 不要删除 .buildozer 目录
# 下次打包会快很多（~10 分钟）
```

### 2. 减少依赖

如果不需要某些功能，可以移除依赖：

```ini
# 最小配置
requirements = python3,kivy==2.1.0,numpy,opencv

# 完整配置
requirements = python3,kivy==2.1.0,numpy,opencv,pillow,plyer,pyjnius,android
```

### 3. 使用预编译包

某些依赖有预编译版本，可以加快打包：

```ini
# 使用预编译的 NumPy
requirements = python3,kivy==2.1.0,numpy==1.19.3,opencv
```

---

## 📱 APK 信息

### 文件大小

- **OpenCV 版本：** ~50-60 MB
- **Pillow 版本：** ~30-40 MB

### 支持架构

```ini
android.archs = arm64-v8a,armeabi-v7a
```

- `arm64-v8a`：64 位 ARM（现代手机）
- `armeabi-v7a`：32 位 ARM（旧手机）

### 最低 Android 版本

```ini
android.minapi = 21  # Android 5.0
android.api = 31     # Android 12
```

---

## ✅ 验证打包结果

### 1. 检查 APK 文件

```python
import os

apk_files = [f for f in os.listdir('bin') if f.endswith('.apk')]
for apk in apk_files:
    size = os.path.getsize(f'bin/{apk}') / 1024 / 1024
    print(f"📦 {apk}: {size:.1f} MB")
```

### 2. 查看日志

```python
# 查看最后 50 行日志
!tail -n 50 .buildozer/android/platform/build-*/build.log
```

### 3. 测试 APK

1. 下载 APK 到手机
2. 安装（允许未知来源）
3. 打开应用
4. 测试功能：
   - 选择图片
   - 查看二值化效果
   - 保存结果

---

## 🎉 成功标志

打包成功后，您会看到：

```
# BUILD SUCCESSFUL
# APK created successfully!
# 📦 binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

APK 位置：
```
bin/binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

---

## 📞 获取帮助

如果遇到问题：

1. 查看完整日志：`.buildozer/android/platform/build-*/build.log`
2. 搜索错误信息
3. 检查 buildozer.spec 配置
4. 确认 requirements 正确

---

**祝您打包顺利！🚀**

