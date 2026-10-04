# pdb-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：RCSB PDB 实验生物大分子结构库：检索冷冻电镜/X射线测定的高分辨率蛋白质、核酸与配体 3D 实验结构。
- **所属领域**：`生物与生命科学`
- **关联标签**：`PDB、晶体结构、大分子结构`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **PDB** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **RCSB Protein Data Bank skill**
- **Prerequisites**
- **Core Rules**
- **Attribute-based search workflow**
- **For step 2: some basic PDB concepts (helpful for attribute choice)**
- **For step 3: Example queries**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Non-human proteins published in Nature, newest first
uv run scripts/search_pdb.py --query '{ "type": "group", "logical_operator": "and", "nodes": [ { "type": "terminal", "service": "text", "parameters": { "operator": "exact_match", "negation": true, "value": "Homo sapiens", "attribute": "rcsb_entity_source_organism.taxonomy_lineage.name" } }, { "type": "terminal", "service": "text", "parameters": { "operator": "exact_match", "value": "Nature", "attribute": "rcsb_primary_citation.rcsb_journal_abbrev" } } ] }' --return_type entry --sort_by rcsb_accession_info.initial_release_date --sort_direction desc --page_start 0 --rows 100 --output results.json
```

```bash
# Structures containing the chemical component CA (Ca2+ ion)
uv run scripts/search_pdb.py --query '{ "type": "terminal", "service": "text_chem", "parameters": { "operator": "exact_match", "value": "CA", "attribute": "rcsb_chem_comp_container_identifiers.comp_id" } }' --return_type entry --output results.json
```

```bash
# Number of entries with disulfide bonds
uv run scripts/search_pdb.py --query '{ "type": "terminal", "service": "text", "parameters": { "operator": "exact_match", "value": "disulfide bridge", "attribute": "rcsb_polymer_struct_conn.connect_type" } }' --return_type entry --count-only --output count.json
```

## 📋 执行要点与最佳实践
- **Always prefer to use the provided scripts**. Only as a last resort use
- **Always redirect output to a file**. Parse output with e.g. `jq`, `grep`,
- **Notification**: If this skill is used, ensure this is mentioned in the
- **Explain your queries** On completing a task that used PDB JSON/GraphQL
- **Entity**: A unique molecule found in a structure.
- **Instance / Chain**: A particular copy of an entity. E.g. if a structure
- **Assembly**: A biologically relevant collection of instances / chains. This
- **Label vs Auth**: Polymer instances get letter labels ("A", "B", "AA") and

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。