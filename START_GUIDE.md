# 🚀 启动指南

## 快速选择

- **想在电脑上测试？** → [方法 1：桌面环境](#方法-1桌面环境推荐先测试)
- **想打包成 Android APK？** → [方法 2：Android 打包](#方法-2android-打包)

---

## 方法 1：桌面环境（推荐先测试）

### ⏱️ 预计时间：5 分钟

### 步骤 1：安装依赖

打开命令行（Windows PowerShell / Mac Terminal / Linux Terminal），运行：

```bash
cd my_kivy_app
pip install -r requirements.txt
```

**等待安装完成**（约 2-3 分钟）

**预期输出：**
```
Successfully installed kivy-2.1.0 opencv-python-4.x.x numpy-1.x.x ...
```

---

### 步骤 2：运行测试（可选但推荐）

```bash
python test_opencv_version.py
```

**预期输出：**
```
✅ 使用 OpenCV 进行图像处理
✅ OpenCV 版本: 4.12.0

📐 测试尺寸: 800x600 (Medium)
   ⏱️  处理时间: 148.1 ms
   ✅ 完成

🎉 所有测试完成！
```

**查看结果：**
- 打开 `test_output_opencv/` 文件夹
- 查看处理前后的对比图片

---

### 步骤 3：运行主应用

```bash
python main.py
```

**预期界面：**

```
┌─────────────────────────────────────────────────────┐
│         Auto Binarization Demo                      │
├─────────────────────────────────────────────────────┤
│  [Select Image]  [Save Result]                      │
│  ☑ Auto Process                                     │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│    Original Image    │    Processed Image           │
│                      │                              │
│                      │                              │
├──────────────────────┴──────────────────────────────┤
│  Status: Ready                                      │
└─────────────────────────────────────────────────────┘
```

---

### 步骤 4：使用应用

1. **选择图片**
   - 点击 "Select Image" 按钮
   - 选择一张文档图片（JPG、PNG 等）

2. **自动处理**
   - 应用会自动进行二值化处理
   - 左侧显示原图
   - 右侧显示处理后的图片

3. **保存结果**
   - 点击 "Save Result" 按钮
   - 图片保存到 `output/binarized/` 文件夹
   - 文件名格式：`binarized_20251008_123456.jpg`

---

### 🎯 测试建议

**测试图片类型：**
- ✅ 手机拍照的文档（有阴影）
- ✅ 扫描仪扫描的文档
- ✅ 书籍拍照（装订处有阴影）
- ✅ 白板拍照（反光和阴影）

**查看效果：**
- 对比左右两侧的图片
- 检查文字是否清晰
- 检查阴影是否消除

---

## 方法 2：Android 打包

### ⏱️ 预计时间：60-70 分钟

### 前置要求

- ✅ Google 账号
- ✅ Google Drive（至少 500MB 空间）
- ✅ 稳定的网络连接

---

### 步骤 1：上传项目到 Google Drive

1. **打开 Google Drive**
   - 访问：https://drive.google.com/
   - 登录您的 Google 账号

2. **上传项目文件夹**
   - 将整个 `my_kivy_app` 文件夹拖拽到 Google Drive
   - 等待上传完成（约 1-2 分钟）

3. **记住路径**
   - 默认路径：`/content/drive/MyDrive/my_kivy_app`
   - 如果放在其他位置，记住完整路径

---

### 步骤 2：在 Google Colab 中打包

1. **打开 Google Colab**
   - 访问：https://colab.research.google.com/
   - 点击 "新建笔记本"

2. **复制打包脚本**
   - 打开 `my_kivy_app/colab_build_script.py`
   - 复制全部内容

3. **粘贴到 Colab**
   - 在 Colab 的代码单元格中粘贴
   - **重要：** 修改 `project_path` 为您的实际路径
   
   ```python
   # 修改这一行
   project_path = '/content/drive/MyDrive/my_kivy_app'
   ```

4. **运行脚本**
   - 点击 ▶️ 运行按钮
   - 或按 `Ctrl+Enter` (Windows) / `Cmd+Enter` (Mac)

---

### 步骤 3：等待打包完成

**打包进度：**

```
📁 步骤 1/8: 挂载 Google Drive... (1 分钟)
   → 授权访问 Google Drive

📦 步骤 2/8: 安装 Buildozer... (2 分钟)
   → 安装打包工具

🔧 步骤 3/8: 安装系统依赖... (3 分钟)
   → 安装编译工具

📂 步骤 4/8: 进入项目目录... (1 秒)
   → 切换到项目文件夹

✅ 步骤 5/8: 验证项目文件... (1 秒)
   → 检查必要文件

🔍 步骤 6/8: 检查配置... (1 秒)
   → 验证 buildozer.spec

🧹 步骤 7/8: 清理旧构建... (可选)
   → 清理缓存（首次打包选 n）

🔨 步骤 8/8: 打包 APK... (50-60 分钟) ⭐
   → 下载 SDK/NDK (10 分钟)
   → 编译 Python (8 分钟)
   → 编译 Kivy (8 分钟)
   → 编译 OpenCV (20 分钟) ⭐ 最耗时
   → 编译 NumPy (8 分钟)
   → 打包 APK (5 分钟)
```

**💡 提示：**
- 保持浏览器标签页打开
- 不要关闭 Colab 页面
- 可以最小化窗口，但不要关闭
- 可以做其他事情，但定期检查进度

---

### 步骤 4：下载 APK

**打包成功后：**

```
✅ 打包成功！找到 1 个 APK 文件：

  📦 binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk
     大小: 55.3 MB
     路径: bin/binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk

📥 下载 APK
正在下载: binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk...
✅ binarization-1.0-arm64-v8a_armeabi-v7a-debug.apk 已开始下载！
```

**浏览器会自动下载 APK 文件**

---

### 步骤 5：安装到 Android 手机

1. **传输 APK**
   - 通过 USB 线连接手机
   - 或通过云盘/邮件发送到手机

2. **允许未知来源**
   - 设置 → 安全 → 允许安装未知来源的应用
   - 或在安装时点击"允许"

3. **安装 APK**
   - 在手机上打开 APK 文件
   - 点击"安装"
   - 等待安装完成

4. **打开应用**
   - 在应用列表中找到 "Auto Binarization Demo"
   - 点击打开

---

### 步骤 6：测试应用

1. **授予权限**
   - 允许访问存储空间
   - 允许访问相机（如果需要）

2. **选择图片**
   - 点击 "Select Image"
   - 从相册选择一张文档照片

3. **查看效果**
   - 左侧：原图
   - 右侧：处理后的图片
   - 检查文字是否清晰

4. **保存结果**
   - 点击 "Save Result"
   - 图片保存到 `/Pictures/BinarizationDemo/`

---

## ⚠️ 常见问题

### 问题 1：pip install 失败

**错误：**
```
ERROR: Could not find a version that satisfies the requirement kivy==2.1.0
```

**解决：**
```bash
# 升级 pip
python -m pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

---

### 问题 2：OpenCV 导入失败

**错误：**
```
ImportError: No module named 'cv2'
```

**解决：**
```bash
pip install opencv-python
```

---

### 问题 3：Kivy 窗口无法打开

**错误：**
```
[CRITICAL] Unable to find any valuable Window provider
```

**解决（Windows）：**
```bash
pip install kivy_deps.angle kivy_deps.glew kivy_deps.sdl2
```

**解决（Mac）：**
```bash
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
```

---

### 问题 4：Android 打包失败

**错误：**
```
Command failed: ['/usr/bin/python3', '-m', 'pythonforandroid.toolchain', ...]
```

**检查：**
1. buildozer.spec 中是否使用 `opencv`（不是 `opencv-python`）
2. 查看完整错误日志
3. 参考 `ANDROID_BUILD_GUIDE.md`

---

### 问题 5：APK 安装失败

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

## 📞 获取帮助

### 文档

- **README.md** - 项目说明
- **ANDROID_BUILD_GUIDE.md** - Android 打包详细指南
- **OPENCV_VERSION_SUMMARY.md** - 技术总结
- **FINAL_SUMMARY.md** - 完整总结

### 测试脚本

- **test_opencv_version.py** - OpenCV 版本测试

---

## 🎯 快速命令参考

### 桌面环境

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python test_opencv_version.py

# 运行应用
python main.py
```

### 查看结果

```bash
# 测试输出
cd test_output_opencv
ls

# 应用输出
cd output/binarized
ls
```

---

**🎉 祝您使用愉快！**

有任何问题，请查看相关文档或运行测试脚本进行诊断。

