# SPA网站（Nuxt/Vue/React）图片抓取回退方案

## 问题

拓维信息（talkweb.com.cn）使用 Nuxt.js，所有页面内容由 JS 动态渲染。`fetch_images.py` 的 `requests` + HTML regex 抓取不到任何图片URL。

## 实测结论

- 官网产品页 / 首页：0 张图片可抓取（纯 SPA，JS 渲染）
- 百度百科：人机验证拦截 curl
- simpleicons：无 `talkweb` 条目
- 百度图片搜索：返回空

## Logo 回退方案

3 步搞定 SPA 站点的 logo：

```bash
# 1. 下载 favicon.ico（几乎所有 SPA 站点都有）
curl -sL "https://www.{domain}/favicon.ico" -o image/logo.ico

# 2. 转为 PNG（weasyprint 兼容）
python3 -c "
from PIL import Image
img = Image.open('image/logo.ico')
img.convert('RGB').save('image/logo.png', 'PNG')
"
```

## 产品图回退方案

所有图片源均失败时，生成彩色占位图：

```python
from PIL import Image, ImageDraw, ImageFont
products = [
    ('product_产品1', '产品\n名称', '#2563EB'),
    ('product_产品2', '另一\n产品', '#16A34A'),
]
for fname, label, color in products:
    img = Image.new('RGB', (200, 140), color)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc', 22)
    # 居中文字
    bbox = d.textbbox((0, 0), label, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text(((200-tw)//2, (140-th)//2), label, fill='white', font=font)
    img.save(os.path.join(outdir, fname + '.png'))
```

占位图使用不同品牌色区分 4 个领域，视觉上可替代实拍产品图。
