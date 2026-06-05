# 企业分析 · AI产业链企业六维安全分析

跨工具的 AI 产业链企业分析 skill/规则包。

## 适用工具

| 工具 | 使用方式 |
|------|---------|
| **Hermes Agent** | `skill_view(name='enterprise-analysis')` 或把 `skill-企业分析/SKILL.md` 放入 `~/.hermes/skills/` |
| **Claude Code** | 项目根目录放 `CLAUDE.md`，或 `claude --patch -p "按 CLAUDE.md 规则分析华为"` |
| **Workbuddy** | 导入 `workbuddy/企业分析.md` 到 workbuddy rules 目录 |
| **其他 Agent** | 直接读 `CLAUDE.md` 或 `skill-企业分析/SKILL.md` |

## 六维框架

1. 企业介绍与主营业务
2. 核心人物
3. 技术与知识产权
4. 经济贡献与经营数据
5. 供应链与区域布局
6. 竞争与市场结构

## 输出

每个分析产出 `.md` + `.pdf`（含图≤2页）+ `.docx` 三种文件。

## 示例

见 `examples/华为/` 目录。

## 安装

```bash
# Hermes
cd ~/.hermes/skills/ && git clone <repo-url> enterprise-analysis

# Claude Code
cp CLAUDE.md /your/project/CLAUDE.md
```

## License

MIT
