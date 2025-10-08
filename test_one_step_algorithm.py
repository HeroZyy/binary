#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 one_step_document_processor.py 算法
"""

import sys
import os
import numpy as np

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from main import SimpleBinarizationProcessor, USE_OPENCV

def create_test_image_with_shadow():
    """创建带阴影的测试图像"""
    print("📝 创建带阴影的测试图像...")
    
    if USE_OPENCV:
        import cv2
        from PIL import ImageDraw, ImageFont, Image
        
        # 创建 PIL 图像（方便绘制文字）
        img_pil = Image.new('L', (800, 600), color=255)
        draw = ImageDraw.Draw(img_pil)
        
        # 添加渐变阴影
        for x in range(800):
            brightness = int(100 + (155 * x / 800))
            for y in range(600):
                current = img_pil.getpixel((x, y))
                new_brightness = int(current * brightness / 255)
                img_pil.putpixel((x, y), new_brightness)
        
        # 添加文字
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        texts = [
            (50, 50, "one_step_document_processor Algorithm"),
            (50, 150, "Left side has shadow (dark)"),
            (50, 250, "Text should be clear after processing"),
            (400, 50, "Right Side (Bright)"),
            (400, 150, "This area is well-lit"),
            (400, 250, "Text should remain sharp"),
        ]
        
        for x, y, text in texts:
            draw.text((x, y), text, fill=0, font=font)
        
        # 添加图形
        draw.rectangle([50, 400, 200, 550], outline=0, width=3)
        draw.ellipse([250, 400, 400, 550], outline=0, width=3)
        
        # 转换为 OpenCV 格式
        img_cv = np.array(img_pil)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2BGR)
        
        print(f"✅ 测试图像创建完成: {img_cv.shape}")
        return img_cv
    else:
        from PIL import Image, ImageDraw, ImageFont
        
        # 使用 Pillow
        img = Image.new('L', (800, 600), color=255)
        draw = ImageDraw.Draw(img)
        
        # 添加渐变阴影
        for x in range(800):
            brightness = int(100 + (155 * x / 800))
            for y in range(600):
                current = img.getpixel((x, y))
                new_brightness = int(current * brightness / 255)
                img.putpixel((x, y), new_brightness)
        
        # 添加文字
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        texts = [
            (50, 50, "one_step Algorithm (Pillow)"),
            (50, 150, "Left side has shadow (dark)"),
            (50, 250, "Text should be readable"),
        ]
        
        for x, y, text in texts:
            draw.text((x, y), text, fill=0, font=font)
        
        img_rgb = img.convert('RGB')
        print(f"✅ 测试图像创建完成: {img_rgb.size}")
        return img_rgb


def test_one_step_algorithm():
    """测试 one_step_document_processor.py 算法"""
    print("\n" + "="*80)
    print(f"🧪 测试 one_step_document_processor.py 算法")
    print("="*80 + "\n")
    
    # 创建测试图像
    test_img = create_test_image_with_shadow()
    
    # 保存原图
    output_dir = "test_output_one_step"
    os.makedirs(output_dir, exist_ok=True)
    
    if USE_OPENCV:
        import cv2
        original_path = os.path.join(output_dir, "01_original_with_shadow.jpg")
        cv2.imwrite(original_path, test_img)
    else:
        original_path = os.path.join(output_dir, "01_original_with_shadow.jpg")
        test_img.save(original_path, quality=95)
    
    print(f"💾 原图已保存: {original_path}\n")
    
    # 测试 one_step_document_processor.py 的参数
    print(f"\n{'='*80}")
    print(f"🔬 测试: one_step_document_processor.py 算法")
    print(f"   参数: block_size=11, C=2, denoise_h=5")
    print(f"   算法: ADAPTIVE_THRESH_GAUSSIAN_C")
    print(f"{'='*80}\n")
    
    # 创建处理器（使用 one_step 的参数）
    processor = SimpleBinarizationProcessor(
        block_size=11,
        c_value=2,
        denoise_h=5
    )
    
    # 处理图像
    try:
        result = processor.apply_binarization(test_img, denoise=True)
        
        # 保存结果
        result_path = os.path.join(output_dir, "02_one_step_algorithm.jpg")
        
        if USE_OPENCV:
            import cv2
            cv2.imwrite(result_path, result, [cv2.IMWRITE_JPEG_QUALITY, 95])
        else:
            result.save(result_path, quality=95)
        
        print(f"✅ 处理成功！")
        print(f"💾 结果已保存: {result_path}\n")
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 对比测试：不同参数
    print(f"\n{'='*80}")
    print(f"🔬 对比测试: 不同参数")
    print(f"{'='*80}\n")
    
    test_cases = [
        ("Small Block (7x7)", 7, 2, 5),
        ("Medium Block (15x15)", 15, 2, 5),
        ("Large Block (21x21)", 21, 2, 5),
        ("High C Value", 11, 5, 5),
        ("Low C Value", 11, 0, 5),
        ("Strong Denoise", 11, 2, 10),
        ("No Denoise", 11, 2, 0),
    ]
    
    for name, block_size, c_value, denoise_h in test_cases:
        print(f"  🔄 {name}: block={block_size}, C={c_value}, denoise={denoise_h}")
        
        processor = SimpleBinarizationProcessor(
            block_size=block_size,
            c_value=c_value,
            denoise_h=denoise_h
        )
        
        try:
            result = processor.apply_binarization(test_img, denoise=(denoise_h > 0))
            
            filename = f"03_{name.replace(' ', '_').replace('(', '').replace(')', '')}.jpg"
            result_path = os.path.join(output_dir, filename)
            
            if USE_OPENCV:
                import cv2
                cv2.imwrite(result_path, result, [cv2.IMWRITE_JPEG_QUALITY, 95])
            else:
                result.save(result_path, quality=95)
            
            print(f"     ✅ 已保存: {filename}")
            
        except Exception as e:
            print(f"     ❌ 失败: {e}")
    
    print("\n" + "="*80)
    print("📊 测试完成！")
    print("="*80)
    print(f"\n📁 所有结果已保存到: {os.path.abspath(output_dir)}")
    print("\n💡 对比说明：")
    print("  - 02_one_step_algorithm.jpg: one_step_document_processor.py 的参数")
    print("  - 03_*.jpg: 不同参数的对比测试")


def test_performance():
    """测试性能"""
    print("\n" + "="*80)
    print("⚡ 性能测试")
    print("="*80 + "\n")
    
    import time
    
    sizes = [
        (400, 300, "Small"),
        (800, 600, "Medium"),
        (1200, 900, "Large"),
    ]
    
    for w, h, name in sizes:
        print(f"📐 测试尺寸: {w}x{h} ({name})")
        
        # 创建测试图像
        if USE_OPENCV:
            import cv2
            img = np.ones((h, w, 3), dtype=np.uint8) * 255
        else:
            from PIL import Image
            img = Image.new('RGB', (w, h), color='white')
        
        # 创建处理器（one_step 参数）
        processor = SimpleBinarizationProcessor(
            block_size=11,
            c_value=2,
            denoise_h=5
        )
        
        # 测试处理时间
        start_time = time.time()
        result = processor.apply_binarization(img, denoise=True)
        end_time = time.time()
        
        elapsed = (end_time - start_time) * 1000
        
        print(f"   ⏱️  处理时间: {elapsed:.1f} ms")
        print(f"   ✅ 完成\n")


def main():
    """主函数"""
    print("="*80)
    print(f"🧪 one_step_document_processor.py 算法测试")
    print("="*80)
    
    if USE_OPENCV:
        import cv2
        print(f"\n✅ OpenCV 版本: {cv2.__version__}")
        print(f"✅ 算法: ADAPTIVE_THRESH_GAUSSIAN_C")
        print(f"✅ 参数: block_size=11, C=2, denoise_h=5")
    else:
        print(f"\n⚠️  使用 Pillow 备用方案")
    
    try:
        # 测试算法
        test_one_step_algorithm()
        
        # 测试性能
        test_performance()
        
        print("\n" + "="*80)
        print("🎉 所有测试完成！")
        print("="*80)
        
        print("\n💡 查看结果：")
        print("  1. 打开 test_output_one_step 文件夹")
        print("  2. 对比原图和处理后的图像")
        print("  3. 查看不同参数的效果")
        
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

