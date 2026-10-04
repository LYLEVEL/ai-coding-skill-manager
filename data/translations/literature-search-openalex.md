# literature-search-openalex 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：OpenAlex 全球学术知识图谱：跨学科检索学术论文、学者影响力（H指数）、科研机构与全球引用网络。
- **所属领域**：`学术检索`
- **关联标签**：`OpenAlex、学术图谱、引用统计`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **OpenAlex** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **OpenAlex Skill**
- **Prerequisites**
- **Core Rules**
- **Rate Limits**
- **CLI Reference**
- **Commands**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```
uv run scripts/openalex_cli.py [--api-key KEY] <command> [flags]
```

```bash
# Author's works (resolve → filter)
uv run scripts/openalex_cli.py resolve authors "Geoffrey Hinton"
uv run scripts/openalex_cli.py filter works \
  --filter "authorships.author.id:A5108093963" \
  --sort "cited_by_count:desc" --per-page 10 > papers.json
cat papers.json | jq '[.results[] | {id, title: .display_name, year: .publication_year, citations: .cited_by_count}]'

# DOI lookup
uv run scripts/openalex_cli.py get works "https://doi.org/10.1038/s41586-021-03819-2"

# Bulk DOI lookup (up to 100)
uv run scripts/openalex_cli.py filter works \
  --filter "doi:10.1234/a|10.1234/b|10.1234/c" --per-page 100 > results.json

# Institutional impact by year
uv run scripts/openalex_cli.py resolve institutions "MIT"
uv run scripts/openalex_cli.py filter works \
  --filter "authorships.institutions.id:I63966007" \
  --group-by "publication_year" > mit_by_year.json

# Random sample
uv run scripts/openalex_cli.py filter works \
  --filter "publication_year:2023,is_oa:true" \
  --sample 100 --seed 42 > results.json
```

## 📋 执行要点与最佳实践
- **With key:** ~10 req/s, $1/day free budget.
- **Without key:** Very limited, $0.01/day budget.
- `--search <query>`: Full-text search (10× cost of `--filter`)
- `--filter <expr>`: Filter expressions. Use `,` for AND and `|` for OR.
- `--sort <field:dir>`: Sort results (e.g., `cited_by_count:desc`)
- `--select <fields>`: Limit the fields returned in the output.
- `--group-by <field>`: Aggregate results by a specific field.
- `--per-page <N>`: Number of results per page (default 25, max 100).

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。