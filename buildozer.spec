[app]

# 应用名称
title = Binarization

# 包名
package.name = binarization

# 包域名
package.domain = org.example

# 源代码目录
source.dir = .

# 源代码包含的文件
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 1.0

# 依赖的 Python 包
# 注意：使用 opencv recipe 而不是 opencv-python
requirements = python3,kivy==2.1.0,numpy,opencv,pillow,plyer,pyjnius,android

# Android 权限
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# Android API 版本
android.api = 31

# Android 最低 API 版本
android.minapi = 21

# Android NDK 版本
android.ndk = 25b

# Android SDK 版本
android.sdk = 31

# 应用图标（可选）
# icon.filename = %(source.dir)s/assets/icon.png

# 启动画面（可选）
# presplash.filename = %(source.dir)s/assets/presplash.png

# 方向（portrait=竖屏, landscape=横屏, all=全部）
orientation = portrait

# 全屏模式
fullscreen = 0

# Android 架构
android.archs = arm64-v8a,armeabi-v7a

# 日志级别
log_level = 2

# 是否使用 androidx
android.gradle_dependencies = 

# 启用 androidX
p4a.bootstrap = sdl2

[buildozer]

# 日志级别 (0 = error only, 1 = info, 2 = debug)
log_level = 2

# 警告级别
warn_on_root = 1

