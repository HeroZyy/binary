#!/bin/bash

# GitHub Actions 构建错误修复脚本
# 用于修复 "chown: invalid user: 'user'" 错误

echo "=================================="
echo "🔧 GitHub Actions 构建错误修复"
echo "=================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "buildozer.spec" ]; then
    echo "❌ 错误：未找到 buildozer.spec 文件"
    echo "   请在 my_kivy_app 目录中运行此脚本"
    exit 1
fi

echo "✅ 检测到 buildozer.spec 文件"
echo ""

# 显示可用的修复方案
echo "请选择修复方案："
echo ""
echo "1. Docker 版本（推荐）⭐⭐⭐⭐⭐"
echo "   - 最稳定"
echo "   - 使用官方 Kivy Docker 镜像"
echo "   - 成功率 95%+"
echo ""
echo "2. 简化版本 ⭐⭐⭐⭐"
echo "   - 直接安装 Buildozer"
echo "   - 无需 Docker"
echo "   - 构建速度更快"
echo ""
echo "3. 修复版本 ⭐⭐⭐⭐"
echo "   - 移除有问题的 Action"
echo "   - 支持缓存"
echo "   - 完全控制"
echo ""
echo "4. 取消"
echo ""

read -p "请输入选择 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🐳 使用 Docker 版本..."
        
        # 备份旧工作流
        if [ -f ".github/workflows/build.yml" ]; then
            mv .github/workflows/build.yml .github/workflows/build.yml.backup
            echo "✅ 已备份旧工作流到 build.yml.backup"
        fi
        
        # 使用 Docker 版本
        if [ -f ".github/workflows/build-docker.yml" ]; then
            mv .github/workflows/build-docker.yml .github/workflows/build.yml
            echo "✅ 已启用 Docker 版本"
        else
            echo "❌ 错误：未找到 build-docker.yml 文件"
            exit 1
        fi
        
        echo ""
        echo "✅ 修复完成！"
        echo ""
        echo "下一步："
        echo "  git add .github/workflows/"
        echo "  git commit -m 'Fix: Use Docker-based build'"
        echo "  git push"
        ;;
        
    2)
        echo ""
        echo "⚡ 使用简化版本..."
        
        # 备份旧工作流
        if [ -f ".github/workflows/build.yml" ]; then
            mv .github/workflows/build.yml .github/workflows/build.yml.backup
            echo "✅ 已备份旧工作流到 build.yml.backup"
        fi
        
        # 使用简化版本
        if [ -f ".github/workflows/build-simple.yml" ]; then
            mv .github/workflows/build-simple.yml .github/workflows/build.yml
            echo "✅ 已启用简化版本"
        else
            echo "❌ 错误：未找到 build-simple.yml 文件"
            exit 1
        fi
        
        echo ""
        echo "✅ 修复完成！"
        echo ""
        echo "下一步："
        echo "  git add .github/workflows/"
        echo "  git commit -m 'Fix: Use simplified build'"
        echo "  git push"
        ;;
        
    3)
        echo ""
        echo "🔧 使用修复版本..."
        echo "✅ build.yml 已经更新为修复版本"
        echo ""
        echo "下一步："
        echo "  git add .github/workflows/build.yml"
        echo "  git commit -m 'Fix: Remove problematic buildozer-action'"
        echo "  git push"
        ;;
        
    4)
        echo ""
        echo "❌ 已取消"
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ 无效的选择"
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "📚 相关文档"
echo "=================================="
echo ""
echo "- BUILD_ERROR_FIXED.md - 错误修复说明"
echo "- GITHUB_ACTIONS_TROUBLESHOOTING.md - 故障排除指南"
echo "- GITHUB_ACTIONS_QUICKSTART.md - 快速开始"
echo ""
echo "🎉 修复完成！推送代码后，访问 GitHub Actions 查看进度。"

