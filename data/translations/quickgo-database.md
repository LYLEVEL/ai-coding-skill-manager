# quickgo-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：QuickGO 基因本体论注释平台：将基因映射至生物学过程、分子功能与细胞组分，探索 GO 词条上下级图谱。
- **所属领域**：`生物与生命科学`
- **关联标签**：`QuickGO、GO分类、生物通路`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **QuickGO** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **QuickGO Database Skill**
- **Prerequisites**
- **Usage**
- **Core Rules**
- **Common Workflows**
- **1. Map a gene to its functions (Annotations)**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Step 1: Find the UniProtKB ID for human (9606) gene PROC
uv run scripts/quickgo_tool.py geneproduct search --query "PROC" --taxonId 9606 --limit 5 --output proc_id.json
# (Look at proc_id.json, observe the ID is e.g., UniProtKB:P04070)

# Step 2: Find experimental GO annotations for that ID
uv run scripts/quickgo_tool.py annotation search --geneProductId "UniProtKB:P04070" --taxonId 9606 --evidenceCode "ECO:0000269" --limit 50 --output proc_annotations.json
```

```bash
# Find human genes with this specific molecular function
uv run scripts/quickgo_tool.py annotation search --goId "GO:0003700" --taxonId 9606 --limit 50 --output tf_genes.json
```

```bash
# Fetch term details (definitions, synonyms)
uv run scripts/quickgo_tool.py go terms --ids "GO:0003150" --output term_details.json

# Check ancestry (e.g., is GO:0001917 a child of something?)
uv run scripts/quickgo_tool.py go terms --ids "GO:0001917" --relation ancestors --output term_ancestors.json
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Pagination & Limits**: Restrict endpoints to a maximum of 100 results per
- **Output Files**: Always use the `--output` flag to save responses to a file
- **Evidence Codes**: Prioritize experimental evidence (`ECO:0000269`) over
- **Taxon Filtering**: Use `--taxonId 9606` to restrict results to Human when
- **Notification**: If this skill is used, ensure this is mentioned in the

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。