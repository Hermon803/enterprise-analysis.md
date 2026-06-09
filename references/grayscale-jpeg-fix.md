# 灰度JPEG（PIL mode L）导致 weasyprint 渲染失败

## 现象

PDF 中图片区域显示为空白，或 weasyprint 报 "parameter error"。用 PyMuPDF 检查时发现图片通道数 `n=1`（正常应为 `n=3` 或 `n=4`）。

## 根因

PIL 打开灰度 JPEG 时 mode 为 `L`（1通道），base64 嵌入 HTML 后 weasyprint 无法渲染单通道 JPEG。

## 检查方法

```python
from PIL import Image
im = Image.open('founder.jpg')
print(f'{im.size} mode={im.mode}')  # 如果 mode='L' → 问题图片
```

## 修复

```python
from PIL import Image
im = Image.open('founder.jpg')
if im.mode == 'L':
    im = im.convert('RGB')
    im.save('founder.jpg', 'JPEG', quality=95)
```

## 自动防护

`fetch_images.py` 的 `download()` 函数 已内置 L→RGB 转换。每次下载 JPEG 文件时自动检查并修正，无需手动处理。

`execute_code` 生成 HTML 前，建议对所有 JPG/JPEG 文件批量做一次检查：

```python
from PIL import Image
import os

img_dir = "./image"
for f in os.listdir(img_dir):
    if not f.lower().endswith(('.jpg', '.jpeg')):
        continue
    im = Image.open(os.path.join(img_dir, f))
    if im.mode == 'L':
        rgb = im.convert('RGB')
        rgb.save(os.path.join(img_dir, f), 'JPEG', quality=95)
        print(f"  L→RGB: {f}")
```

## 受影响文件

- 百度百科下载的 JPEG（经常是灰度图，如人物肖像 200×200 灰度照）
- 部分旧版数码相机拍摄的 JPEG
