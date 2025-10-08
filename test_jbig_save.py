#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JBIG 格式保存测试脚本

测试将二值化图像保存为 JBIG 格式（实际使用 TIFF G4 压缩）
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from main import SimpleBinarizationProcessor

def create_test_image():
    """创建测试图像"""
    # 创建一个简单的文本图像
    img = np.ones((600, 800), dtype=np.uint8) * 255
    
    # 添加一些文本（模拟扫描文档）
    cv2.putText(img, 'Test Document', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)
    cv2.putText(img, 'JBIG Compression Test', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 2)
    cv2.putText(img, 'This is a binary image', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    
    # 添加一些噪点
    noise = np.random.randint(0, 50, (600, 800), dtype=np.uint8)
    img = cv2.add(img, noise)
    
    return img

def test_jbig_save():
    """测试 JBIG 保存功能"""
    print("=" * 60)
    print("JBIG 格式保存测试")
    print("=" * 60)
    print()
    
    # 创建输出目录
    output_dir = os.path.join(os.path.dirname(__file__), 'test_output_jbig')
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 输出目录: {output_dir}")
    print()
    
    # 创建测试图像
    print("📝 创建测试图像...")
    test_img = create_test_image()
    
    # 保存原始图像
    original_path = os.path.join(output_dir, 'original.png')
    cv2.imwrite(original_path, test_img)
    print(f"✅ 原始图像: {original_path}")
    print()
    
    # 二值化处理
    print("🔄 二值化处理...")
    processor = SimpleBinarizationProcessor()
    binary_img = processor.apply_binarization(test_img)

    # 转换为灰度图（用于保存）
    if len(binary_img.shape) == 3:
        binary_img = cv2.cvtColor(binary_img, cv2.COLOR_BGR2GRAY)

    print("✅ 二值化完成")
    print()
    
    # 测试不同格式的保存
    formats = [
        ('JBIG', 'test.jbig', SimpleBinarizationProcessor.save_as_jbig),
        ('TIFF-G4', 'test.tiff', SimpleBinarizationProcessor.save_as_tiff_g4),
        ('PNG', 'test.png', None),
        ('JPEG', 'test.jpg', None),
    ]
    
    results = []
    
    for fmt_name, filename, save_func in formats:
        filepath = os.path.join(output_dir, filename)
        
        try:
            if save_func:
                # 使用自定义保存函数
                success = save_func(binary_img, filepath)
                if not success:
                    print(f"❌ {fmt_name} 保存失败")
                    continue
            else:
                # 使用 OpenCV 保存
                if fmt_name == 'PNG':
                    cv2.imwrite(filepath, binary_img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
                elif fmt_name == 'JPEG':
                    cv2.imwrite(filepath, binary_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            # 获取文件大小
            size_bytes = os.path.getsize(filepath)
            size_kb = size_bytes / 1024
            
            results.append({
                'format': fmt_name,
                'filename': filename,
                'size_bytes': size_bytes,
                'size_kb': size_kb,
                'path': filepath
            })
            
            print(f"✅ {fmt_name:10s} - {size_kb:8.2f} KB - {filename}")
            
        except Exception as e:
            print(f"❌ {fmt_name} 保存失败: {e}")
    
    print()
    print("=" * 60)
    print("压缩率对比")
    print("=" * 60)
    print()
    
    if results:
        # 找到最小的文件作为基准
        min_size = min(r['size_bytes'] for r in results)
        
        print(f"{'格式':<12} {'大小 (KB)':<12} {'压缩率':<12} {'相对大小'}")
        print("-" * 60)
        
        for r in sorted(results, key=lambda x: x['size_bytes']):
            ratio = r['size_bytes'] / min_size
            compression = (1 - r['size_bytes'] / results[0]['size_bytes']) * 100 if results[0]['size_bytes'] > 0 else 0
            
            print(f"{r['format']:<12} {r['size_kb']:>8.2f} KB  {compression:>6.1f}%      {ratio:>5.2f}x")
    
    print()
    print("=" * 60)
    print("文件验证")
    print("=" * 60)
    print()
    
    # 验证文件可以正确读取
    for r in results:
        try:
            if r['format'] in ['JBIG', 'TIFF-G4']:
                # 使用 Pillow 读取
                img = Image.open(r['path'])
                print(f"✅ {r['format']:10s} - 可读取 - 模式: {img.mode}, 大小: {img.size}")
            else:
                # 使用 OpenCV 读取
                img = cv2.imread(r['path'], cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    print(f"✅ {r['format']:10s} - 可读取 - 形状: {img.shape}")
                else:
                    print(f"❌ {r['format']:10s} - 读取失败")
        except Exception as e:
            print(f"❌ {r['format']:10s} - 读取失败: {e}")
    
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
    print()
    print(f"📁 所有文件已保存到: {output_dir}")
    print()
    
    # 显示推荐格式
    if results:
        best = min(results, key=lambda x: x['size_bytes'])
        print(f"🏆 推荐格式: {best['format']} ({best['size_kb']:.2f} KB)")
        print()
        print("📊 格式说明:")
        print("  - JBIG/TIFF-G4: 最高压缩率，适合文档扫描")
        print("  - PNG: 无损压缩，通用性好")
        print("  - JPEG: 有损压缩，不适合二值图像")

def main():
    """主函数"""
    try:
        test_jbig_save()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

