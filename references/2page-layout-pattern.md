# 两页版PDF排版模式

本文件记录了在"PDF不超过两页A4"约束下的HTML/CSS排版技术。适用于六维企业分析PDF生成。

## 核心排版策略

| 策略 | 效果 | 实现方式 |
|------|------|---------|
| Logo与h1并排 | 省一整行（~0.8cm） | `flex + justify-content: space-between` |
| 去掉`---`板块分隔线 | 省约0.15cm×5=0.75cm | 仅保留header-bottom一条底线 |
| blockquote内换行改`·`分隔 | 省垂直空间 | 用`<br>`仅在最必要处分行 |
| 表格≤6行/字号9pt | 省1/3表格高度 | 只保留营收/利润/研发/员工/现金流/资产 |
| 创始人矩形右侧 | 比圆形更紧凑 | `flex-direction: row-reverse`，width≤90px |
| 产品展示4并排置底 | 集中展示产品线 | width≤100px，gap 0.8em |
| 板块间距0.7em | 呼吸感而非密排 | section-header上间距0.7em |

## 用户偏好：宁可"松"不要"挤"

**历史教训**：2026-06-05用户评价排版"太密集拥挤"。修复方向是整体往松调，而非压缩塞更多内容。经验证，以下偏松的值能稳定卡在2页内：

| 参数 | 拥挤版（被批评） | 宽松版（验证通过） |
|------|----------------|------------------|
| 页边距 | 1.3cm | **1.5cm** |
| body行高 | 1.5-1.6 | **1.7**（blockquote内**1.85**） |
| blockquote内边距 | 0.3em 0.7em | **0.5em 0.9em** |
| 板块间间距 | 0.3-0.4em | **0.7em** |
| h1字号 | 16-18pt | **22pt**（加2px letter-spacing） |
| h2字号 | 10-11pt | **12pt**（加1px letter-spacing） |
| 表格字号 | ≤8pt | **9pt**（加"说明"列替代纯"同比"） |
| 创始人照片 | 圆形72px左侧 | **矩形90px右侧** |

**原则**：在2页硬约束内，优先用满空间做呼吸感，而非塞更多内容。字数不够就精炼文本，不要压缩间距。

## HTML结构模板

```html
<div class="header-row">
  <h1>公司名</h1>
  <img src='...base64...' alt="Logo">
</div>
<div class="bq"><!-- 定位+主营业务 --></div>

<div class="section-header">核心人物</div>
<div class="founder-layout"><!-- flex-direction: row-reverse -->
  <div class="f-img"><img src='...base64...' alt="人物"></div>
  <div class="f-text">...</div>
</div>

<div class="section-header">技术自主与知识产权</div>
<div class="bq">...</div>

<div class="section-header">经济贡献与经营数据</div>
<table>...6行...</table>

<div class="section-header">供应链与区域布局</div>
<div class="bq">...</div>

<div class="section-header">竞争与市场结构</div>
<div class="bq">...</div>

<!-- 相关产品展示区：至少4个不同领域 -->
<div class="product-showcase">
  <div class="stitle">相关产品</div>
  <div class="gallery">
    <div class="item"><img src='...'><div class="label">产品A（领域1）</div></div>
    <div class="item"><img src='...'><div class="label">产品B（领域2）</div></div>
    <div class="item"><img src='...'><div class="label">产品C（领域3）</div></div>
    <div class="item"><img src='...'><div class="label">产品D（领域4）</div></div>
  </div>
</div>

<div class="source-block">来源信息</div>
```

## 关键CSS

```css
@page { size: A4; margin: 1.5cm; }

.header-row {
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 2.5px solid var(--brand-color, #cf0a2c);
  padding-bottom: 0.3em; margin-bottom: 0.8em;
}
.header-row h1 { font-size: 22pt; color: var(--brand-color); margin: 0; letter-spacing: 2px; }
.header-row img { height: 30px; }

.section-header { font-size: 12pt; font-weight: bold; letter-spacing: 1px; margin: 0.7em 0 0.3em 0; color: #333; }

.bq {
  background: #f7f7f7; border-left: 3.5px solid var(--brand-color);
  padding: 0.5em 0.9em; margin: 0.15em 0 0.1em 0;
  font-size: 9.5pt; line-height: 1.85;
}

table { width: 100%; border-collapse: collapse; margin: 0.2em 0; font-size: 9pt; }
th { background: var(--brand-color); color: white; padding: 0.3em 0.6em; text-align: left; }
td { border: 1px solid #ddd; padding: 0.25em 0.6em; }
tr:nth-child(even) td { background: #f9f9f9; }

/* 创始人：矩形，右侧 */
.founder-layout { display: flex; align-items: flex-start; gap: 0.9em; flex-direction: row-reverse; }
.founder-layout .f-img img { width: 90px; height: auto; object-fit: contain; border: 2px solid var(--brand-color); border-radius: 2px; }

.tag { display: inline-block; background: var(--brand-color); color: white; padding: 0.1em 0.5em; border-radius: 3px; font-size: 8pt; }

/* 相关产品展示区：4+并排 */
.product-showcase { margin: 0.5em 0 0.3em 0; }
.product-showcase .stitle { font-size: 12pt; font-weight: bold; color: #333; letter-spacing: 1px; margin-bottom: 0.25em; }
.product-showcase .gallery { display: flex; justify-content: center; gap: 0.8em; flex-wrap: wrap; }
.product-showcase .gallery .item { text-align: center; width: 110px; }
.product-showcase .gallery .item img { max-width: 100px; max-height: 80px; object-fit: contain; border: 1px solid #eee; border-radius: 4px; padding: 3px; background: #fafafa; }
.product-showcase .gallery .item .label { font-size: 7pt; color: #888; margin-top: 0.15em; line-height: 1.3; }

.source-block { margin-top: 0.8em; padding-top: 0.4em; border-top: 1px solid #ccc; font-size: 7.5pt; color: #999; }
.hl { color: var(--brand-color); font-weight: bold; }
```

## weasyprint 图片嵌入

- 使用 `data:image/...;base64,...` 格式嵌入
- **`src`属性必须用单引号**：`src='data:...'` 而非 `src="data:..."`（weasyprint解析 `src=\"...\"` 会报错）
- **灰度JPEG防坑**：所有JPEG嵌入前检查 mode，L→RGB 转换（fetch_images.py 已自动处理）

## 两页检验

```python
import fitz
doc = fitz.open('report.pdf')
assert 1 <= len(doc) <= 2, f"PDF页数超出范围：{len(doc)}页"
# 确认所有嵌入图片为3通道
for i in range(len(doc)):
    for img in doc[i].get_images(full=True):
        pix = fitz.Pixmap(doc, img[0])
        assert pix.n >= 3, f"第{i+1}页有{pix.n}通道图片（应为3+）"
```
