#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阴影消除功能
"""

import sys
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from main import SimpleBinarizationProcessor


def create_test_image_with_shadow():
    """创建带阴影的测试图像"""
    print("📝 创建带阴影的测试图像...")
    
    # 创建 800x600 的白色图像
    img = Image.new('L', (800, 600), color=255)
    draw = ImageDraw.Draw(img)
    
    # 添加渐变阴影（左侧暗，右侧亮）
    for x in range(800):
        # 从左到右，亮度从 100 渐变到 255
        brightness = int(100 + (155 * x / 800))
        for y in range(600):
            current = img.getpixel((x, y))
            # 混合原始亮度和渐变
            new_brightness = int(current * brightness / 255)
            img.putpixel((x, y), new_brightness)
    
    # 添加黑色文字（模拟文档）
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        # 如果没有字体，使用默认字体
        font = ImageFont.load_default()
    
    draw = ImageDraw.Draw(img)
    
    # 在不同位置添加文字
    texts = [
        (50, 50, "Shadow Test - Left (Dark)"),
        (50, 150, "This text is in shadow area"),
        (50, 250, "Should be readable after processing"),
        (400, 50, "Right Side (Bright)"),
        (400, 150, "This area is well-lit"),
        (400, 250, "Text should remain clear"),
    ]
    
    for x, y, text in texts:
        draw.text((x, y), text, fill=0, font=font)
    
    # 添加一些图形（模拟图片区域）
    draw.rectangle([50, 400, 200, 550], outline=0, width=3)
    draw.ellipse([250, 400, 400, 550], outline=0, width=3)
    draw.line([450, 400, 600, 550], fill=0, width=3)
    draw.line([450, 550, 600, 400], fill=0, width=3)
    
    # 转换为 RGB
    img_rgb = img.convert('RGB')
    
    print(f"✅ 测试图像创建完成: {img_rgb.size}")
    return img_rgb


def test_shadow_removal():
    """测试阴影消除"""
    print("\n" + "="*80)
    print("🧪 测试阴影消除功能")
    print("="*80 + "\n")
    
    # 创建测试图像
    test_img = create_test_image_with_shadow()
    
    # 保存原图
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    original_path = os.path.join(output_dir, "01_original_with_shadow.jpg")
    test_img.save(original_path, quality=95)
    print(f"💾 原图已保存: {original_path}\n")
    
    # 测试不同参数
    test_cases = [
        ("Small Window (11x11)", 11, 10),
        ("Medium Window (21x21)", 21, 12),
        ("Large Window (31x31)", 31, 15),
        ("Extra Large Window (51x51)", 51, 20),
    ]
    
    for name, block_size, offset in test_cases:
        print(f"\n{'='*80}")
        print(f"🔬 测试: {name}")
        print(f"   参数: block_size={block_size}, offset={offset}")
        print(f"{'='*80}\n")
        
        # 创建处理器
        processor = SimpleBinarizationProcessor(block_size=block_size, offset=offset)
        
        # 处理图像
        try:
            result = processor.apply_binarization(test_img, denoise=True)
            
            # 保存结果
            filename = f"02_{name.replace(' ', '_').replace('(', '').replace(')', '')}.jpg"
            result_path = os.path.join(output_dir, filename)
            result.save(result_path, quality=95)
            
            print(f"✅ 处理成功！")
            print(f"💾 结果已保存: {result_path}\n")
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("📊 测试完成！")
    print("="*80)
    print(f"\n📁 所有结果已保存到: {os.path.abspath(output_dir)}")
    print("\n💡 建议:")
    print("  1. 打开 test_output 文件夹查看结果")
    print("  2. 对比原图和处理后的图像")
    print("  3. 观察阴影区域是否变亮")
    print("  4. 检查文字是否清晰可读")


def test_performance():
    """测试性能"""
    print("\n" + "="*80)
    print("⚡ 性能测试")
    print("="*80 + "\n")
    
    import time
    
    # 创建不同尺寸的测试图像
    sizes = [
        (400, 300, "Small"),
        (800, 600, "Medium"),
        (1200, 900, "Large"),
    ]
    
    for w, h, name in sizes:
        print(f"📐 测试尺寸: {w}x{h} ({name})")
        
        # 创建测试图像
        img = Image.new('RGB', (w, h), color='white')
        
        # 创建处理器
        processor = SimpleBinarizationProcessor(block_size=31, offset=15)
        
        # 测试处理时间
        start_time = time.time()
        result = processor.apply_binarization(img, denoise=True)
        end_time = time.time()
        
        elapsed = (end_time - start_time) * 1000  # 转换为毫秒
        
        print(f"   ⏱️  处理时间: {elapsed:.1f} ms")
        print(f"   ✅ 完成\n")


def main():
    """主函数"""
    print("="*80)
    print("🧪 阴影消除功能测试")
    print("="*80)
    
    try:
        # 测试阴影消除
        test_shadow_removal()
        
        # 测试性能
        test_performance()
        
        print("\n" + "="*80)
        print("🎉 所有测试完成！")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

