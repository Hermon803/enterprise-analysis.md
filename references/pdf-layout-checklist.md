# PDF 排版检查清单（生成前逐项核对）

## 字体

- [ ] `@font-face` src 路径指向 `/usr/share/fonts/opentype/noto/`（非 truetype/noto/）
- [ ] `ls /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` 存在
- [ ] h2 使用 Medium 字重（`NotoSansCJK-Medium.ttc`）或 Bold
- [ ] 正文字号 >= 10pt，h2 >= 13pt

## 表格

- [ ] 数值列右对齐 + `tabular-nums`
- [ ] 负值使用 `.neg { color: #DC2626; }`
- [ ] 单元格 padding >= 4px 10px
- [ ] 顶边线 + 底边线闭合表格
- [ ] 斑马线 >= `#F1F5F9`

## 分页控制

- [ ] `h2, h3 { page-break-after: avoid; }`
- [ ] `table, .bq, .founder-row { page-break-inside: avoid; }`
- [ ] `body { widows: 2; orphans: 2; }`

## 色彩

- [ ] 表头用 `--brand-dark`（#1D4ED8），非主品牌色
- [ ] `.tag` 用浅蓝背景 + 深蓝文字
- [ ] 负值/亏损红色标记

## 间距

- [ ] `p { margin-bottom: >= 0.5em }`
- [ ] `h2 { margin-top: >= 0.9em; margin-bottom: 0.3em }`
- [ ] 产品区有视觉分隔（边框或背景框）

## 图片

- [ ] 创始人照片已压缩（thumbnail + quality 80）
- [ ] 产品图 width >= 100px
- [ ] 产品标签 font-size >= 8.5pt
- [ ] 灰度 JPEG 已转 RGB
