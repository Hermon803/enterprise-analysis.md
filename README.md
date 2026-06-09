<p align="center">
  <img src="https://img.shields.io/badge/status-active-success?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/agent-Hermes%20%7C%20Claude%20Code%20%7C%20Codex%20%7C%20Workbuddy-8A2BE2?style=flat-square" alt="Agents">
  <img src="https://img.shields.io/badge/output-MD%20%7C%20PDF%20%7C%20DOCX-orange?style=flat-square" alt="Output">
</p>

<h1 align="center">📊 企业分析 · AI产业链企业六维分析</h1>

<p align="center">
  <strong>跨 Agent 的企业分析规则包</strong><br>
  输入公司名 → 输出六维结构化报告（MD + PDF + DOCX），含 Logo、创始人照片、产品图
</p>

---

## 📖 目录

- [这是什么](#-这是什么)
- [快速开始](#-快速开始)
- [六维分析框架](#-六维分析框架)
- [输出制品](#-输出制品)
- [图片系统](#-图片系统)
- [排版规范](#-排版规范)
- [数据源](#-数据源)
- [目录结构](#-目录结构)
- [安装到各 Agent](#-安装到各-agent)
- [实战案例](#-实战案例)
- [License](#-license)

---

## 🧭 这是什么

一个让 AI Agent 能**自动生成专业级企业分析报告**的规则包。适用于：

- **信创/半导体/AI 产业链研究** — 快速生成标准化企业画像
- **投资/尽调场景** — 六维框架覆盖企业核心维度，格式统一便于横向对比
- **管理层简报** — 2 页 A4 PDF，含数据表格和产品展示，直接交付

覆盖的企业类型：

| 类型 | 数据可用性 | 示例 |
|------|-----------|------|
| **A股上市** | ✅ 完整10项财务指标 | 拓维信息、比亚迪、华为 |
| **港股上市** | ✅ 完整财务数据 | 腾讯（0700.HK） |
| **美股上市** | ✅ 完整财务数据 | NVIDIA（NVDA） |
| **拟上市/独角兽** | ⚠️ 招股书数据 | 宇树科技（科创板 IPO 中） |
| **非上市中小企业** | ❌ 仅公开注册信息 | — |

---

## ⚡ 快速开始

```bash
# Hermes Agent 加载 skill
hermes skill view enterprise-analysis

# 按规则分析企业（Agent 自动执行六维流程）
"使用企业分析skill，分析一下NVIDIA"
"企业分析 拓维信息 talkweb.com.cn talkweb"
```

Agent 会自动执行：

```
Step 0 → 检查本地已有文件
Step 1 → 并行搜集经营数据/核心人物/技术专利 ← 3路并发
Step 2 → 按自然语句风格撰写六维报告
Step 3 → 图片抓取（Logo + 创始人 + 产品图）
Step 4 → 生成 HTML + base64 嵌入图片 → PDF（WeasyPrint）
Step 5 → pandoc 生成 DOCX
         └─ 输出: ./[公司名]_企业分析.{md, pdf, docx}
```

---

## 🏛️ 六维分析框架

每个分析有且仅有以下六个维度：

| # | 维度 | 内容覆盖 | 数据来源 |
|---|------|---------|---------|
| ① | **企业介绍与主营业务** | 成立时间、总部、上市情况、业务板块、市场定位 | 官网/Wikipedia/年报 |
| ② | **核心人物** | 创始人/CEO 姓名、籍贯、教育背景、关键履历（仅保留1人） | 百度百科/Wikipedia |
| ③ | **技术与知识产权** | 专利数、软著、标准参与、研发投入、研发平台 | 年报/Wikipedia/官网 |
| ④ | **经济贡献与经营数据** | **10 项固定指标 × 3 年**（营收/毛利率/净利/现金流/研发/员工/资产） | 年报/招股书/Yahoo Finance |
| ⑤ | **供应链与区域布局** | 核心芯片/技术依赖、总部/研发/生产基地分布 | 年报/公开报道 |
| ⑥ | **竞争与市场结构** | 主要竞争者、市场份额、差异化优势、风险因素 | 年报/行业报告 |

### 固定财务指标模板

```
| 指标             | 2023年  | 2024年  | 2025年  |
|-----------------|---------|---------|---------|
| 营业总收入       | 填入    | 填入    | 填入    |
| 营收同比增速     | —       | 自动    | 自动    |
| 毛利率           | 填入    | 填入    | 填入    |
| 归母净利润       | 填入    | 填入    | 填入    |
| 净利率           | 自动    | 自动    | 自动    |
| 经营活动现金流   | 填入    | 填入    | 填入    |
| 研发投入         | 填入    | 填入    | 填入    |
| 研发占营收比     | —       | 自动    | 自动    |
| 员工总数         | 填入    | 填入    | 填入    |
| 总资产           | 填入    | 填入    | 填入    |
```

> 非上市企业不可获取的字段标注「未公开披露」。拟上市企业可提取招股书数据。

---

## 📦 输出制品

每个分析产生 **3 种文件**：

```
[公司名]_企业分析.md    → 完整六维 Markdown 报告
[公司名]_企业分析.pdf   → 2 页 A4 PDF（含 Logo + 创始人照 + 4 产品图）
[公司名]_企业分析.docx  → Word 文档（pandoc 转换）
```

### PDF 排版规格

| 属性 | 规格 |
|------|------|
| 纸张 | A4，边距 1.6cm |
| 字号层级 | h1=20pt → h2=12pt → 正文=9.5pt → 表格=8.5pt |
| 字体 | Noto Sans CJK SC / PingFang SC / Microsoft YaHei（跨平台 fallback） |
| 首行 | h1（公司名，无后缀）+ Logo（SVG/PNG flex 同行） |
| 表格 | 顶部/底部闭合边线 + 数字右对齐 + 负值红色 + 斑马线 |
| 产品展示 | 底部 4 图并排，title + tag + sub-label |
| 数据源 | 底栏浅灰小字 |
| 分页控制 | widows/orphans + page-break-inside:avoid |

---

## 🖼️ 图片系统

支持两种图片来源，自动检测：

### 方式 A：用户预置（优先）

```bash
# 在 image/ 目录放入以下文件即可，Agent 自动识别跳过抓取
image/
├── logo.png / logo.svg        ← 公司 Logo
├── founder.png / founder.jpg  ← 创始人照片
└── product_*.png              ← 产品图（≥4张，按文件名排序）
```

### 方式 B：自动抓取

```bash
python3 scripts/fetch_images.py \
  --company "公司名" --domain "域名" \
  --english "英文名" --founder "创始人名" \
  --output ./image/
```

抓取优先级：

| 图片 | 来源链 |
|------|--------|
| **Logo** | simpleicons.org → 官网 favicon/og:image → curl 官网 |
| **创始人** | 百度百科（curl 绕过 403） → 官网 about 页面 |
| **产品图** | 官网产品页 → 国内科技媒体 → 第三方评测 |
| **兜底** | favicon→PNG 转 Logo + PIL 生成产品占位图 |

---

## 📐 排版规范（关键规则）

```css
/* 字体：跨平台 fallback */
font-family: 'Noto Sans CJK SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;

/* 创始人图与文字等高 */
.founder-row { align-items: stretch; }
.founder-row img { width: auto; max-height: 110px; object-fit: contain; }

/* 英文品牌词防止 justify 拉伸 */
.hl { white-space: nowrap; }
/* 含空格的英文品牌词用 &nbsp; 替代空格 */
GeForce&nbsp;RTX

/* 色彩层次 */
--brand: #2563EB;       /* 主色（按公司自定义） */
--brand-dark: #1D4ED8;  /* 表头深色 */
--brand-light: #DBEAFE; /* 标签/斑马线浅色 */
--neg: #DC2626;         /* 负值红色 */
```

---

## 🔗 数据源

| 企业类型 | 来源 | 获取方式 |
|----------|------|----------|
| **A股上市** | 巨潮资讯网 / 东方财富 / 同花顺 | `akshare.stock_financial_abstract_ths()` |
| **港股上市** | Yahoo Finance | `yfinance` |
| **美股上市** | SEC EDGAR / Yahoo Finance | `yfinance` / 10-K 直连 |
| **拟上市** | 上交所科创板招股书 | 搜狗搜索 / SSE 官网 |
| **非上市** | 官网 / 百度百科 / 搜狗搜索 | 手动搜集 |

---

## 📁 目录结构

```
enterprise-analysis.md/
├── README.md                      ← 本文件
├── SKILL.md                       ← Hermes Agent 主技能文件
├── CLAUDE.md                      ← Claude Code 兼容格式
├── scripts/
│   └── fetch_images.py            ← 图片自动抓取脚本
├── references/
│   ├── financial-indicator-template.md   ← 10项指标+3年数据+来源分级
│   ├── chinese-typography.md             ← 中文排版最佳实践
│   ├── page-balance-technique.md         ← 两页PDF均衡技巧
│   ├── spa-image-fallback.md             ← SPA网站图片回退
│   ├── 2page-layout-pattern.md          ← 两页版CSS模板
│   ├── company-registration-scraping.md   ← 工商注册信息抓取
│   ├── grayscale-jpeg-fix.md            ← 灰度JPEG修复
│   ├── image-fetching-pitfalls.md        ← 图片抓取避坑
│   └── ... (共14个参考文件)
└── examples/
    └── 拓维信息/        ← 完整示例（MD+PDF+DOCX+image）
    └── NVIDIA/          ← 美股示例
    └── 华为/            ← 已有示例
    └── ... 
```

---

## 🔧 安装到各 Agent

### Hermes Agent

```bash
# 方式一：直接加载
hermes skill view enterprise-analysis

# 方式二：克隆到本地 skills 目录
cd ~/.hermes/skills/
git clone git@github.com:Hermon803/enterprise-analysis.md.git mlops/enterprise-analysis
```

### Claude Code

```bash
# 项目根目录放置 CLAUDE.md
cp CLAUDE.md /path/to/project/
cd /path/to/project
claude "按规则分析 NVIDIA"
```

### 其他 Agent

直接读取 `SKILL.md` 中的规则定义，按工作流步骤执行即可。

---

## 📋 实战案例

| 公司 | 类型 | 数据源 | 输出 |
|------|------|--------|------|
| **[拓维信息](examples/拓维信息/)** | A股上市（002261.SZ） | 东方财富 + 同花顺 | ✅ 完整10项指标 |
| **[NVIDIA](examples/nvidia/)** | 美股（NVDA） | SEC 10-K | ✅ 完整财务数据 |
| **[腾讯](examples/腾讯/)** | 港股（0700.HK） | Yahoo Finance | ✅ 完整财务数据 |
| **[宇树科技](examples/宇树科技/)** | 科创板 IPO 中 | 招股说明书 | ⚠️ 部分未公开披露 |

---

## 📄 License

MIT

---

<p align="center">
  <sub>Made with ❤️ for AI产业链研究 · 欢迎 PR / Issue</sub>
</p>
