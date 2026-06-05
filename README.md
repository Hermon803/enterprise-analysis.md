# 企业分析 · AI产业链企业六维分析

跨工具的 AI 产业链企业分析 skill/规则包。

## 适用工具

| 工具 | 使用方式 |
|------|---------|
| **Hermes Agent** | `skill_view(name='enterprise-analysis')` 或把 `skill-企业分析/SKILL.md` 放入 `~/.hermes/skills/` |
| **Claude Code** | 项目根目录放 `CLAUDE.md`，或 `claude --patch -p "按 CLAUDE.md 规则分析华为"` |
| **Workbuddy** | 导入 `workbuddy/企业分析.md` 到 workbuddy rules 目录 |
| **其他 Agent** | 直接读 `CLAUDE.md` 或 `skill-企业分析/SKILL.md` |

## 六维分析框架

1. **企业介绍与主营业务** — 全称/成立/总部/性质/标签/主营业务
2. **核心人物** — 创始人/CEO籍贯/毕业院校/关键履历
3. **技术与知识产权** — 国产化率/核心依赖/专利/PCT/标准参与
4. **经济贡献与经营数据** — 营收/利润/税收/就业/上下游
5. **供应链与区域布局** — 芯片依赖/替代进展/供应链评级/总部/生产
6. **竞争与市场结构** — 份额排名/竞争格局/对中小企业影响

## 输出制品

每个分析产出三种文件：
- `[公司名]_企业分析.md` — 完整Markdown报告
- `[公司名]_企业分析.pdf` — A4 PDF（含图，不超过2页）
- `[公司名]_企业分析.docx` — Word文档

**报告包含：**
- ✅ 六个维度的结构化分析
- ✅ 公司Logo（h1同行右上）
- ✅ 创始人照片（圆形裁切）
- ✅ 相关产品展示区（底部，1-2个代表性产品图并排，互联网公司用App图标）
- ✅ 数据来源标注

## 自动图片抓取

配套 `scripts/fetch_images.py` 脚本自动拉取三张图：

```bash
python3 scripts/fetch_images.py \
  --company "公司名" --domain "域名" \
  --english "英文名" --founder "创始人名" \
  --output ./image/
```

支持场景：
- 实体企业：Logo + 创始人 + 产品图 ✓
- 互联网企业：Logo + App图标（product位）✓
- 大厂（NVIDIA/华为等）：特定路径策略 ✓

## 排版规则（PDF 2页版）

- A4 · 边距1.5cm · Noto Sans CJK SC
- h1+logo flex同行（h1左 logo右，h1 22pt品牌色）
- blockquote行高1.85，内边距0.5em 0.9em
- 表格9pt，分"数据"与"说明"列
- 关键数据红色加粗高亮
- 无分隔线，0.7em间距自然分隔
- 底部"相关产品"展示区 + 数据源

## 目录结构

```
├── README.md
├── CLAUDE.md                    ← Claude Code 格式
├── skill-企业分析/
│   └── SKILL.md                 ← Hermes Agent 格式（YAML frontmatter）
├── workbuddy/
│   └── 企业分析.md              ← Workbuddy 格式
├── scripts/
│   └── fetch_images.py          ← 自动图片抓取脚本
└── examples/
    └── 华为/                    ← 华为分析完整成品示例
        ├── 华为_企业分析.md
        ├── 华为_企业分析.pdf
        └── image/
```

## 安装到 Hermes

```bash
# 方式一：克隆仓库
cd ~/.hermes/skills/analysis/
git clone git@github.com:Hermon803/enterprise-analysis.md.git enterprise-analysis

# 方式二：使用命令加载
hermes skill view enterprise-analysis
```

## 安装到 Claude Code

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
cd /path/to/your/project
claude "按照规则分析以下企业：华为"
```

## License

MIT
