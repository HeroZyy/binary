"""
Google Colab APK 打包脚本（OpenCV 版本）
复制此代码到 Google Colab 运行
"""

print("="*80)
print("🚀 开始打包 APK（OpenCV 版本）")
print("="*80)

# ========================================
# 步骤 1：挂载 Google Drive
# ========================================
print("\n📁 步骤 1/8: 挂载 Google Drive...")
import os
if not os.path.exists('/content/drive/MyDrive'):
    from google.colab import drive
    drive.mount('/content/drive')
    print("✅ Google Drive 已挂载")
else:
    print("✅ Google Drive 已经挂载")

# ========================================
# 步骤 2：安装 Buildozer
# ========================================
print("\n📦 步骤 2/8: 安装 Buildozer...")
!pip install -q buildozer cython==0.29.33
print("✅ Buildozer 安装完成")

# ========================================
# 步骤 3：安装系统依赖
# ========================================
print("\n🔧 步骤 3/8: 安装系统依赖...")
!sudo apt update -qq
!sudo apt install -y -qq \
    git zip unzip openjdk-11-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev \
    libffi-dev libssl-dev \
    cmake
print("✅ 系统依赖安装完成")

# ========================================
# 步骤 4：进入项目目录
# ========================================
print("\n📂 步骤 4/8: 进入项目目录...")

# ⚠️ 修改这里为您的项目路径
project_path = '/content/drive/MyDrive/my_kivy_app'

if not os.path.exists(project_path):
    print(f"❌ 错误：项目路径不存在: {project_path}")
    print("\n💡 请修改 project_path 为您的实际路径")
    print("   例如：project_path = '/content/drive/MyDrive/my_kivy_app'")
    raise FileNotFoundError(f"项目路径不存在: {project_path}")

%cd {project_path}
print(f"✅ 已进入项目目录: {project_path}")

# ========================================
# 步骤 5：验证文件
# ========================================
print("\n✅ 步骤 5/8: 验证项目文件...")

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
# 步骤 6：检查 buildozer.spec 配置
# ========================================
print("\n🔍 步骤 6/8: 检查 buildozer.spec 配置...")

with open('buildozer.spec', 'r') as f:
    spec_content = f.read()
    
    # 检查是否使用了正确的 opencv recipe
    if 'opencv-python' in spec_content:
        print("⚠️  警告：检测到 opencv-python，这会导致打包失败！")
        print("   应该使用 opencv（recipe）而不是 opencv-python")
        print("\n修复建议：")
        print("   将 requirements 中的 opencv-python 改为 opencv")
    elif 'opencv' in spec_content:
        print("✅ 配置正确：使用 opencv recipe")
    else:
        print("⚠️  警告：未检测到 opencv 依赖")

# ========================================
# 步骤 7：清理旧的构建（可选）
# ========================================
print("\n🧹 步骤 7/8: 清理旧的构建...")
if os.path.exists('.buildozer'):
    print("  发现旧的构建缓存")
    clean = input("  是否清理？(y/n，默认 n): ").strip().lower()
    if clean == 'y':
        !rm -rf .buildozer bin
        print("  ✅ 已清理")
    else:
        print("  ⏭️  保留缓存（可加快打包速度）")
else:
    print("  ✅ 无需清理")

# ========================================
# 步骤 8：打包 APK
# ========================================
print("\n🔨 步骤 8/8: 开始打包 APK...")
print("="*80)
print("⏰ 预计时间：60 分钟")
print("="*80)
print("\n📊 打包进度说明：")
print("  1. 下载 Android SDK/NDK: 10-15 分钟")
print("  2. 编译 Python: 5-10 分钟")
print("  3. 编译 Kivy: 5-10 分钟")
print("  4. 编译 OpenCV: 15-20 分钟 ⭐ 最耗时")
print("  5. 编译 NumPy: 5-10 分钟")
print("  6. 打包 APK: 3-5 分钟")
print("\n💡 提示：")
print("  - 请保持浏览器标签页打开")
print("  - 不要关闭 Colab 页面")
print("  - 可以最小化窗口，但不要关闭")
print("\n开始打包...\n")
print("="*80)

# 开始打包
!buildozer -v android debug

# ========================================
# 步骤 9：检查打包结果
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
        # 步骤 10：下载 APK
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
    print("  3. 查看日志：!tail -n 100 .buildozer/android/platform/build-*/build.log")

print("\n" + "="*80)

