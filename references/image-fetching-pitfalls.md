# 图片抓取实战记录

`scripts/fetch_images.py` 在多次实战中积累的经验和防坑策略。

## 灰度 JPEG 导致 weasyprint 渲染失败

**症状**：PDF生成成功但JPEG图片在PDF中显示为空白或"参数错误"。PIL检查图片为模式 `L`（灰度）。

**原因**：WeasyPrint 对灰度 JPEG（PIL mode L，单通道）的 base64 内嵌渲染存在兼容问题。PDF中的图片编码会失败或显示异常。

**诊断**：
```python
from PIL import Image
im = Image.open('founder.jpg')
print(im.mode)  # 如果是 'L' → 灰度，需要转换
```

**修复**：在 embedding 图片进入 HTML 之前，将所有灰度 JPEG 转换为 RGB：
```python
if im.mode == 'L':
    im = im.convert('RGB')
    im.save(path, 'JPEG', quality=95)
```

**预防**：`fetch_images.py` 的 `download()` 函数下载后自动做此转换。如果手动添加图片到 `image/` 目录，务必检查模式是否为 L。

## 核心发现：requests 在某些站点被拦截

### 百度百科 403

**症状**：Python requests 访问 `baike.baidu.com/item/*` 返回 403，curl 同URL+同Headers返回200。

**原因**：Baidu 识别 urllib3/requests 的 TLS 指纹并直接拦截，curl 的 libcurl 指纹通过。

**解决方案**：在 `fetch_founder_from_baidu()` 中用 subprocess curl 代替 requests：

```python
cmd = [
    "curl", "-sL", "--connect-timeout", "10",
    "-H", "User-Agent: Mozilla/5.0 ... Safari/537.36",
    "-H", "Accept: text/html,application/xhtml+xml",
    "-H", "Cookie: BAIDUID=0123456789ABCDEF:FG=1; BIDUPSID=0123456789ABCDEF",
    search_url,
]
result = subprocess.run(cmd, capture_output=True, timeout=15)
```

关键点：`Cookie` 头必须携带（值任意有效格式即可）。

### 官网 CDN 拦截

**症状**：`consumer-img.huawei.com` 等官网CDN返回HTML（验证页/重定向），即使加了浏览器UA。

**应对**：
- 优先从第三方源（百度百科、科技媒体）获取产品图
- 部分官网（如 `www.grandtec-ic.com`）无此限制，curl直达
- 兜底：用Logo本身作为产品占位图

## 产品图静态度 vs JS渲染

| 企业 | 产品页类型 | 策略 |
|------|-----------|------|
| grandtec-ic.com | 静态HTML | curl 官网产品页，`grep -i img` 提取，支持data-src |
| nvidia.com/product | JS渲染 | 改用 `nvidia.com/en-us/geforce/news/`（静态页，含GPU产品图） |
| huawei.com | CDN验证 | 无法直接抓取，需第三方源 |

**教训**：对于大厂JS渲染页面，找其新闻/媒体静态页面比想办法渲染更快。

## 图片去重

`fetch_product()` 接收 `skip_urls` 参数（已下载的logo/founder路径集合），产品抓取时跳过。避免产品图与创始人图重复的问题——这在"关于我们"页面既有产品图又有团队照片时尤其重要。

```python
# main() 中收集已用URL
used_urls.add(os.path.abspath(logo_path))
used_urls.add(os.path.abspath(founder_path))
results["product"] = fetch_product(domain, output_dir, company, skip_urls=used_urls)
```

## NVIDIA 产品图的特殊处理

**问题**：`nvidia.com/product` 是 JS 渲染页面，curl 拿不到任何产品图片。

**解法**：`nvidia.com/en-us/geforce/news/` 是静态HTML页面，包含当前 GPU 产品新闻配图（625x330 JPEG），直接用 curl 抓取 HTML 后提取 `src` 属性即可获得产品图。

```python
if "nvidia" in domain.lower():
    strategies.append("https://www.nvidia.com/en-us/geforce/news/")
```

**通用教训**：大厂的产品页常是SPA/JS渲染。找其"新闻"、"媒体"、"Press" 等静态页面往往比对抗JS渲染更高效。

## 图片有效性校验

不仅仅是检查 HTTP 200，还要用 PIL 验证：

```python
def validate_image(data):
    try:
        img = Image.open(BytesIO(data))
        img.verify()
        return True, img.format.lower()
    except Exception:
        return False, None
```

同时检查 Content-Type 和文件头，跳过HTML响应。

## fetch_images.py 参数速查

```bash
python3 scripts/fetch_images.py \
  --company "公司中文名" \
  --domain "company.com" \
  --english "company" \        # simpleicons.org 用
  --founder "创始人姓名" \       # 百度百科搜索用
  --output ./image/
```

输出目录自动创建。三张图分别命名为 `logo.*`, `founder.*`, `product.*`。
