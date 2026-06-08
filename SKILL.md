---
name: enterprise-analysis
description: AI产业链企业六维分析（企业介绍/核心人物/技术知识产权/经济数据/供应链/竞争格局）。输出MD+PDF+DOCX三种格式，含图片嵌入。
---

# 企业分析 · AI产业链企业六维分析

## 约束规则（必须遵守）

1. **维度锁定**：最终报告有且仅有以下六个维度，不得增减、合并或扩展：
   ① 企业介绍与主营业务 / ② 核心人物 / ③ 技术与知识产权 / ④ 经济贡献与经营数据 / ⑤ 供应链与区域布局 / ⑥ 竞争与市场结构

2. **制品固定**：每个分析必须生成且仅生成三种文件：
   - `[公司名]_企业分析.md` — Markdown 报告
   - `[公司名]_企业分析.pdf` — PDF 报告（含图）
   - `[公司名]_企业分析.docx` — Word 报告

3. **数据溯源**：每项数据必须标注来源，禁止编造，多源交叉验证。

4. **篇幅限制**：PDF最终产物不超过两页A4。所有内容（含图片）必须压缩在2页内，经济数据表固定10项指标（见下文模板），不限制具体行数但需控制列宽和字号（≤9pt）。
5. **相关产品展示**：报告底部（数据源上方）增设"相关产品"视觉展示区，展示**至少4个不同领域**的产品图片，每个领域选最具代表性的1个，并排展示。这是视觉/版面元素，不属于分析维度，不违反第1条的维度锁定。纯互联网公司无实体产品时，展示代表性App图标（使用simpleicons或官网下载），同样≥4个。
6. **模板性质**：下方报告模板为内容指引，PDF实际排版需按两页限制做密度优化，并非逐字逐段输出。
7. **语言**：若用户用中文提问，全部输出为中文（包括报告内容、表格头、来源标注）。

## 用法

```
企业分析 <公司名> <官网域名> <英文名>
```

**示例：**
```
企业分析 百度 baidu.com baidu
企业分析 NVIDIA nvidia.com nvidia
企业分析 比亚迪 byd.com
企业分析 华为 huawei.com huawei
企业分析 深圳格芯集成电路装备 grandtec-ic.com
```

## 工作流

### Step 0 — 优先检查本地工作空间

在任何网络搜索前，先检查用户工作空间中是否有该公司的已有分析文件。用户可能在 `~/Progress/analysis/v1.*/` 下维护了结构化的企业分析目录（如 `格芯集成电路_产业安全分析.md`），六维数据已存在，直接复用远比重新搜集高效。

找到已有文件后，extract其中的核心人物/经营数据/技术专利等信息并交叉验证时效性即可。如果在本地找不到现成分析，再进入 Step 1。

### Step 1 — 数据搜集

使用 `delegate_task` 并行搜集以下三类数据（并发3个子任务）：

| 任务 | 内容 |
|------|------|
| **经营数据** | **最近3年**（本年/上一年/前年）的10项固定指标：营业总收入、营收同比增速、毛利率、归母净利润、净利率、经营活动现金流净额、研发投入、研发占营收比、员工总数、总资产。标注数据来源。详见 `references/financial-indicator-template.md` |
| **核心人物** | 创始人/CEO、当前管理层、轮值制度（如有）。报告时只用创始人/董事长作为代表性人物，无需列出全部管理层 |
| **技术专利** | 累计专利数、PCT申请、标准必要专利份额、国标/行标参与 |

要求每个子任务输出结构化摘要，包含数据来源。

**数据来源分级（按优先级）**：

| 企业类型 | 营收/利润/现金流/资产/毛利率 | 研发投入 | 员工 | 来源工具 |
|----------|---------------------------|---------|------|---------|
| **A股上市** | ✅ 年报（巨潮/东方财富/同花顺） | ✅ 年报可查 | ✅ 年报可查 | `akshare.stock_financial_abstract_ths()` |
| **非上市大企业** | 官网/新闻稿/搜狗搜索 | 部分可查 | ✅ | 官网+百度百科+搜狗 |
| **中小企业** | 搜狗注册信息（仅营收估算） | ❌ | ✅ 官网 | 标注"未公开披露" |

**注册信息前置采集**：在执行以上子任务之前，先用 curl 获取该公司的基本工商注册信息（注册资本、成立日期、法定代表人、企业类型），作为报告的 baseline 数据。详见 `references/company-registration-scraping.md` — 当企查查/天眼查不可达时，用官网 + 搜狗搜索组合拳获取这些字段。

### Step 2 — 撰写六维报告（自然语句风格）

以连贯的自然语句撰写，避免标签+符号分隔的简历式格式。**禁止使用 `·` 间隔符做字段分隔**，应将信息整合为完整通顺的介绍语句。

参考风格（每个维度一段话，而非列表）：

```
## ① 企业介绍与主营业务

> [公司名]成立于[年份]，[上市/未上市]，总部位于[城市]，是国内领先的[定位]。公司主营业务为[一句话概括]，覆盖[领域A]、[领域B]、[领域C]等行业。

## ② 核心人物

> **[姓名]** · 创始人、董事长 · [籍贯] · [毕业院校] · [关键履历一句话]

## ③ 技术与知识产权

> 公司坚持[技术路线]，累计获得发明专利[X]项、软件著作权[X]项。参与制定国标[X]项，[年份]年研发投入[X]亿元（占营收[X]%），研发人员[X]人。

## ④ 经济贡献与经营数据（最近3年，固定10项指标）

| 指标 | 2023年 | 2024年 | 2025年 |
|------|--------|--------|--------|
| 营业总收入 | 填入 | 填入 | 填入 |
| 营收同比增速 | — | 自动计算 | 自动计算 |
| 毛利率 | 填入 | 填入 | 填入 |
| 归母净利润 | 填入 | 填入 | 填入 |
| 净利率 | 自动计算 | 自动计算 | 自动计算 |
| 经营活动现金流净额 | 填入 | 填入 | 填入 |
| 研发投入 | 填入 | 填入 | 填入 |
| 研发占营收比 | — | 自动计算 | 自动计算 |
| 员工总数 | 填入 | 填入 | 填入 |
| 总资产 | 填入 | 填入 | 填入 |

> 每个公司统一使用相同指标模板。非上市企业不可获取的字段标注"未公开披露"。计算项（营收同比增速/净利率/研发占营收比）在表格中填入计算结果。

## ⑤ 供应链与区域布局

> 公司核心芯片/技术来自[供应商]，[国产化程度]。总部位于[城市]，研发中心分布于[多个城市]，生产基地位于[多个城市]。旗下子公司包括...

## ⑥ 竞争与市场结构

> [公司名]在[行业]领域属于[规模级别]企业（营收约[X]亿元），主要竞争者包括...。公司差异化优势在于...。需关注的风险包括...
```

> ⚠️ **两页版说明**：以上模板为内容指引。PDF实际排版需做压缩——blockquote 内用自然语句而非 `·` 分隔，**禁止使用 `·` 间隔符做字段分隔**（如 `**定位**：软件服务商 · A股上市 · 长沙`），应将信息整合为完整通顺的介绍语句（如"公司总部位于长沙，成立于1996年，在深交所A股上市"）。表格字号≤9pt，边距1.3-1.5cm。
```

### Step 3 — 图片搜集（强制执行，无图不交付）

**图片是报告的必需组成部分，严禁跳过。** 三张图缺一不可。

首选用配套脚本全自动抓取：

```bash
python3 scripts/fetch_images.py \
  --company "$公司名" \
  --domain "$域名" \
  --english "$英文名" \
  --founder "$创始人名" \
  --output ./image/
```

脚本自动执行以下流程，依次尝试各来源，**找到即停**：
- **Logo**: simpleicons.org → 官网HTML解析(icon/og:image/logo图) → 常见路径
- **创始人**: 百度百科 → 官网关于我们页面(排除产品和logo类图片)
- **产品图**: 官网产品页(支持懒加载 data-src) → 产品详情子页面

**脚本特性：**
- 自动去重：产品图不会与已下载的logo/创始人图重复
- 图片有效性校验（PIL verify，不只是看HTTP status）
- 跳过返回HTML的无效响应
- User-Agent轮换防拦截

全部失败才标注"图片待补充"。同时输出图片需求清单供跟踪：

```yaml
图片需求:
  - id: logo      描述: "公司Logo"        来源: "simpleicons/官网"   状态: 待抓取
  - id: founder   描述: "创始人照片"        来源: "百度百科/官网"      状态: 待抓取
  - id: product   描述: "核心产品图"        来源: "官网产品页"         状态: 待抓取
```

#### Logo 抓取（按优先级依次尝试，找到即停）

| 优先级 | 方法 | 说明 |
|--------|------|------|
| ① | `curl -sL https://cdn.simpleicons.org/<英文名>` | SimpleIcons CDN（Cloudflare），国内可达，覆盖~80%科技公司 |
| ② | WebSearch 中文搜索 + curl | 搜"公司名 logo 百度百科"，从中文网页提取图片直链下载 |
| ③ | curl 官网 `grep -iE 'icon\|favicon\|og:image'` | 从官网HTML提取favicon或og:image URL → curl下载 |
| ④ | WebSearch 英文兜底 + curl | `公司英文名 press kit logo` → curl下载 |

```bash
# 下载后必须检查是否为有效图片
curl -sL <图片URL> -o /tmp/logo_check
file /tmp/logo_check   # 应输出 "PNG/JPEG/SVG image data"
# 如输出 "HTML document" → 非图片，跳过
```

#### 创始人/CEO照片抓取

**最高优先级：百度百科**（使用 curl 绕过 requests 的 Baidu 403 拦截）。`fetch_images.py` 自动执行，手动备选：

| 优先级 | 方法 | 说明 |
|--------|------|------|
| ① | 百度百科（curl直连，绕过requests的UA检测） | `curl -sL "https://baike.baidu.com/item/人物名?fromModule=lemma_search-box" -H "Cookie: BAIDUID=..."` 提取 `bkimg.cdn.bcebos.com` 图片URL |
| ② | 官网关于我们/团队页面 | 过滤logo/icon/product类图片，优先含 people/team/headshot 关键词的URL |
| ③ | WebSearch 英文兜底 | `founder name photo official` |

#### 产品图抓取

**优先搜索国内中文站点**，按优先级依次尝试：

| 优先级 | 方法 | 说明 |
|--------|------|------|
| ① | WebSearch 中文搜索 + curl | 搜"公司名 产品 评测"，从汽车之家/中关村在线/太平洋科技/IT之家等国内媒体找图 |
| ② | curl 官网产品页 `grep -i img` | 从官网产品页提取大图URL，优先含 `large`/`high`/`1920` 的链接 |
| ③ | WebSearch 通用英文兜底 | `company product official photo press` |

关键技巧：
- **中文搜索优先**：国内科技媒体（汽车之家、中关村在线、太平洋科技、IT之家等）图片走国内CDN加速，下载成功率高
- 对懒加载网站，检查 `data-src`、`data-original` 属性
- 图片URL优先选**大分辨率**（含 `large`、`high`、`1920` 等关键词）

#### 图片源可达性（实测）

**⚠️ 关键发现：WebFetch ≠ 真实网络。** WebFetch 工具有域名安全策略，会拒绝访问 nvidia.com 等知名站点。但 **curl/Bash 不受此限制**。图片抓取阶段应**全部用 Bash(curl) 下载**，WebFetch 仅用于分析HTML文本。

**国内可达源 ✅（优先使用）**

| 来源 | 说明 |
|------|------|
| `cdn.simpleicons.org`（Cloudflare） | SimpleIcons，知名公司Logo首选，curl直达 |
| 百度系（baidu.com / baike.baidu.com） | 中文搜索Logo/产品图首选 |
| 国内科技媒体（汽车之家/中关村在线/太平洋/IT之家等） | 含大量产品实拍图，国内CDN加速 |
| 公司官网（通过 Bash curl） | 官网路径需摸索但连接可达 |

**国内不可达源 ❌**

| 来源 | 原因 |
|------|------|
| `upload.wikimedia.org` / Wikipedia | 网络层阻断（TLS握手超时） |
| Google系（含 `s2/favicons`） | 网络层阻断 |
| `logo.clearbit.com` | DNS无法解析 |
| `raw.githubusercontent.com` | HTTP 403 |
| 境外官网CDN（如 `images.nvidia.com`） | 连接可达但具体路径需摸索 |

#### 实操策略速查

```
Logo 抓取:
  ① curl cdn.simpleicons.org/{英文名}
  ② WebSearch 中文"公司名 logo" → 百度百科 → curl图片URL
  ③ curl 官网 | grep -iE 'icon|favicon|og:image' → 提取URL → curl下载

产品图抓取:
  ① WebSearch 中文"公司名 产品 评测" → 国内科技媒体 → curl图片URL
  ② curl 官网产品页 | grep -iE 'img.*jpg|img.*png' → 提取URL → curl下载

兜底: 全部失败则纯文字输出，标注 [图片待补充]
```

嵌入报告时使用 `[图片:类型:描述]` 占位标记：
- `[图片:logo:xxx]` → h1同一行右上角，height=28px，右浮动（不单独占行），两页版必用此模式
- `[图片:founder:xxx]` → "核心人物"板块右侧，矩形（非圆形），width≤90px，圆角2px，带品牌色边框，flex-direction: row-reverse 排到右侧
- `[图片:product:xxx]` → 用于"相关产品"展示区（PDF底部），至少4个不同领域产品图标并排，width≤100px；纯互联网公司用App图标统一展示
- `[图片:app:xxx]` → 互联网公司App图标，width≤60px，与产品图同样式统一展示

### Step 4 — 生成HTML并转PDF

创建自包含HTML文件（所有图片base64嵌入），用 weasyprint 转PDF。

PDF底部必须包含 **相关产品展示区**（至少4个不同领域产品并排），CSS模板见 `references/product-showcase-template.md`。

关键坑：`<img>` 的 `src` 属性必须用**单引号** `src='data:...'`，不能用双引号。详见陷阱6。

### Step 5 — 生成DOCX

`pandoc [公司名]_企业分析.md -o [公司名]_企业分析.docx`

## PDF排版要求

- A4纸张 · 边距 **1.5cm**（不低于1.3）· 中文使用 Noto Sans CJK SC
- h1公司名与logo flex同行（h1左 logo右），h1字号**22pt**品牌色，带2px字间距
- h2板块标题字号**12pt**，加1px字间距，上间距0.7em
- blockquote（正文容器）字号9.5pt，行高**1.85**，内边距**0.5em 0.9em**，文字不贴边，使用 `text-align: justify` 实现中文两端对齐
- 表格字号9pt，区分"数据"与"说明"两列（避免纯百分比），行高保持1.7以上
- 关键数据用 `.hl { color: brand; font-weight: bold; }` 高亮
- 去掉所有`---`分隔线，板块间用**0.7em**上下间距自然分隔
- **相关产品展示区**（底部，数据源上方）：标题"相关产品"12pt，产品图至少4个并排（不同领域），width≤100px，间距0.8em。纯互联网公司用App图标（width≤60px）。
- 创始人图片矩形（非圆形），width≤90px，flex-direction: row-reverse 排到"核心人物"板块右侧
- 数据源区块置底，字号7.5pt，浅灰色，上边线分隔

使用 `:root { --brand-color: 华为#cf0a2c / 百度#2932e1 / NVIDIA#76b900; }` CSS自定义属性统一品牌色

## 参考文件

- `references/huawei-analysis-workflow.md` — 华为分析实战记录（数据源、CDN拦截、输出结构）
- `references/2page-layout-pattern.md` — 两页版HTML/CSS排版模板与技巧（包括h1+logo并排、base64引号陷阱、品牌色表、产品展示区）
- `references/private-company-analysis.md` — 非上市/中小企业六维分析指南（数据缺失处理、官网图片抓取、实战案例）
- `references/company-registration-scraping.md` — 中国公司注册信息抓取实战
- `references/workspace-fallback-pattern.md` — 网络不可达时的工作区回退模式
- `references/executive-research-guide.md` — 企业高管背景研究方法
- `references/image-fetching-pitfalls.md` — 图片抓取防坑记录（百度百科403curl应对、JS渲染页面替代源、去重策略）
- `references/grayscale-jpeg-fix.md` — 灰度JPEG(mode L)导致weasyprint渲染失败的原因与修复
- `references/workspace-git-workflow.md` — 企业分析仓库布局、工作空间结构、推送流程与相关仓库区分
- `references/financial-indicator-template.md` — 固定10项财务指标模板 + 3年数据规范 + 数据来源分级
- `references/page-balance-technique.md` — 两页PDF排版失衡时（"版块以较少内容单独成页"）的反向调优技巧
- `references/chinese-typography.md` — 中文排版CSS最佳实践（字号层级、两端对齐、自然语句风格、两页均衡策略）

## 陷阱与注意事项

1. **Web搜索/联网不可达时的工作区回退**：当用户拒绝网络搜索或网络不可达时，不要停止工作。优先搜索用户工作目录（如 `~/Progress/analysis/`、当前cwd）下是否有该公司的既有分析文件。如存在，提取结构化数据并标注"数据来源：已有存档，需交叉验证"，然后尝试增量补缺。

2. **专利数据口径不一致处理**：不同来源可能报告不同的专利数字（如"累计139项发明及实用新型" vs "40余项发明专利"）。如果无法确定数字间的包含关系（40+项发明是否在139项总数内），在报告中明确标注两个数字的关系含糊，并优先使用可信来源（官方年报 > 百度百科 > 第三方咨询）。不要替用户做归并假设。

3. **技术知识产权板块不仅包含专利**：还应包含软著（软件著作权）、省市级研发平台（如"广东省集成电路封测设备工程技术研究中心"）、承担过的国家重大科技专项（如"02专项"）。这些是"知识产权"维度的重要组成部分。

4. **厂商CDN可能拦截curl**：部分企业官网（如华为 consumer-img.huawei.com）会拒绝无浏览器User-Agent的curl请求，返回HTML而非图片。应对策略：

5. **SPA网站（Nuxt.js/Vue/React）没有服务端渲染图片URL**：拓维信息 talkweb.com.cn 使用 Nuxt.js，所有产品页/首页内容由 JS 动态渲染。fetch_images.py 的 `requests` + HTML regex 抓取不到任何图片URL。实战胜率极低。应对策略：
   - **Logo → 直接 curl favicon.ico + PIL 转 PNG**：`curl -sL https://www.{domain}/favicon.ico -o /tmp/favicon.ico; python3 -c "from PIL import Image; Image.open('/tmp/favicon.ico').convert('RGB').save('image/logo.png')"`。SPA 站点通常至少配了 favicon。
   - **产品图 → 生成彩色占位图**：所有图片源均失败时，用 PIL 生成 200×140 的色块 + 品名文字标注作为产品图。避免纯文字输出"图片待补充"降低报告观感。示例代码见 `references/spa-image-fallback.md`。
   - 优先从第三方源（百度百科、科技媒体）获取产品图
   - 如官网CDN不可达，使用 `-H "User-Agent: Mozilla/5.0 ..."` 重试
   - 产品图兜底：logo本身作为产品占位图，或留白标注"图片待补充"
   - 不编造、不使用侵权图片

6. **境外图片源可能超时**：Wikimedia、GitHub等境外源可能不可达。优先使用国内CDN源（baidu.com、bcebos.com、jd.com等）。

7. **PDF嵌入图片**：weasyprint渲染使用 `data:image/...;base64,...` 格式嵌入，不可使用外部URL。
   **关键坑**：Python生成HTML时，`<img>`的`src`属性必须用**单引号** `src='data:...'`，不能用双引号 `src="data:..."`。
   weasyprint解析 `src=\\"..."`（Python escaping产生的转义）会报 `File name too long` 错误。
   ✅ 正确写法：`f"<img src='{b64data}'>"` ❌ 错误写法：`f'<img src="{b64data}">'`

8. **数据时效性**：优先从最新年报（公司官网/证监会网站）获取经营数据。PCT/SEP数据在WIPO/3GPP网站可查。

9. **并发搜集**：使用 delegate_task 并发3个子任务（经营数据、核心人物、技术专利），每个任务要求返回结构化带来源的数据。

10. **灰度JPEG导致weasyprint渲染失败**：PIL mode L（灰度，1通道）的JPEG图片在weasyprint base64内嵌时显示为空白或报参数错误。所有JPEG图片入HTML前必须检查模式：`if im.mode == 'L': im = im.convert('RGB')`。`fetch_images.py` 的 `download()` 已自动处理，手动添加的图片需注意。

10. **百度百科创始人照片体积过大**：百度百科下载的创始人照片原始分辨率可能很大（实测 4480×6720px，8+MB），直接 base64 嵌入导致PDF膨胀至8+MB。入HTML前必须压缩：
    ```python
    from PIL import Image
    img = Image.open('founder.png')
    img.thumbnail((400, 500), Image.LANCZOS)  # 缩小到合理尺寸
    if img.mode == 'RGBA': img = img.convert('RGB')
    img.save('founder_compressed.jpg', 'JPEG', quality=80, optimize=True)
    ```
    压缩后约 15-30KB，视觉差异极小。此步骤应在 base64 嵌入之前执行。

11. **两页PDF排版失衡**：当第二页仅包含产品展示区+数据源等少量内容时，不要直觉性地缩小字号试图"拉回"内容。应反向操作——增大的字号+行高+间距，让页1内容自然溢出到页2，同时单独放大页2各元素的视觉占位（blockquote字号+0.5pt、产品图面积翻倍等）。详细方法论见 `references/page-balance-technique.md`。

12. **核心人物板块独立布局**：用户明确要求核心人物板块不应与其他维度（如技术与知识产权）分栏并排。核心人物应单独一栏全宽展示，创始人照片在右侧（flex-direction: row-reverse）。若内容少只保留创始人一人即可，不需要列出所有管理层。

13. **中文排版偏好**：用户偏好自然语句叙述而非标签式列表。正文应使用 text-align: justify 两端对齐，line-height >= 1.8 保证中文可读性。blockquote 内用完整句子而非 **字段名**：值 · 值 · 值 格式。

14. **字体与字号层级**：h1=20-22pt 品牌色，h2=11pt 加下边线，正文=9-9.5pt，blockquote 正文同字号但行高略高。表格 >= 8.5pt 避免过小。产品图标签 >= 7pt。使用 :root { --brand: #2563EB; } 统一品牌色，body 文本色用 slate-800（#1e293b）而非纯黑。