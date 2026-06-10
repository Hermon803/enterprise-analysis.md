# 核心产品展示区 · HTML 表格模板

插入位置：PDF 报告底部，第⑥板块（市场份额与生态安全）之后、数据源区块之前。

## 标准表格模板（4+产品，三列：产品名称 | 发布时间 | 介绍）

```html
<div class="product-section">
<h3>核心产品</h3>
<table class="products">
<tr><th>产品名称</th><th>发布时间</th><th>产品介绍</th></tr>
<tr><td class="pname">产品A</td><td>2024年3月</td><td>简要功能描述，一句话</td></tr>
<tr><td class="pname">产品B</td><td>2023年8月</td><td>简要功能描述，一句话</td></tr>
<tr><td class="pname">产品C</td><td>2022年12月</td><td>简要功能描述，一句话</td></tr>
<tr><td class="pname">产品D</td><td>2021年6月</td><td>简要功能描述，一句话</td></tr>
</table>
</div>
```

## CSS

```css
.product-section { margin-top: 0.7em; page-break-inside: avoid; }
.product-section h3 {
  font-family: 'Noto Sans CJK SC Med','PingFang SC','Microsoft YaHei',sans-serif;
  font-size: 12pt; color: var(--brand-dark); letter-spacing: 1px; margin-bottom: 0.15em;
}
table.products { width: 100%; font-size: 9pt; border-collapse: collapse; }
table.products th {
  background: var(--brand-dark); color: white; padding: 3px 8px; text-align: left; font-weight: normal;
}
table.products th:first-child { width: 25%; }
table.products th:nth-child(2) { width: 18%; text-align: center; }
table.products td { padding: 2.5px 8px; border-bottom: 0.5px solid var(--border); }
table.products td:nth-child(2) { text-align: center; color: var(--text-sec); font-size: 8.5pt; }
table.products tr:last-child td { border-bottom: 1.5px solid var(--brand-dark); }
table.products .pname { font-weight: bold; color: #1E293B; }
```

## 列说明

| 列 | 宽度 | 内容要求 |
|----|------|---------|
| 产品名称 | 25% | 加粗，简明产品/服务名（如"Mate 70系列""昇腾910B"），不加"华为"等公司前缀 |
| 发布时间 | 18% | 精确到**月份**（如"2024年11月""2022年5月"），居中显示，用次色 #64748B 字号8.5pt |
| 产品介绍 | 57% | 简要说明核心功能或定位，一行以内，避免换行 |

## 产品选择规则

1. **实体企业** → 选 **至少4个不同领域** 最具代表性的产品（如：华为→麒麟芯片、旗舰手机、华为云、问界汽车）
2. **半导体设备企业** → 选不同产品线设备（如：格芯→AOI检测、分选机、晶圆检测、激光打标）
3. **互联网/软件公司** → 展示核心App或服务（如：微信、腾讯云、腾讯视频、腾讯游戏）
4. **产品名称列** 加粗，产品介绍列简要说明（一行以内，避免换行）
5. **至少4行**，不足时从次要产品中补充
6. **发布时间** 精确到月份，不确定的标注年份（如"2020年"），切勿编造具体日期

## 注意事项

- 该表格替代了旧版的产品图片展示区，不再需要抓取/嵌入产品图片
- 表格宽度 100%，三列宽度分配：25% | 18% | 57%
- 保持文字精简，产品介绍不超过一行
