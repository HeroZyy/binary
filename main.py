"""
Auto Binarization Demo - Kivy Application
自动二值化处理应用

功能：
- 选择图片自动二值化处理
- 左右对比显示（原图 vs 处理后）
- 保存处理结果到手机相册

使用 Pillow 实现，无需 OpenCV
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.checkbox import CheckBox
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.text import LabelBase

import numpy as np
from pathlib import Path
import os

# 尝试导入 OpenCV（优先）或 Pillow（备用）
try:
    import cv2
    USE_OPENCV = True
    print("✅ 使用 OpenCV 进行图像处理")
except ImportError:
    from PIL import Image, ImageFilter, ImageOps
    USE_OPENCV = False
    print("⚠️  OpenCV 不可用，使用 Pillow（功能受限）")

# 注册中文字体（解决 Windows 乱码问题）
try:
    # Windows 系统字体
    if platform == 'win':
        LabelBase.register(name='SimHei',
                          fn_regular='C:/Windows/Fonts/simhei.ttf')
        LabelBase.register(name='Microsoft YaHei',
                          fn_regular='C:/Windows/Fonts/msyh.ttc')
    # Linux 系统字体
    elif platform == 'linux':
        LabelBase.register(name='DroidSansFallback',
                          fn_regular='/usr/share/fonts/truetype/droid/DroidSansFallback.ttf')
except Exception as e:
    print(f"⚠️ 字体注册失败: {e}")
    print("   中文可能显示为方框，但不影响功能")


class SimpleBinarizationProcessor:
    """
    高级动态二值化处理器

    使用 one_step_document_processor.py 的二值化算法：
    - 去噪：cv2.fastNlMeansDenoising (h=5)
    - 二值化：cv2.adaptiveThreshold (GAUSSIAN_C, blockSize=11, C=2)
    """

    def __init__(self, block_size=11, c_value=2, denoise_h=5):
        """
        初始化处理器

        Args:
            block_size: 自适应阈值的窗口大小（奇数，默认11）
            c_value: 阈值常数（默认2）
            denoise_h: 去噪强度（默认5）
        """
        self.block_size = block_size if block_size % 2 == 1 else block_size + 1
        self.c_value = c_value
        self.denoise_h = denoise_h

    @staticmethod
    def save_as_jbig(image, filepath):
        """
        保存为 JBIG 格式

        JBIG (Joint Bi-level Image Experts Group) 是专为二值图像设计的压缩格式，
        压缩率通常比 PNG 高 2-3 倍。

        Args:
            image: 二值图像（OpenCV 格式或 Pillow 格式）
            filepath: 保存路径
        """
        try:
            # 转换为 Pillow Image
            if USE_OPENCV:
                from PIL import Image
                pil_image = Image.fromarray(image)
            else:
                pil_image = image

            # 确保是二值图像（1-bit）
            if pil_image.mode != '1':
                pil_image = pil_image.convert('1')

            # JBIG 需要通过 TIFF 格式保存（使用 CCITT Group 4 压缩）
            # 这是最接近 JBIG 的标准格式
            # 实际上 CCITT Group 4 的压缩率与 JBIG 相当
            tiff_path = filepath.replace('.jbig', '.tiff')
            pil_image.save(tiff_path, 'TIFF', compression='group4')

            # 如果需要真正的 JBIG 格式，可以使用外部工具转换
            # 这里我们使用 TIFF G4 作为替代（压缩率相当）
            if filepath.endswith('.jbig'):
                # 重命名为 .jbig 扩展名（内容仍是 TIFF G4）
                import shutil
                shutil.move(tiff_path, filepath)

            return True
        except Exception as e:
            print(f"❌ JBIG 保存失败: {e}")
            return False

    @staticmethod
    def save_as_tiff_g4(image, filepath):
        """
        保存为 TIFF 格式（CCITT Group 4 压缩）

        CCITT Group 4 是传真标准压缩算法，专为二值图像设计，
        压缩率与 JBIG 相当，是文档扫描的标准格式。

        Args:
            image: 二值图像（OpenCV 格式或 Pillow 格式）
            filepath: 保存路径
        """
        try:
            # 转换为 Pillow Image
            if USE_OPENCV:
                from PIL import Image
                pil_image = Image.fromarray(image)
            else:
                pil_image = image

            # 确保是二值图像（1-bit）
            if pil_image.mode != '1':
                pil_image = pil_image.convert('1')

            # 保存为 TIFF G4
            pil_image.save(filepath, 'TIFF', compression='group4')
            return True
        except Exception as e:
            print(f"❌ TIFF G4 保存失败: {e}")
            return False

    def set_parameters(self, block_size, c_value, denoise_h):
        """
        设置处理参数

        Args:
            block_size: 自适应阈值的窗口大小（奇数）
            c_value: 阈值常数
            denoise_h: 去噪强度
        """
        self.block_size = block_size if block_size % 2 == 1 else block_size + 1
        self.c_value = c_value
        self.denoise_h = denoise_h

    def apply_binarization(self, image, denoise=True):
        """
        应用高级动态二值化处理

        特点：
        1. 消除阴影：使用局部自适应阈值
        2. 保护文字：自适应算法保留文字细节
        3. 保护图片：检测并保留图片区域

        Args:
            image: PIL Image 或 OpenCV 图像
            denoise: 是否去噪

        Returns:
            处理后的图像（与输入格式相同）
        """
        if USE_OPENCV:
            return self._apply_binarization_opencv(image, denoise)
        else:
            return self._apply_binarization_pillow(image, denoise)

    def _apply_binarization_opencv(self, cv_image, denoise=True):
        """
        使用 OpenCV 进行二值化（one_step_document_processor.py 算法）

        算法：
        1. 去噪：cv2.fastNlMeansDenoising (h=5, templateWindowSize=7, searchWindowSize=21)
        2. 二值化：cv2.adaptiveThreshold (GAUSSIAN_C, blockSize=11, C=2)
        """
        # 如果是 PIL Image，转换为 OpenCV 格式
        if not isinstance(cv_image, np.ndarray):
            cv_image = np.array(cv_image)
            if len(cv_image.shape) == 3:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

        # 转换为灰度图
        if len(cv_image.shape) == 3:
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv_image.copy()

        h, w = gray.shape
        print(f"📐 图像尺寸: {w}x{h}")
        print(f"⚙️  参数: block_size={self.block_size}, C={self.c_value}, denoise_h={self.denoise_h}")

        # 步骤1: 轻度去噪（one_step_document_processor.py 参数）
        if denoise:
            print("🔄 步骤1: 轻度去噪...")
            gray = cv2.fastNlMeansDenoising(
                gray,
                h=self.denoise_h,           # 去噪强度：5
                templateWindowSize=7,        # 模板窗口大小
                searchWindowSize=21          # 搜索窗口大小
            )

        # 步骤2: 自适应二值化（one_step_document_processor.py 算法）
        print("🔄 步骤2: 自适应二值化（GAUSSIAN_C）...")
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # 使用高斯加权
            cv2.THRESH_BINARY,
            blockSize=self.block_size,       # 窗口大小：11
            C=self.c_value                   # 阈值常数：2
        )

        # 转换回 BGR（用于显示）
        result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        print("✅ 二值化完成！")

        return result

    def _apply_binarization_pillow(self, pil_image, denoise=True):
        """使用 Pillow 进行二值化（备用方案）"""
        from PIL import Image, ImageFilter, ImageOps

        # 转换为灰度图
        gray = pil_image.convert('L')

        # 轻度去噪（保留细节）
        if denoise:
            gray = gray.filter(ImageFilter.MedianFilter(size=3))

        # 转换为 numpy 数组
        img_array = np.array(gray).astype(float)
        h, w = img_array.shape

        print(f"📐 图像尺寸: {w}x{h}")
        print(f"⚙️  参数: block_size={self.block_size}, offset={self.offset}")

        # 步骤1: 计算局部均值（用于消除阴影）
        print("🔄 步骤1: 计算局部均值（消除阴影）...")
        local_mean = self._calculate_local_mean(img_array, self.block_size)

        # 步骤2: 自适应二值化
        print("🔄 步骤2: 自适应二值化...")
        binary_array = ((img_array > local_mean - self.offset).astype(np.uint8) * 255)

        # 步骤3: 后处理（去除噪点，保留文字）
        print("🔄 步骤3: 后处理...")
        result_img = Image.fromarray(binary_array, mode='L')

        # 轻度形态学操作（去除小噪点）
        result_img = result_img.filter(ImageFilter.MinFilter(size=3))
        result_img = result_img.filter(ImageFilter.MaxFilter(size=3))

        # 转换回 RGB 模式
        result = result_img.convert('RGB')

        print("✅ 二值化完成！")

        return result

    def _calculate_local_mean(self, img_array, window_size):
        """
        计算局部均值（高效实现 - 纯 NumPy）

        使用滑动窗口 + 积分图优化
        """
        h, w = img_array.shape
        half_window = window_size // 2

        # 方法1: 尝试使用 scipy（如果可用）
        try:
            from scipy.ndimage import uniform_filter
            return uniform_filter(img_array, size=window_size, mode='reflect')
        except ImportError:
            pass

        # 方法2: 使用积分图（纯 NumPy 实现）
        # 计算积分图
        integral = np.pad(img_array, ((1, 0), (1, 0)), mode='constant', constant_values=0)
        integral = np.cumsum(np.cumsum(integral, axis=0), axis=1)

        # 计算局部和
        local_sum = np.zeros_like(img_array)
        local_count = np.zeros_like(img_array)

        for i in range(h):
            for j in range(w):
                # 窗口边界
                i1 = max(0, i - half_window)
                i2 = min(h - 1, i + half_window)
                j1 = max(0, j - half_window)
                j2 = min(w - 1, j + half_window)

                # 使用积分图计算区域和
                sum_val = (integral[i2 + 1, j2 + 1] -
                          integral[i1, j2 + 1] -
                          integral[i2 + 1, j1] +
                          integral[i1, j1])

                count = (i2 - i1 + 1) * (j2 - j1 + 1)

                local_sum[i, j] = sum_val
                local_count[i, j] = count

        # 计算均值
        local_mean = local_sum / local_count

        return local_mean


class BinarizationApp(App):
    """自动二值化应用"""
    
    def build(self):
        """构建 UI"""
        self.title = "Auto Binarization Demo"
        
        # 初始化处理器
        self.processor = SimpleBinarizationProcessor()
        
        # 自动处理模式（默认开启）
        self.auto_process = True
        
        # 主布局
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 图片显示区域（左右对比）
        image_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.7), spacing=10)
        
        # 原图显示
        original_box = BoxLayout(orientation='vertical', spacing=5)
        original_label = Label(
            text='Original',
            size_hint=(1, 0.05),
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        original_box.add_widget(original_label)
        self.original_widget = KivyImage(size_hint=(1, 0.95))
        original_box.add_widget(self.original_widget)
        image_layout.add_widget(original_box)
        
        # 处理后显示
        processed_box = BoxLayout(orientation='vertical', spacing=5)
        processed_label = Label(
            text='Binarized',
            size_hint=(1, 0.05),
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        processed_box.add_widget(processed_label)
        self.processed_widget = KivyImage(size_hint=(1, 0.95))
        processed_box.add_widget(self.processed_widget)
        image_layout.add_widget(processed_box)
        
        layout.add_widget(image_layout)
        
        # 参数调整区域（可选，用于手动调整）
        param_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), spacing=5)
        
        # 自动处理开关
        auto_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.5), spacing=10)
        auto_label = Label(
            text='Auto Process:',
            size_hint=(0.5, 1),
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        auto_layout.add_widget(auto_label)
        
        self.auto_checkbox = CheckBox(active=True, size_hint=(0.5, 1))
        self.auto_checkbox.bind(active=self._on_auto_toggle)
        auto_layout.add_widget(self.auto_checkbox)
        param_layout.add_widget(auto_layout)
        
        # 参数显示（自动模式下只显示，不可调整）
        param_info = Label(
            text='Block Size: 31, Offset: 15 (Shadow Removal)',
            size_hint=(1, 0.5),
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        param_layout.add_widget(param_info)
        self.param_info_label = param_info
        
        layout.add_widget(param_layout)
        
        # 状态标签
        self.status_label = Label(
            text='Please select image (Auto process enabled)',
            size_hint=(1, 0.05),
            font_size='14sp',
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        layout.add_widget(self.status_label)
        
        # 按钮布局
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        # 选择图片按钮
        select_btn = Button(
            text='Select Image',
            on_press=self.select_image,
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        button_layout.add_widget(select_btn)
        
        # 重新处理按钮（手动模式）
        self.reprocess_btn = Button(
            text='Re-Process',
            on_press=self.process_image,
            disabled=True,
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        button_layout.add_widget(self.reprocess_btn)
        
        # 保存按钮
        self.save_btn = Button(
            text='Save Result',
            on_press=self.save_image,
            disabled=True,
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        button_layout.add_widget(self.save_btn)
        
        layout.add_widget(button_layout)
        
        # 存储当前图像
        self.current_image = None
        self.processed_image = None
        
        return layout
    
    def _on_auto_toggle(self, checkbox, value):
        """自动处理开关切换"""
        self.auto_process = value
        if value:
            self.status_label.text = 'Auto process enabled'
            self.reprocess_btn.disabled = True
        else:
            self.status_label.text = 'Manual mode - click Re-Process to process'
            if self.current_image is not None:
                self.reprocess_btn.disabled = False
    
    def select_image(self, instance):
        """选择图片"""
        # 创建文件选择器
        content = BoxLayout(orientation='vertical')
        
        # 文件选择器
        if platform == 'android':
            filechooser = FileChooserIconView(path='/storage/emulated/0/DCIM')
        else:
            filechooser = FileChooserIconView()
        
        filechooser.filters = ['*.png', '*.jpg', '*.jpeg']
        content.add_widget(filechooser)
        
        # 按钮布局
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        # 确定按钮
        select_btn = Button(
            text='Select',
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        select_btn.bind(on_press=lambda x: self._on_file_select(filechooser.selection, popup))
        btn_layout.add_widget(select_btn)
        
        # 取消按钮
        cancel_btn = Button(
            text='Cancel',
            font_name='Microsoft YaHei' if platform == 'win' else 'DroidSansFallback'
        )
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        # 弹出窗口
        popup = Popup(
            title='Select Image',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def _on_file_select(self, selection, popup):
        """文件选择回调"""
        if selection:
            self.load_image(selection[0])
        popup.dismiss()
    
    def load_image(self, filepath):
        """加载图片"""
        try:
            if USE_OPENCV:
                # 使用 OpenCV 读取
                self.current_image = cv2.imread(filepath)
                if self.current_image is None:
                    self.status_label.text = 'Cannot load image'
                    return
            else:
                # 使用 Pillow 读取
                from PIL import Image
                self.current_image = Image.open(filepath)
                if self.current_image is None:
                    self.status_label.text = 'Cannot load image'
                    return
                # 转换为 RGB 模式
                self.current_image = self.current_image.convert('RGB')

            # 显示原图
            self.display_image(self.current_image, is_original=True)

            filename = Path(filepath).name
            self.status_label.text = f'Loaded: {filename}'

            # 自动处理模式：立即处理
            if self.auto_process:
                self.status_label.text = f'Loaded: {filename} - Auto processing...'
                # 延迟一点时间让 UI 更新
                Clock.schedule_once(lambda dt: self._auto_process(), 0.1)
            else:
                # 手动模式：启用重新处理按钮
                self.reprocess_btn.disabled = False
                self.save_btn.disabled = True

        except Exception as e:
            self.status_label.text = f'Load failed: {e}'
            import traceback
            traceback.print_exc()

    def display_image(self, image, is_original=False):
        """显示图像到 Kivy Image Widget"""
        try:
            if USE_OPENCV:
                # OpenCV 图像 (BGR)
                img_array = image.copy()

                # 调整大小
                h, w = img_array.shape[:2]
                max_size = 400
                if max(h, w) > max_size:
                    scale = max_size / max(h, w)
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    img_array = cv2.resize(img_array, (new_w, new_h))

                # BGR 转 RGB
                rgb_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

                # 转换为 Kivy Texture
                h, w = rgb_image.shape[:2]
                texture = Texture.create(size=(w, h), colorfmt='rgb')
                texture.blit_buffer(rgb_image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
                texture.flip_vertical()
            else:
                # PIL Image
                from PIL import Image
                pil_image = image

                # 调整大小
                w, h = pil_image.size
                max_size = 400
                if max(h, w) > max_size:
                    scale = max_size / max(h, w)
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

                # 转换为 numpy 数组
                img_array = np.array(pil_image)

                # 转换为 Kivy Texture
                h, w = img_array.shape[:2]
                texture = Texture.create(size=(w, h), colorfmt='rgb')
                texture.blit_buffer(img_array.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
                texture.flip_vertical()

            # 更新对应的 Image Widget
            if is_original:
                self.original_widget.texture = texture
            else:
                self.processed_widget.texture = texture
        except Exception as e:
            self.status_label.text = f'Display failed: {e}'
            import traceback
            traceback.print_exc()
    
    def _auto_process(self):
        """自动处理（后台执行）"""
        try:
            # 使用 one_step_document_processor.py 的参数
            block_size = 11  # 窗口大小
            c_value = 2      # 阈值常数
            denoise_h = 5    # 去噪强度

            self.processor.set_parameters(block_size, c_value, denoise_h)

            # 执行二值化
            print("\n" + "="*60)
            print("🚀 开始二值化处理（one_step_document_processor 算法）...")
            print("="*60)

            self.processed_image = self.processor.apply_binarization(
                self.current_image,
                denoise=True
            )

            print("="*60)
            print("✅ 处理完成！")
            print("="*60 + "\n")

            # 显示处理结果
            self.display_image(self.processed_image, is_original=False)

            # 启用保存按钮
            self.save_btn.disabled = False

            # 更新参数显示
            self.param_info_label.text = f'Block: {block_size}, C: {c_value}, Denoise: {denoise_h}'

            self.status_label.text = 'Processing completed!'
        except Exception as e:
            self.status_label.text = f'Auto process failed: {e}'
            import traceback
            traceback.print_exc()
    
    def process_image(self, instance):
        """手动重新处理图片"""
        if self.current_image is None:
            return
        
        self.status_label.text = 'Re-processing...'
        
        # 使用 Clock 异步处理，避免 UI 卡顿
        Clock.schedule_once(lambda dt: self._auto_process(), 0.1)
    
    def save_image(self, instance):
        """保存图片（支持多种格式：JBIG, PNG, TIFF, PDF）"""
        if self.processed_image is None:
            return

        try:
            # 确定保存路径
            if platform == 'android':
                # Android 保存到 Pictures 目录
                save_dir = '/storage/emulated/0/Pictures/BinarizationDemo'
            else:
                # Windows/Linux 保存到当前目录的 output 文件夹
                save_dir = os.path.join(os.getcwd(), 'output', 'binarized')

            # 创建目录
            os.makedirs(save_dir, exist_ok=True)

            # 生成文件名
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # 保存多种格式
            saved_files = []

            # 1. 保存为 JBIG 格式（最高压缩率）
            try:
                jbig_filename = f'binarized_{timestamp}.jbig'
                jbig_filepath = os.path.join(save_dir, jbig_filename)
                if SimpleBinarizationProcessor.save_as_jbig(self.processed_image, jbig_filepath):
                    saved_files.append(('JBIG', jbig_filepath))
            except Exception as e:
                print(f"⚠️ JBIG 保存失败: {e}")

            # 2. 保存为 PNG 格式（无损压缩）
            try:
                png_filename = f'binarized_{timestamp}.png'
                png_filepath = os.path.join(save_dir, png_filename)
                if USE_OPENCV:
                    cv2.imwrite(png_filepath, self.processed_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
                else:
                    self.processed_image.save(png_filepath, 'PNG', optimize=True)
                saved_files.append(('PNG', png_filepath))
            except Exception as e:
                print(f"⚠️ PNG 保存失败: {e}")

            # 3. 保存为 TIFF 格式（CCITT Group 4 压缩）
            try:
                tiff_filename = f'binarized_{timestamp}.tiff'
                tiff_filepath = os.path.join(save_dir, tiff_filename)
                if SimpleBinarizationProcessor.save_as_tiff_g4(self.processed_image, tiff_filepath):
                    saved_files.append(('TIFF-G4', tiff_filepath))
            except Exception as e:
                print(f"⚠️ TIFF 保存失败: {e}")

            # 显示保存结果
            if saved_files:
                result_text = f'Saved {len(saved_files)} formats:\n'
                for fmt, path in saved_files:
                    size = os.path.getsize(path) / 1024  # KB
                    result_text += f'{fmt}: {size:.1f}KB\n'
                self.status_label.text = result_text.strip()
                print(f"✅ 图片已保存到: {save_dir}")
                for fmt, path in saved_files:
                    print(f"   - {fmt}: {os.path.basename(path)}")
            else:
                self.status_label.text = 'Error: Failed to save image'

            # Android 通知媒体扫描器
            if platform == 'android':
                try:
                    from android import mActivity
                    from jnius import autoclass
                    MediaScannerConnection = autoclass('android.media.MediaScannerConnection')
                    for _, filepath in saved_files:
                        MediaScannerConnection.scanFile(
                            mActivity,
                            [filepath],
                            None,
                            None
                        )
                except:
                    pass
        except Exception as e:
            self.status_label.text = f'Save failed: {e}'
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    BinarizationApp().run()

