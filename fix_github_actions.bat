@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==================================
echo 🔧 GitHub Actions 构建错误修复
echo ==================================
echo.

REM 检查是否在正确的目录
if not exist "buildozer.spec" (
    echo ❌ 错误：未找到 buildozer.spec 文件
    echo    请在 my_kivy_app 目录中运行此脚本
    pause
    exit /b 1
)

echo ✅ 检测到 buildozer.spec 文件
echo.

REM 显示可用的修复方案
echo 请选择修复方案：
echo.
echo 1. Docker 版本（推荐）⭐⭐⭐⭐⭐
echo    - 最稳定
echo    - 使用官方 Kivy Docker 镜像
echo    - 成功率 95%%+
echo.
echo 2. 简化版本 ⭐⭐⭐⭐
echo    - 直接安装 Buildozer
echo    - 无需 Docker
echo    - 构建速度更快
echo.
echo 3. 修复版本 ⭐⭐⭐⭐
echo    - 移除有问题的 Action
echo    - 支持缓存
echo    - 完全控制
echo.
echo 4. 取消
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" goto docker
if "%choice%"=="2" goto simple
if "%choice%"=="3" goto fixed
if "%choice%"=="4" goto cancel
goto invalid

:docker
echo.
echo 🐳 使用 Docker 版本...

REM 备份旧工作流
if exist ".github\workflows\build.yml" (
    move /y ".github\workflows\build.yml" ".github\workflows\build.yml.backup" >nul
    echo ✅ 已备份旧工作流到 build.yml.backup
)

REM 使用 Docker 版本
if exist ".github\workflows\build-docker.yml" (
    move /y ".github\workflows\build-docker.yml" ".github\workflows\build.yml" >nul
    echo ✅ 已启用 Docker 版本
) else (
    echo ❌ 错误：未找到 build-docker.yml 文件
    pause
    exit /b 1
)

echo.
echo ✅ 修复完成！
echo.
echo 下一步：
echo   git add .github/workflows/
echo   git commit -m "Fix: Use Docker-based build"
echo   git push
goto end

:simple
echo.
echo ⚡ 使用简化版本...

REM 备份旧工作流
if exist ".github\workflows\build.yml" (
    move /y ".github\workflows\build.yml" ".github\workflows\build.yml.backup" >nul
    echo ✅ 已备份旧工作流到 build.yml.backup
)

REM 使用简化版本
if exist ".github\workflows\build-simple.yml" (
    move /y ".github\workflows\build-simple.yml" ".github\workflows\build.yml" >nul
    echo ✅ 已启用简化版本
) else (
    echo ❌ 错误：未找到 build-simple.yml 文件
    pause
    exit /b 1
)

echo.
echo ✅ 修复完成！
echo.
echo 下一步：
echo   git add .github/workflows/
echo   git commit -m "Fix: Use simplified build"
echo   git push
goto end

:fixed
echo.
echo 🔧 使用修复版本...
echo ✅ build.yml 已经更新为修复版本
echo.
echo 下一步：
echo   git add .github/workflows/build.yml
echo   git commit -m "Fix: Remove problematic buildozer-action"
echo   git push
goto end

:cancel
echo.
echo ❌ 已取消
pause
exit /b 0

:invalid
echo.
echo ❌ 无效的选择
pause
exit /b 1

:end
echo.
echo ==================================
echo 📚 相关文档
echo ==================================
echo.
echo - BUILD_ERROR_FIXED.md - 错误修复说明
echo - GITHUB_ACTIONS_TROUBLESHOOTING.md - 故障排除指南
echo - GITHUB_ACTIONS_QUICKSTART.md - 快速开始
echo.
echo 🎉 修复完成！推送代码后，访问 GitHub Actions 查看进度。
echo.
pause

