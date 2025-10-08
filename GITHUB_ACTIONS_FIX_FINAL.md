# 🔧 GitHub Actions 构建错误最终修复方案

## 🐛 错误信息

```
chown: invalid user: 'user'
subprocess.CalledProcessError: Command '['sudo', 'chown', '-R', 'user', '/github/workspace']' returned non-zero exit status 1.
```

**原因：** GitHub 上的工作流文件仍在使用有问题的 `ArtemSBulgakov/buildozer-action`。

---

## ✅ 解决方案

### 步骤 1：确认本地文件正确

检查 `.github/workflows/build.yml` 文件，确保它**不包含** Docker 或 `ArtemSBulgakov/buildozer-action`。

**正确的文件应该是这样的：**

```yaml
name: Build Android APK

on:
  push:
    branches: [ main, master, develop ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-20.04
    
    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v3
    
    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: 📦 Install system dependencies
      run: |
        sudo apt-get update -qq
        sudo apt-get install -y \
          git zip unzip openjdk-11-jdk wget \
          autoconf libtool pkg-config \
          zlib1g-dev libncurses5-dev \
          libffi-dev libssl-dev cmake \
          libltdl-dev ccache
    
    - name: 📦 Install Buildozer
      run: |
        pip install --upgrade pip setuptools wheel
        pip install buildozer==1.5.0 cython==0.29.36
    
    - name: 📦 Cache Buildozer global directory
      uses: actions/cache@v3
      with:
        path: ~/.buildozer
        key: buildozer-global-${{ hashFiles('buildozer.spec') }}
        restore-keys: |
          buildozer-global-
    
    - name: 📦 Cache Buildozer directory
      uses: actions/cache@v3
      with:
        path: .buildozer
        key: buildozer-${{ hashFiles('buildozer.spec') }}
        restore-keys: |
          buildozer-
    
    - name: 🏗️ Build APK
      run: |
        yes | buildozer android debug || buildozer android debug
      env:
        ANDROID_SDK_ROOT: /opt/android-sdk
        ANDROID_HOME: /opt/android-sdk
    
    - name: 📊 Find APK file
      id: find_apk
      run: |
        APK_FILE=$(find bin -name "*.apk" -type f | head -n 1)
        if [ -z "$APK_FILE" ]; then
          echo "❌ 错误：未找到 APK 文件"
          echo "bin 目录内容："
          ls -la bin/ || echo "bin 目录不存在"
          exit 1
        fi
        echo "apk_path=$APK_FILE" >> $GITHUB_OUTPUT
        echo "apk_name=$(basename $APK_FILE)" >> $GITHUB_OUTPUT
        echo "✅ 找到 APK: $APK_FILE"
        echo "📏 文件大小: $(du -h $APK_FILE | cut -f1)"
    
    - name: 📤 Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: android-apk
        path: ${{ steps.find_apk.outputs.apk_path }}
        retention-days: 30
```

---

### 步骤 2：强制推送更新

```bash
cd my_kivy_app

# 1. 确认当前工作流文件
cat .github/workflows/build.yml | head -20

# 2. 如果文件正确，强制提交并推送
git add .github/workflows/build.yml
git commit -m "Fix: Use direct Buildozer installation (no Docker)"
git push origin main --force

# 3. 如果 push 失败，尝试先 pull
git pull origin main --rebase
git push origin main
```

---

### 步骤 3：删除旧的工作流运行

1. 访问：`https://github.com/YOUR_USERNAME/my_kivy_app/actions`
2. 点击左侧的工作流名称
3. 点击右上角的 "..." 菜单
4. 选择 "Delete workflow runs"
5. 删除所有旧的运行记录

---

### 步骤 4：手动触发新构建

1. 访问：`https://github.com/YOUR_USERNAME/my_kivy_app/actions`
2. 点击左侧的 "Build Android APK"
3. 点击右侧的 "Run workflow"
4. 选择 `main` 分支
5. 点击 "Run workflow"

---

## 🔍 验证修复

### 检查工作流文件

在 GitHub 上查看文件：

```
https://github.com/YOUR_USERNAME/my_kivy_app/blob/main/.github/workflows/build.yml
```

**确保文件中：**
- ✅ **有** `runs-on: ubuntu-20.04`
- ✅ **有** `pip install buildozer==1.5.0`
- ✅ **有** `buildozer android debug`
- ❌ **没有** `docker run`
- ❌ **没有** `ArtemSBulgakov/buildozer-action`
- ❌ **没有** `kivy/buildozer:latest`

---

## 🚨 如果仍然失败

### 方案 A：完全重建工作流

```bash
cd my_kivy_app

# 1. 删除旧工作流
rm -rf .github/workflows/build.yml

# 2. 使用简化版本
cp build-simple.yml .github/workflows/build.yml

# 3. 提交
git add .github/workflows/
git commit -m "Fix: Replace with simplified build workflow"
git push origin main --force
```

---

### 方案 B：使用 Google Colab

如果 GitHub Actions 持续有问题，使用 Google Colab 作为备选方案：

```bash
# 参考文档
cat COLAB_BUILD_COMPLETE_GUIDE.md
```

**步骤：**
1. 上传 `my_kivy_app` 到 Google Drive
2. 在 Colab 中运行 `colab_build_android.py`
3. 等待 60 分钟
4. 下载 APK

---

## 📋 完整的修复脚本

创建一个脚本来自动修复：

```bash
#!/bin/bash
# fix_github_workflow.sh

cd my_kivy_app

echo "🔧 修复 GitHub Actions 工作流"
echo ""

# 检查文件是否存在
if [ ! -f ".github/workflows/build.yml" ]; then
    echo "❌ 错误：未找到 build.yml"
    exit 1
fi

# 检查文件内容
if grep -q "ArtemSBulgakov/buildozer-action" .github/workflows/build.yml; then
    echo "⚠️  检测到有问题的 buildozer-action"
    echo "🔄 替换为正确的工作流..."
    
    # 使用简化版本
    if [ -f ".github/workflows/build-simple.yml" ]; then
        cp .github/workflows/build-simple.yml .github/workflows/build.yml
        echo "✅ 已替换为简化版本"
    else
        echo "❌ 错误：未找到 build-simple.yml"
        exit 1
    fi
else
    echo "✅ 工作流文件看起来正确"
fi

# 提交更改
echo ""
echo "📤 提交更改..."
git add .github/workflows/build.yml
git commit -m "Fix: Use direct Buildozer installation (no Docker)"

echo ""
echo "🚀 推送到 GitHub..."
git push origin main

echo ""
echo "✅ 完成！"
echo ""
echo "下一步："
echo "1. 访问：https://github.com/YOUR_USERNAME/my_kivy_app/actions"
echo "2. 手动触发新的构建"
echo "3. 等待 20-25 分钟"
```

**使用方法：**

```bash
chmod +x fix_github_workflow.sh
./fix_github_workflow.sh
```

---

## 🎯 推荐流程

### 最简单的方法

```bash
cd my_kivy_app

# 1. 确保使用正确的工作流
cat .github/workflows/build.yml | grep -E "buildozer-action|docker run"

# 如果有输出，说明文件有问题，需要替换
rm .github/workflows/build.yml
cp .github/workflows/build-simple.yml .github/workflows/build.yml

# 2. 提交并推送
git add .github/workflows/build.yml
git commit -m "Fix: Use simplified build workflow"
git push origin main --force

# 3. 访问 GitHub Actions 手动触发
# https://github.com/YOUR_USERNAME/my_kivy_app/actions
```

---

## 📊 工作流对比

### ❌ 错误的工作流（会失败）

```yaml
- name: 🐳 Build APK with Docker
  uses: ArtemSBulgakov/buildozer-action@v1  # ❌ 这个会失败
  with:
    command: buildozer android debug
```

### ✅ 正确的工作流（会成功）

```yaml
- name: 📦 Install Buildozer
  run: |
    pip install buildozer==1.5.0 cython==0.29.36

- name: 🏗️ Build APK
  run: |
    yes | buildozer android debug || buildozer android debug
```

---

## 🎊 总结

### 问题

GitHub 上的工作流文件仍在使用有问题的 Docker Action。

### 解决方案

1. ✅ 确认本地文件正确
2. ✅ 强制推送更新
3. ✅ 删除旧的工作流运行
4. ✅ 手动触发新构建

### 立即修复

```bash
cd my_kivy_app

# 使用简化版本
rm .github/workflows/build.yml
cp .github/workflows/build-simple.yml .github/workflows/build.yml

# 提交并推送
git add .github/workflows/build.yml
git commit -m "Fix: Use simplified build workflow"
git push origin main --force
```

### 预期结果

- ⏱️ 首次构建：20-25 分钟
- ⏱️ 缓存后：8-10 分钟
- ✅ APK 文件准备好
- 📥 从 Artifacts 下载

---

**🎉 按照这个流程，您的 GitHub Actions 应该可以正常工作！**

**如果仍然有问题，请使用 Google Colab 作为备选方案。**

