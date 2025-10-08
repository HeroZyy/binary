@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==================================
echo 🔧 GitHub Actions 工作流修复
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

REM 检查工作流文件
if not exist ".github\workflows\build.yml" (
    echo ❌ 错误：未找到 .github\workflows\build.yml
    pause
    exit /b 1
)

echo 📋 检查工作流文件...
echo.

REM 检查是否包含有问题的内容
findstr /C:"ArtemSBulgakov/buildozer-action" .github\workflows\build.yml >nul
if %errorlevel% equ 0 (
    echo ⚠️  检测到有问题的 buildozer-action
    set HAS_PROBLEM=1
    goto fix
)

findstr /C:"docker run" .github\workflows\build.yml >nul
if %errorlevel% equ 0 (
    echo ⚠️  检测到 Docker 命令
    set HAS_PROBLEM=1
    goto fix
)

findstr /C:"kivy/buildozer:latest" .github\workflows\build.yml >nul
if %errorlevel% equ 0 (
    echo ⚠️  检测到 Docker 镜像
    set HAS_PROBLEM=1
    goto fix
)

echo ✅ 工作流文件看起来正确
set HAS_PROBLEM=0
goto check_result

:fix
echo.
echo 🔄 需要修复工作流文件
echo.

REM 备份旧文件
echo 📦 备份旧工作流...
copy /y ".github\workflows\build.yml" ".github\workflows\build.yml.backup" >nul
echo ✅ 已备份到 build.yml.backup
echo.

REM 使用简化版本
if exist ".github\workflows\build-simple.yml" (
    echo 🔄 使用简化版本替换...
    copy /y ".github\workflows\build-simple.yml" ".github\workflows\build.yml" >nul
    echo ✅ 已替换为简化版本
) else (
    echo ❌ 错误：未找到 build-simple.yml
    echo    请确保 build-simple.yml 文件存在
    pause
    exit /b 1
)

echo.
echo ✅ 修复完成！
echo.
echo 下一步：
echo   git add .github/workflows/build.yml
echo   git commit -m "Fix: Use simplified build workflow"
echo   git push origin main
goto end

:check_result
echo.
if %HAS_PROBLEM% equ 0 (
    echo ✅ 工作流文件正确，无需修复
    echo.
    echo 如果 GitHub Actions 仍然失败，请：
    echo 1. 确认 GitHub 上的文件已更新
    echo 2. 删除旧的工作流运行记录
    echo 3. 手动触发新的构建
)

:end
echo.
echo ==================================
echo 📚 相关文档
echo ==================================
echo.
echo - GITHUB_ACTIONS_FIX_FINAL.md - 详细修复指南
echo - DOCKER_ERROR_FIXED.md - Docker 错误说明
echo - BUILD_ERROR_FIXED.md - 构建错误说明
echo.
pause

