# Google Colab 在线打包 APK 完整指南

## 🎯 优势

使用 Google Colab 打包 APK 的优势：
- ✅ 无需本地安装 Linux 环境
- ✅ 无需安装 Android SDK/NDK
- ✅ 免费使用 Google 的云端资源
- ✅ 打包速度快（高性能服务器）
- ✅ 随时随地可以打包

---

## 📋 准备工作

### 1. 准备项目文件

确保您有以下文件：
```
my_kivy_app/
├── main.py              ✅ 主程序
├── buildozer.spec       ✅ 配置文件
├── requirements.txt     ✅ 依赖列表
└── README.md           📖 说明文档
```

### 2. 上传到 Google Drive

1. 打开 Google Drive: https://drive.google.com/
2. 创建文件夹（可选）
3. 上传整个 `my_kivy_app` 文件夹
4. 记住路径，例如：`/content/drive/MyDrive/my_kivy_app`

---

## 🚀 打包步骤

### 步骤 1：打开 Google Colab

访问：https://colab.research.google.com/

点击 "新建笔记本"

### 步骤 2：复制粘贴打包代码

在 Colab 笔记本中，创建一个代码单元格，复制粘贴以下代码：

```python
# ========================================
# Google Colab APK 打包脚本
# ========================================

print("🚀 开始打包 APK...")

# 1. 挂载 Google Drive
print("\n📁 步骤 1/6: 挂载 Google Drive...")
from google.colab import drive
drive.mount('/content/drive')

# 2. 安装 Buildozer
print("\n📦 步骤 2/6: 安装 Buildozer...")
!pip install -q buildozer cython

# 3. 安装系统依赖
print("\n🔧 步骤 3/6: 安装系统依赖...")
!sudo apt update -qq
!sudo apt install -y -qq git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 4. 进入项目目录
print("\n📂 步骤 4/6: 进入项目目录...")
%cd /content/drive/MyDrive/my_kivy_app

# 5. 验证文件
print("\n✅ 验证项目文件...")
!ls -la main.py buildozer.spec

# 6. 打包 APK
print("\n🔨 步骤 5/6: 开始打包 APK（预计 30-60 分钟）...")
!buildozer -v android debug

# 7. 显示结果
print("\n🎉 步骤 6/6: 打包完成！")
!ls -lh bin/*.apk

# 8. 下载 APK
print("\n📥 下载 APK 到本地...")
from google.colab import files
import os

apk_files = [f for f in os.listdir('bin') if f.endswith('.apk')]
if apk_files:
    apk_path = os.path.join('bin', apk_files[0])
    print(f"✅ 找到 APK: {apk_path}")
    files.download(apk_path)
    print("✅ APK 已开始下载！")
else:
    print("❌ 未找到 APK 文件")

print("\n🎊 全部完成！")
```

### 步骤 3：修改项目路径

**重要：** 修改第 15 行的路径为您的实际路径：

```python
%cd /content/drive/MyDrive/my_kivy_app
```

改为您的实际路径，例如：
- `/content/drive/MyDrive/my_kivy_app`
- `/content/drive/MyDrive/projects/my_kivy_app`
- `/content/drive/MyDrive/kivy_apps/my_kivy_app`

### 步骤 4：运行代码

1. 点击代码单元格左侧的 ▶️ 按钮
2. 首次运行会要求授权访问 Google Drive
3. 点击链接，选择您的 Google 账号，允许访问
4. 等待打包完成

---

## ⏱️ 打包进度

### 预计时间

- **首次打包**: 30-60 分钟
- **后续打包**: 10-20 分钟（使用缓存）

### 进度显示

```
[INFO]    Downloading Android SDK...           # 5-10 分钟
[INFO]    Downloading Android NDK...           # 10-15 分钟
[INFO]    Downloading Python-for-Android...    # 2-3 分钟
[INFO]    Compiling Python...                  # 5-10 分钟
[INFO]    Compiling Kivy...                    # 5-10 分钟
[INFO]    Compiling OpenCV...                  # 5-10 分钟
[INFO]    Packaging APK...                     # 3-5 分钟
[INFO]    APK created successfully!            # 完成！
```

---

## 📥 下载 APK

### 自动下载

脚本会自动触发下载，APK 文件会下载到您的电脑。

### 手动下载

如果自动下载失败，可以手动下载：

```python
# 在 Colab 中运行
from google.colab import files
files.download('bin/binarization-1.0-arm64-v8a-debug.apk')
```

### 从 Google Drive 下载

APK 也会保存在 Google Drive 中：
```
/content/drive/MyDrive/my_kivy_app/bin/binarization-1.0-arm64-v8a-debug.apk
```

直接在 Google Drive 中下载即可。

---

## 🐛 常见问题

### Q1: 挂载 Google Drive 失败

**错误信息：**
```
Mounted at /content/drive
```

**解决方案：**
- 刷新页面重试
- 检查网络连接
- 清除浏览器缓存

### Q2: 找不到项目目录

**错误信息：**
```
/bin/bash: line 1: cd: /content/drive/MyDrive/my_kivy_app: No such file or directory
```

**解决方案：**
```python
# 列出 Google Drive 中的文件
!ls /content/drive/MyDrive/

# 找到正确的路径后修改代码
```

### Q3: 打包失败

**错误信息：**
```
Command failed: ...
```

**解决方案：**
```python
# 清理后重新打包
!buildozer android clean
!buildozer -v android debug
```

### Q4: 内存不足

**错误信息：**
```
Killed
```

**解决方案：**
1. 在 Colab 中选择：运行时 → 更改运行时类型 → 高 RAM
2. 或使用 Colab Pro（付费）

### Q5: 超时断开

**解决方案：**
- Colab 免费版有时间限制（12小时）
- 保持浏览器标签页打开
- 或使用 Colab Pro

---

## 💡 优化技巧

### 1. 使用 GPU 运行时

虽然打包不需要 GPU，但 GPU 运行时通常有更多内存：

```
运行时 → 更改运行时类型 → GPU
```

### 2. 保存缓存

首次打包后，`.buildozer` 文件夹会保存在 Google Drive 中，下次打包会更快。

### 3. 分步运行

可以将打包脚本分成多个单元格，方便调试：

```python
# 单元格 1: 挂载 Drive
from google.colab import drive
drive.mount('/content/drive')

# 单元格 2: 安装依赖
!pip install buildozer cython
!sudo apt install -y ...

# 单元格 3: 打包
%cd /content/drive/MyDrive/my_kivy_app
!buildozer -v android debug

# 单元格 4: 下载
from google.colab import files
files.download('bin/*.apk')
```

---

## 📊 完整打包脚本（一键运行）

```python
# ========================================
# 一键打包脚本（复制粘贴到 Colab）
# ========================================

# 挂载 Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 安装 Buildozer
!pip install -q buildozer cython

# 安装系统依赖
!sudo apt update -qq && sudo apt install -y -qq git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 进入项目目录（修改为您的路径）
%cd /content/drive/MyDrive/my_kivy_app

# 打包 APK
!buildozer -v android debug

# 下载 APK
from google.colab import files
import os
apk_files = [f for f in os.listdir('bin') if f.endswith('.apk')]
if apk_files:
    files.download(os.path.join('bin', apk_files[0]))
```

---

## ✅ 验证 APK

打包完成后，验证 APK：

```python
# 查看 APK 信息
!ls -lh bin/*.apk

# 应该显示类似：
# -rw-r--r-- 1 root root 42M Oct 8 14:30 binarization-1.0-arm64-v8a-debug.apk
```

---

## 📱 安装到手机

1. 下载 APK 到电脑
2. 通过微信/QQ/邮件发送到手机
3. 在手机上点击安装
4. 允许安装未知来源应用
5. 完成安装

---

## 🎉 总结

使用 Google Colab 打包 APK 的完整流程：

```
1. 准备项目文件
   ↓
2. 上传到 Google Drive
   ↓
3. 打开 Google Colab
   ↓
4. 复制粘贴打包脚本
   ↓
5. 修改项目路径
   ↓
6. 运行脚本（30-60 分钟）
   ↓
7. 下载 APK
   ↓
8. 安装到手机
```

**就这么简单！🚀**

---

## 📖 相关资源

- Google Colab: https://colab.research.google.com/
- Buildozer 文档: https://buildozer.readthedocs.io/
- Kivy 文档: https://kivy.org/doc/stable/

---

**祝您打包顺利！🎊**

