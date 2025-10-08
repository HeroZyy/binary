# 📱 Google Colab APK 打包完整指南

## 🎯 重要说明

### Android 支持的包

在 Android 打包时，**不能直接使用 PyPI 的包**，必须使用 `python-for-android` 的 **recipes**。

#### ✅ 支持的包（recipes）

| PyPI 包名 | Buildozer 中使用 | 说明 |
|-----------|-----------------|------|
| opencv-python | **opencv** | ⭐ 使用 opencv recipe |
| numpy | **numpy** | 直接支持 |
| pillow | **pillow** | 直接支持 |
| kivy | **kivy** | 直接支持 |
| plyer | **plyer** | 直接支持 |

#### ❌ 不支持的包

- `opencv-python` - 会导致打包失败
- `opencv-contrib-python` - 不支持
- `scipy` - 不支持（太大）

---

## 📋 准备工作

### 1. 检查项目文件

确保 `my_kivy_app` 文件夹包含以下文件：

```
my_kivy_app/
├── main.py              ✅ 主程序
├── buildozer.spec       ✅ 配置文件
├── requirements.txt     ✅ 依赖列表（仅供参考）
└── README.md           ✅ 说明文档
```

### 2. 检查 buildozer.spec 配置

**关键配置：**

```ini
[app]
# 应用名称
title = Auto Binarization Demo

# 包名（必须是唯一的）
package.name = binarization
package.domain = org.example

# 源代码目录
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 入口文件
source.main = main.py

# 版本
version = 1.0

# 依赖包（⭐ 重要：使用 opencv 而不是 opencv-python）
requirements = python3,kivy==2.1.0,numpy,opencv,pillow,plyer,pyjnius,android

# Android 配置
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
```

**⚠️ 关键点：**
- ✅ 使用 `opencv`（recipe）
- ❌ 不要使用 `opencv-python`（会失败）

---

## 🚀 Colab 打包流程

### 步骤 1：上传项目到 Google Drive

1. 打开 Google Drive: https://drive.google.com/
2. 上传整个 `my_kivy_app` 文件夹
3. 记住路径，例如：`/content/drive/MyDrive/my_kivy_app`

---

### 步骤 2：打开 Google Colab

1. 访问：https://colab.research.google.com/
2. 点击 "新建笔记本"
3. 将笔记本重命名为 "APK_Builder"

---

### 步骤 3：复制打包脚本

在 Colab 的代码单元格中，复制粘贴以下完整脚本：

```python
# ========================================
# Google Colab APK 打包脚本
# 适用于 my_kivy_app（OpenCV 版本）
# ========================================

print("="*80)
print("🚀 开始打包 APK（OpenCV 版本）")
print("="*80)

# ========================================
# 步骤 1：挂载 Google Drive
# ========================================
print("\n📁 步骤 1/9: 挂载 Google Drive...")
import os
if not os.path.exists('/content/drive/MyDrive'):
    from google.colab import drive
    drive.mount('/content/drive')
    print("✅ Google Drive 已挂载")
else:
    print("✅ Google Drive 已经挂载")

# ========================================
# 步骤 2：配置项目路径
# ========================================
print("\n📂 步骤 2/9: 配置项目路径...")

# ⚠️ 修改这里为您的实际路径
project_path = '/content/drive/MyDrive/my_kivy_app'

if not os.path.exists(project_path):
    print(f"❌ 错误：项目路径不存在: {project_path}")
    print("\n💡 请修改 project_path 为您的实际路径")
    print("   例如：project_path = '/content/drive/MyDrive/my_kivy_app'")
    raise FileNotFoundError(f"项目路径不存在: {project_path}")

print(f"✅ 项目路径: {project_path}")

# ========================================
# 步骤 3：安装 Buildozer
# ========================================
print("\n📦 步骤 3/9: 安装 Buildozer...")
!pip install -q buildozer cython==0.29.33
print("✅ Buildozer 安装完成")

# ========================================
# 步骤 4：安装系统依赖
# ========================================
print("\n🔧 步骤 4/9: 安装系统依赖...")
!sudo apt update -qq
!sudo apt install -y -qq \
    git zip unzip openjdk-11-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev \
    libffi-dev libssl-dev \
    cmake

print("✅ 系统依赖安装完成")

# ========================================
# 步骤 5：进入项目目录
# ========================================
print("\n📂 步骤 5/9: 进入项目目录...")
%cd {project_path}
print(f"✅ 当前目录: {os.getcwd()}")

# ========================================
# 步骤 6：验证文件
# ========================================
print("\n✅ 步骤 6/9: 验证项目文件...")

required_files = ['main.py', 'buildozer.spec']
missing_files = []

for file in required_files:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} - 缺失！")
        missing_files.append(file)

if missing_files:
    print(f"\n❌ 错误：缺少必要文件: {missing_files}")
    raise FileNotFoundError(f"缺少文件: {missing_files}")

print("\n✅ 所有必要文件都存在")

# ========================================
# 步骤 7：检查 buildozer.spec 配置
# ========================================
print("\n🔍 步骤 7/9: 检查 buildozer.spec 配置...")

with open('buildozer.spec', 'r') as f:
    spec_content = f.read()
    
    print("\n检查依赖配置：")
    
    # 检查是否使用了错误的 opencv-python
    if 'opencv-python' in spec_content:
        print("  ❌ 错误：检测到 opencv-python")
        print("     这会导致打包失败！")
        print("\n  💡 修复建议：")
        print("     将 requirements 中的 opencv-python 改为 opencv")
        print("\n  是否自动修复？(y/n)")
        
        # 自动修复
        spec_content = spec_content.replace('opencv-python', 'opencv')
        with open('buildozer.spec', 'w') as f_out:
            f_out.write(spec_content)
        print("  ✅ 已自动修复：opencv-python → opencv")
    elif 'opencv' in spec_content:
        print("  ✅ 配置正确：使用 opencv recipe")
    else:
        print("  ⚠️  警告：未检测到 opencv 依赖")
    
    # 显示 requirements 配置
    import re
    req_match = re.search(r'requirements\s*=\s*(.+)', spec_content)
    if req_match:
        requirements = req_match.group(1)
        print(f"\n  📋 当前依赖: {requirements}")

print("\n✅ 配置检查完成")

# ========================================
# 步骤 8：清理旧构建（可选）
# ========================================
print("\n🧹 步骤 8/9: 清理旧构建...")

if os.path.exists('.buildozer'):
    print("  发现旧的构建缓存")
    print("  💡 提示：")
    print("     - 首次打包：建议清理（输入 y）")
    print("     - 重新打包：保留缓存可加快速度（输入 n）")
    
    # 自动决策：如果 bin 目录存在，说明之前打包过，保留缓存
    if os.path.exists('bin'):
        print("  ⏭️  检测到之前的打包，保留缓存以加快速度")
    else:
        print("  🗑️  首次打包，清理缓存...")
        !rm -rf .buildozer bin
        print("  ✅ 已清理")
else:
    print("  ✅ 无需清理")

# ========================================
# 步骤 9：打包 APK
# ========================================
print("\n🔨 步骤 9/9: 开始打包 APK...")
print("="*80)
print("⏰ 预计时间：60 分钟")
print("="*80)
print("\n📊 打包进度说明：")
print("  1. 下载 Android SDK/NDK: 10-15 分钟")
print("  2. 编译 Python: 5-10 分钟")
print("  3. 编译 Kivy: 5-10 分钟")
print("  4. 编译 OpenCV: 15-20 分钟 ⭐ 最耗时")
print("  5. 编译 NumPy: 5-10 分钟")
print("  6. 编译 Pillow: 3-5 分钟")
print("  7. 打包 APK: 3-5 分钟")
print("\n💡 提示：")
print("  - 请保持浏览器标签页打开")
print("  - 不要关闭 Colab 页面")
print("  - 可以最小化窗口，但不要关闭")
print("\n开始打包...\n")
print("="*80)

# 开始打包
!buildozer -v android debug

# ========================================
# 步骤 10：检查打包结果
# ========================================
print("\n" + "="*80)
print("📊 检查打包结果")
print("="*80)

if os.path.exists('bin'):
    apk_files = [f for f in os.listdir('bin') if f.endswith('.apk')]
    
    if apk_files:
        print(f"\n✅ 打包成功！找到 {len(apk_files)} 个 APK 文件：\n")
        
        for apk in apk_files:
            apk_path = os.path.join('bin', apk)
            size_mb = os.path.getsize(apk_path) / 1024 / 1024
            print(f"  📦 {apk}")
            print(f"     大小: {size_mb:.1f} MB")
            print(f"     路径: {apk_path}\n")
        
        # ========================================
        # 步骤 11：下载 APK
        # ========================================
        print("="*80)
        print("📥 下载 APK")
        print("="*80)
        
        from google.colab import files
        
        for apk in apk_files:
            apk_path = os.path.join('bin', apk)
            print(f"\n正在下载: {apk}...")
            files.download(apk_path)
            print(f"✅ {apk} 已开始下载！")
        
        print("\n" + "="*80)
        print("🎊 打包完成！")
        print("="*80)
        print("\n📱 下一步：")
        print("  1. 等待浏览器下载完成")
        print("  2. 将 APK 传输到 Android 手机")
        print("  3. 在手机上安装 APK（允许未知来源）")
        print("  4. 打开应用测试功能")
        print("\n✅ 全部完成！")
        
    else:
        print("\n❌ 打包失败：未找到 APK 文件")
        print("\n💡 故障排除：")
        print("  1. 查看上面的错误信息")
        print("  2. 检查 buildozer.spec 配置")
        print("  3. 确认使用 opencv（不是 opencv-python）")
        print("  4. 查看完整日志：")
        print("     !tail -n 100 .buildozer/android/platform/build-*/build.log")
else:
    print("\n❌ 打包失败：bin 目录不存在")
    print("\n💡 故障排除：")
    print("  1. 查看上面的错误信息")
    print("  2. 运行：!ls -la")
    print("  3. 查看日志：")
    print("     !find .buildozer -name 'build.log' -exec tail -n 50 {} \\;")

print("\n" + "="*80)
```

---

### 步骤 4：运行脚本

1. 点击代码单元格左侧的 ▶️ 运行按钮
2. 或按 `Ctrl+Enter` (Windows) / `Cmd+Enter` (Mac)

---

### 步骤 5：授权 Google Drive

首次运行时会要求授权：

1. 点击授权链接
2. 选择您的 Google 账号
3. 允许访问 Google Drive
4. 复制授权码
5. 粘贴到 Colab 输入框

---

### 步骤 6：等待打包完成

**预计时间：60 分钟**

**进度说明：**
```
📁 步骤 1/9: 挂载 Google Drive... (1 分钟)
📂 步骤 2/9: 配置项目路径... (1 秒)
📦 步骤 3/9: 安装 Buildozer... (2 分钟)
🔧 步骤 4/9: 安装系统依赖... (3 分钟)
📂 步骤 5/9: 进入项目目录... (1 秒)
✅ 步骤 6/9: 验证项目文件... (1 秒)
🔍 步骤 7/9: 检查配置... (1 秒)
🧹 步骤 8/9: 清理旧构建... (可选)
🔨 步骤 9/9: 打包 APK... (50-60 分钟) ⭐
  - 下载 SDK/NDK (10 分钟)
  - 编译 Python (8 分钟)
  - 编译 Kivy (8 分钟)
  - 编译 OpenCV (20 分钟) ⭐ 最耗时
  - 编译 NumPy (8 分钟)
  - 编译 Pillow (5 分钟)
  - 打包 APK (5 分钟)
```

**💡 提示：**
- 保持浏览器标签页打开
- 不要关闭 Colab 页面
- 可以做其他事情，但定期检查进度

---

### 步骤 7：下载 APK

打包成功后，脚本会自动下载 APK：

```
✅ 打包成功！找到 1 个 APK 文件：

  📦 binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk
     大小: 55.3 MB
     路径: bin/binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk

📥 下载 APK
正在下载: binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk...
✅ binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk 已开始下载！
```

浏览器会自动下载 APK 文件。

---

## 📱 安装到 Android 手机

### 步骤 1：传输 APK

**方法 1：USB 线**
1. 用 USB 线连接手机和电脑
2. 将 APK 复制到手机存储

**方法 2：云盘**
1. 上传 APK 到 Google Drive / OneDrive
2. 在手机上下载

**方法 3：邮件**
1. 将 APK 作为附件发送到自己的邮箱
2. 在手机上下载附件

---

### 步骤 2：允许未知来源

**Android 8.0+：**
1. 设置 → 安全 → 安装未知应用
2. 选择文件管理器
3. 允许安装未知应用

**Android 7.0 及以下：**
1. 设置 → 安全
2. 勾选"未知来源"

---

### 步骤 3：安装 APK

1. 在手机上打开 APK 文件
2. 点击"安装"
3. 等待安装完成
4. 点击"打开"

---

### 步骤 4：授予权限

首次打开应用时：
1. 允许访问存储空间
2. 允许访问相机（如果需要）

---

### 步骤 5：测试功能

1. 点击 "Select Image"
2. 从相册选择一张文档照片
3. 查看左右对比效果
4. 点击 "Save Result" 保存结果
5. 检查保存的图片（在 `/Pictures/BinarizationDemo/`）

---

## ⚠️ 常见问题

### 问题 1：opencv-python 打包失败

**错误：**
```
Could not find a version that satisfies the requirement opencv-python
```

**原因：** 使用了 PyPI 的 `opencv-python` 而不是 recipe 的 `opencv`

**解决：**

修改 `buildozer.spec`：
```ini
# 错误
requirements = python3,kivy==2.1.0,opencv-python,numpy,...

# 正确
requirements = python3,kivy==2.1.0,opencv,numpy,...
```

脚本会自动检测并修复此问题。

---

### 问题 2：Colab 超时

**错误：**
```
Session timeout
```

**原因：** 免费版 Colab 有运行时间限制

**解决：**
1. 使用 Colab Pro（更长运行时间）
2. 保留 `.buildozer` 缓存，下次继续
3. 定期点击页面保持活跃

---

### 问题 3：内存不足

**错误：**
```
Killed (OOM)
```

**解决：**

在 `buildozer.spec` 中添加：
```ini
[app:android]
android.gradle_dependencies =
android.add_compile_options = -j1
```

---

### 问题 4：APK 安装失败

**错误：**
```
应用未安装
```

**解决：**
1. 检查手机是否允许未知来源
2. 卸载旧版本（如果有）
3. 检查手机存储空间（至少 100MB）
4. 重新下载 APK（可能下载损坏）

---

## 📊 打包时间估算

| 步骤 | 时间 | 说明 |
|------|------|------|
| 挂载 Drive | ~1min | 快速 |
| 安装 Buildozer | ~2min | 快速 |
| 安装系统依赖 | ~3min | 中等 |
| 下载 SDK/NDK | ~10min | 较慢 |
| 编译 Python | ~8min | 较慢 |
| 编译 Kivy | ~8min | 较慢 |
| **编译 OpenCV** | **~20min** | **最慢** ⭐ |
| 编译 NumPy | ~8min | 较慢 |
| 编译 Pillow | ~5min | 中等 |
| 打包 APK | ~5min | 中等 |
| **总计** | **~60min** | |

---

## 🎯 优化建议

### 1. 保留缓存

第一次打包后，`.buildozer` 目录会缓存编译结果。

**下次打包时间：** ~10 分钟（如果代码没有大改动）

### 2. 减少依赖

如果不需要某些功能，可以移除依赖：

```ini
# 最小配置
requirements = python3,kivy==2.1.0,numpy,opencv

# 完整配置
requirements = python3,kivy==2.1.0,numpy,opencv,pillow,plyer,pyjnius,android
```

### 3. 使用 Colab Pro

- 更长的运行时间
- 更快的 GPU/CPU
- 优先访问资源

---

## ✅ 成功标志

打包成功后，您会看到：

```
✅ 打包成功！找到 1 个 APK 文件：

  📦 binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk
     大小: 55.3 MB
     路径: bin/binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk

🎊 打包完成！
```

APK 会自动下载到您的电脑。

---

**祝您打包顺利！🚀**

