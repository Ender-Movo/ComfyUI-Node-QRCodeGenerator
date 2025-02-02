import torch
import numpy as np
import qrcode
from PIL import Image
from nodes import SaveImage

class QRCodeGenerator:
    """
    生成二维码图像的节点
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "size": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 4096,
                    "step": 64
                }),
                "text": ("STRING", {
                    "multiline": True,
                    "default": "https://github.com",
                    "dynamicPrompts": False
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "generate_qr"
    CATEGORY = "image/QRCode"

    def generate_qr(self, text, size):
        # 创建二维码对象
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        
        # 添加数据并生成二维码
        qr.add_data(text)
        qr.make(fit=True)
        
        # 生成PIL图像并转换为RGB
        pil_image = qr.make_image(fill_color="black", back_color="white")
        pil_image = pil_image.convert("RGB")
        
        # 调整到指定尺寸
        pil_image = pil_image.resize((size, size), Image.LANCZOS)
        
        # 转换为PyTorch张量
        image_array = np.array(pil_image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_array)[None,]
        
        return (image_tensor,)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "QRCodeGenerator": QRCodeGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QRCodeGenerator": "🔳 QR Code Generator"
}