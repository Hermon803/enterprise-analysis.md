# 相关产品展示区 · HTML/CSS 模板

插入位置：PDF 报告底部，竞争与市场结构板块之后、数据源区块之前。

## 标准模板（硬件/实体企业，4+产品）

```html
<!-- 相关产品展示区 -->
<div class="product-showcase">
  <div class="stitle">相关产品</div>
  <div class="gallery">
    <div class="item">
      <img src='data:image/...;base64,...' alt="产品1">
      <div class="label">产品1（领域A）</div>
    </div>
    <div class="item">
      <img src='data:image/...;base64,...' alt="产品2">
      <div class="label">产品2（领域B）</div>
    </div>
    <div class="item">
      <img src='data:image/...;base64,...' alt="产品3">
      <div class="label">产品3（领域C）</div>
    </div>
    <div class="item">
      <img src='data:image/...;base64,...' alt="产品4">
      <div class="label">产品4（领域D）</div>
    </div>
  </div>
</div>
```

## CSS

```css
.product-showcase { margin: 0.4em 0 0.2em 0; }
.product-showcase .stitle {
  font-size: 12pt; font-weight: bold; color: #333;
  letter-spacing: 1px; margin-bottom: 0.25em;
}
.product-showcase .gallery {
  display: flex; justify-content: center;
  gap: 0.8em; flex-wrap: wrap;
}
.product-showcase .gallery .item {
  text-align: center; flex: 0 0 auto; width: 110px;
}
.product-showcase .gallery .item img {
  max-width: 100px; max-height: 80px;
  object-fit: contain; border: 1px solid #eee;
  border-radius: 4px; padding: 3px; background: #fafafa;
}
.product-showcase .gallery .item .label {
  font-size: 7pt; color: #888; margin-top: 0.15em; line-height: 1.3;
}
```

## 互联网公司变体（App图标，4+）

```html
<div class="product-showcase">
  <div class="stitle">相关产品</div>
  <div class="gallery">
    <div class="item">
      <img src='data:image/...;base64,...' style="max-width:60px;" alt="App1">
      <div class="label">App名称1</div>
    </div>
    <div class="item">
      <img src='data:image/...;base64,...' style="max-width:60px;" alt="App2">
      <div class="label">App名称2</div>
    </div>
    <div class="item">
      <img src='data:image/...;base64,...' style="max-width:60px;" alt="App3">
      <div class="label">App名称3</div>
    </div>
    <div class="item">
      <img src='data:image/...;base64,...' style="max-width:60px;" alt="App4">
      <div class="label">App名称4</div>
    </div>
  </div>
</div>
```

## 产品图选择规则

1. **实体企业** → 选 **至少4个不同领域** 最具代表性的产品（如：华为→麒麟芯片、旗舰手机、华为云、问界汽车）
2. **半导体设备企业** → 选不同产品线设备（如：格芯→AOI检测、分选机、晶圆检测、激光打标）
3. **互联网/软件公司** → 用 App 图标，≥4个不同产品（从 simpleicons.org 或官网下载）
4. **产品图去重**：产品图不得与 logo/创始人图重复（fetch_images.py 自动处理）
5. **无产品图兜底** → 用公司 logo 居中替代，标注"产品图待补充"

## 注意事项

- 产品图必须 **base64 嵌入**，不走外部 URL（weasyprint 不支持外部URL）
- 两页版中产品图压缩到 max-width:100px（App图标60px）以节省空间
- 如使用 fetch_images.py 脚本，自动去重保证产品图与 logo/创始人不同
- 产品图应体现不同业务领域，而非同一领域的不同型号
