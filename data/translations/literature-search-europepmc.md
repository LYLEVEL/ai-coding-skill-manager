# literature-search-europepmc 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：Europe PMC 欧洲医学文献库检索：检索生命科学文献、获取开放获取（OA）全文 XML/文本并分析引用链。
- **所属领域**：`学术检索`
- **关联标签**：`EuropePMC、医学文献、开放获取`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **EuropePMC** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Europe PMC Database**
- **Prerequisites**
- **Core Rules**
- **Utility Scripts**
- **1. Search (`search`)**
- **Look up a paper by DOI**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Look up a paper by DOI
uv run scripts/europepmc_api.py search "DOI:10.1038/s41586-021-03819-2" --output result.json

# Keyword search
uv run scripts/europepmc_api.py search "CRISPR cancer" --max_results 5 --output results.json

# Author search
uv run scripts/europepmc_api.py search "AUTH:Jumper J" --max_results 10 --output results.json

# PMID lookup
uv run scripts/europepmc_api.py search "EXT_ID:34265844 AND SRC:MED" --output result.json

# Sorted by citations
uv run scripts/europepmc_api.py search "machine learning" \
  --sort "CITED desc" --max_results 20 --output results.json
```

```bash
uv run scripts/europepmc_api.py download_pdf PMC8371605 --output alphafold.pdf
```

```bash
# Get plain text (default)
uv run scripts/europepmc_api.py get_fulltext PMC8371605 --output fulltext.txt

# Get raw XML
uv run scripts/europepmc_api.py get_fulltext PMC8371605 --format xml --output fulltext.xml
```

## 📋 执行要点与最佳实践
- **Open Access Only**: This skill exclusively searches open-access content.
- **NEVER run python3 or python3 -c directly**: the system Python does not
- **Use the Wrapper**: ALWAYS use the provided script rather than calling the
- **Output Files**: All subcommands require `--output` to write results to a
- **List Sources.** If this skill is used, ensure this is mentioned in the
- `query` (str, required) — search query using Europe PMC syntax
- `--output` (str, required) — output JSON file path
- `--max_results` (int, default 10) — maximum results per page (max 1000)

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。