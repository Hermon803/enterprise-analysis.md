# 中文排版CSS最佳实践

## 核心原则

1. **自然语句替代标签列表**：避免 `**字段名**：值 · 值 · 值` 格式，用完整句子
2. **两端对齐**：中文字体 `text-align: justify` 避免右侧参差不齐
3. **行高 ≥ 1.8**：中文正文 line-height 1.8-1.9 可读性最佳
4. **字号层级清晰**：h1=20-22pt → h2=10.5-11pt → 正文/blockquote=9-9.5pt → 表格=8.5-9pt → 注释=6.5-7pt
5. **色彩系统**：品牌色统一 `:root { --brand: #2563EB; }`，正文 `#1e293b`(slate-800)，注释 `#94a3b8`

## 推荐CSS

```css
body { font-family: 'Noto Sans CJK SC', 'PingFang SC', 'Microsoft YaHei', sans-serif; color: #1e293b; }
p, .bq { text-align: justify; }
p { font-size: 9.5pt; line-height: 1.9; }
.bq { font-size: 9.5pt; line-height: 1.9; padding: 0.5em 0.8em; }
h2 { font-size: 11pt; letter-spacing: 1px; }
table { font-size: 9pt; }
```

## 两页均衡策略

当第二页仅剩产品展示区+数据源（约15%页高），不要缩小字号试图"拉回"内容，而是：

1. **增大字号+行高**：正文 8pt→9.5pt，h2 10pt→11pt，让页1内容自然溢出到页2
2. **增大边距**：1.3cm→1.5cm
3. **放大页2元素**：产品图面积翻倍（72×50→110×75）、blockquote 字号单独+0.5pt
4. **目标比例**：页1:页2 ≈ 60:40（按中文字数）

## 内容表述

- 定位/简介区块用一段话而非 `**字段**：值` 格式
- 核心人物只保留创始人/CEO，去掉全部管理层名单
- 竞争分析包含竞对营收对比（如"东华软件约120亿，软通动力约180亿"）
