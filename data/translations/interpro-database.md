# interpro-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：InterPro 蛋白质家族与功能结构域：整合 Pfam/CDD 等 14 个数据库，识别蛋白质结构域、保守位点与 GO 功能。
- **所属领域**：`生物与生命科学`
- **关联标签**：`InterPro、结构域、蛋白质家族`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **InterPro** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **InterPro Database Access**
- **Prerequisites**
- **Overview**
- **Core Rules**
- **fetch_interpro_data lazily yields results page-by-page**
- **4 Ways to Construct Endpoints:**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run ./scripts/interpro_client.py fetch protein --source_db reviewed --limit 2 --query_params tax_id=9606 --output exploratory_results.jsonl
```

```python
import sys
sys.path.append('scripts')
from interpro_client import fetch_interpro_data
import itertools

# fetch_interpro_data lazily yields results page-by-page
results = fetch_interpro_data(
    endpoint="entry",
    source_db="pfam",
    query_params={"page_size": 10}
)
for match in itertools.islice(results, 10):
    print(match["metadata"]["accession"])
```

```bash
uv run scripts/interpro_client.py fetch entry
  --query_params ida_search=PF00069,PF00017
  --flags ordered exact
  --output architectures.jsonl
```

## 📋 执行要点与最佳实践
- Identify what domains, families, and sites are found in a particular
- Identify all proteins that belong to a protein family or contain a
- Examine the species in which a particular protein family or domain is found.
- Annotate genomes with protein family information and Gene Ontology (GO)
- **Use the Wrapper**: ALWAYS execute the `scripts/interpro_client.py` helper
- **For exploratory queries**: ALWAYS use the CLI with a strict `--limit`.
- **Output to file**: Use the CLI with --output to output to a file rather
- **For more complex pipelines** import the module natively into your Python

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。