# pubmed-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：PubMed 生物医学文献库：检索生物医学研究与临床试验论文，抓取摘要全文，并与基因/化合物数据库交叉互联。
- **所属领域**：`学术检索`
- **关联标签**：`PubMed、生物医学、临床文献`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **PubMed** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **PubMed API**
- **Prerequisites**
- **Core Rules**
- **Structure of the skill folder**
- **CLI Usage**
- **Example Usage**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/pubmed_api.py <output_file> <function_name> <required_args> [--flag value ...]
```

```bash
uv run scripts/pubmed_api.py ./search_results.json search_pubmed "BRCA1" --max_results 5
cat ./search_results.json | jq '.[]' -r
uv run scripts/pubmed_api.py ./abstracts.json fetch_article_abstracts "35113657"
cat ./abstracts.json | jq '.[0].title' -r
```

```bash
cat ./search_results.json | jq -r 'join(",")'
```

## 📋 执行要点与最佳实践
- **API Use**: Always use the provided wrapper `scripts/pubmed_api.py` which
- **JSON Processing**: Use `jq` to filter and transform JSON output (or python
- **Temporary Files**: To avoid polluting the working directory with JSON
- **Notification**: If this skill is used, ensure this is mentioned in the
- `SKILL.md` - This file
- `scripts/pubmed_api.py` - The skill CLI
- `references/` - Directory with detailed function specifications
- `advanced-linking.md`

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。