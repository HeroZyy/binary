#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Kivy 应用（无需 OpenCV）
"""

import sys
import os

def test_imports():
    """测试依赖导入"""
    print("🔍 测试依赖导入...")
    
    dependencies = {
        'kivy': 'Kivy',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'plyer': 'Plyer'
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            all_ok = False
    
    return all_ok


def test_binarization():
    """测试二值化功能"""
    print("\n🔍 测试二值化功能...")
    
    try:
        from PIL import Image, ImageFilter, ImageOps
        import numpy as np
        
        # 创建测试图像
        print("  📝 创建测试图像...")
        test_img = Image.new('RGB', (100, 100), color='white')
        
        # 添加一些黑色文字
        from PIL import ImageDraw
        draw = ImageDraw.Draw(test_img)
        draw.text((10, 10), "Test", fill='black')
        
        # 转换为灰度
        print("  🔄 转换为灰度...")
        gray = test_img.convert('L')
        
        # 应用滤镜
        print("  🔄 应用滤镜...")
        gray = gray.filter(ImageFilter.MedianFilter(size=3))
        gray = ImageOps.autocontrast(gray, cutoff=2)
        gray = gray.filter(ImageFilter.SHARPEN)
        
        # Otsu 二值化
        print("  🔄 Otsu 二值化...")
        img_array = np.array(gray)
        hist, _ = np.histogram(img_array.ravel(), bins=256, range=(0, 256))
        hist = hist.astype(float)
        
        total = img_array.size
        current_max = 0
        threshold = 0
        sum_total = np.dot(np.arange(256), hist)
        sum_background = 0
        weight_background = 0
        
        for t in range(256):
            weight_background += hist[t]
            if weight_background == 0:
                continue
            
            weight_foreground = total - weight_background
            if weight_foreground == 0:
                break
            
            sum_background += t * hist[t]
            mean_background = sum_background / weight_background
            mean_foreground = (sum_total - sum_background) / weight_foreground
            
            variance_between = weight_background * weight_foreground * \
                               (mean_background - mean_foreground) ** 2
            
            if variance_between > current_max:
                current_max = variance_between
                threshold = t
        
        print(f"  ✅ 计算阈值: {threshold}")
        
        # 应用阈值
        binary_array = (img_array > threshold).astype(np.uint8) * 255
        result = Image.fromarray(binary_array, mode='L')
        result = result.convert('RGB')
        
        print(f"  ✅ 二值化成功: {result.size}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 二值化失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_app_import():
    """测试应用导入"""
    print("\n🔍 测试应用导入...")
    
    try:
        # 添加当前目录到路径
        sys.path.insert(0, os.path.dirname(__file__))
        
        # 导入主应用
        from main import SimpleBinarizationProcessor, BinarizationApp
        
        print("  ✅ SimpleBinarizationProcessor 导入成功")
        print("  ✅ BinarizationApp 导入成功")
        
        # 测试处理器初始化
        processor = SimpleBinarizationProcessor()
        print(f"  ✅ 处理器初始化成功: threshold={processor.threshold}, adaptive={processor.use_adaptive}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 应用导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("="*80)
    print("🧪 Kivy 应用测试（无 OpenCV）")
    print("="*80)
    
    tests = [
        ("依赖导入", test_imports),
        ("二值化功能", test_binarization),
        ("应用导入", test_app_import)
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            result = test_func()
            results[name] = result
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results[name] = False
    
    # 统计结果
    print("\n" + "="*80)
    print("📊 测试结果汇总")
    print("="*80)
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print("\n" + "="*80)
    print(f"总计: {total} 个测试")
    print(f"✅ 通过: {passed} 个")
    print(f"❌ 失败: {failed} 个")
    print("="*80)
    
    if failed > 0:
        print("\n💡 提示:")
        print("  1. 检查依赖: pip install kivy pillow numpy plyer")
        print("  2. 确保没有安装 opencv-python")
        sys.exit(1)
    else:
        print("\n🎉 所有测试通过！")
        print("\n📱 可以运行应用:")
        print("  python main.py")
        sys.exit(0)


if __name__ == "__main__":
    main()

