# 企业分析仓库与工作空间布局

## 仓库地址

- **远程仓库（GitHub）：** `git@github.com:Hermon803/enterprise-analysis.md.git`
- **本地工作空间（非 git 仓库）：** `~/Progress/analysis/v1.*/`
- **本地无永久 git clone** — 该仓库没有长期驻留的本地克隆

## 工作空间结构

```
~/Progress/analysis/
├── v1.1/                          ← 当前活跃版本
│   ├── 华为/
│   │   ├── image/                 ← 图片素材（logo/founder/product）
│   │   ├── 华为_企业分析.md       ← MD报告
│   │   └── ... (PDF/DOCX)
│   ├── 深圳格芯集成电路装备/
│   │   ├── image/
│   │   └── ...
│   └── skill-企业分析/
│       └── 企业分析.md           ← Skill源文件
└── v1.0/                          ← 旧版本（存档）
```

## 推送流程

Skill 仓库没有本地 clone，推送通过**临时克隆**完成：

```bash
cd /tmp
rm -rf ea
git clone --depth 1 git@github.com:Hermon803/enterprise-analysis.md.git ea
# 复制制品到仓库示例目录
cp ~/Progress/analysis/v1.1/华为/image/* ea/examples/华为/image/
cp ~/Progress/analysis/v1.1/华为/华为_企业分析.pdf ea/examples/华为/
# 提交并推送
cd ea
git add -A
git commit -m "描述性提交信息"
git push origin main
# 清理
rm -rf /tmp/ea
```

## 制品存放位置

| 制品类型 | 路径 |
|---------|------|
| MD 分析报告 | `~/Progress/analysis/v1.1/<公司名>/<公司名>_企业分析.md` |
| PDF 报告 | `~/Progress/analysis/v1.1/<公司名>/<公司名>_企业分析.pdf` |
| DOCX 报告 | `~/Progress/analysis/v1.1/<公司名>/<公司名>_企业分析.docx` |
| 图片素材 | `~/Progress/analysis/v1.1/<公司名>/image/` |
| 已推送示例 | `ea/examples/<公司名>/`（GitHub 仓库示例目录） |
| Skill 文件 | `~/.hermes/skills/mlops/enterprise-analysis/SKILL.md` |

## 相关仓库（非企业分析）

注意区分本仓库与其他项目仓库：

| 仓库 | 远程 | 本地路径 |
|------|------|---------|
| 企业分析 skill | `git@github.com:Hermon803/enterprise-analysis.md.git` | ⚠️ 无本地 clone，临时推 |
| 任务管理系统 | `git@gitee.com:zhermon/task-management-system.git` | `/home/bary/task-management-system/` |
| Spring Demo | 无远程 | `/home/bary/spring-demo/` |

当用户问"本地仓库地址"时需先确认：是问 Skill 仓库（无本地 clone）还是任务管理仓库（有本地 clone）。
