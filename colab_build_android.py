"""
Google Colab APK 打包脚本
适用于 my_kivy_app（OpenCV 版本）

使用方法：
1. 上传 my_kivy_app 文件夹到 Google Drive
2. 在 Google Colab 中运行此脚本
3. 等待 60 分钟
4. 下载 APK

⚠️ 重要：修改 project_path 为您的实际路径
"""

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

# ⚠️⚠️⚠️ 修改这里为您的实际路径 ⚠️⚠️⚠️
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
        print("\n  💡 自动修复中...")
        
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
    print("     - 首次打包：建议清理")
    print("     - 重新打包：保留缓存可加快速度")
    
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

