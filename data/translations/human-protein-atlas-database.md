# human-protein-atlas-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：人类蛋白质图谱 (HPA)：查询人体正常组织与肿瘤中蛋白质的半定量表达及细胞内亚显微定位（免疫荧光）。
- **所属领域**：`生物与生命科学`
- **关联标签**：`HPA、组织表达、亚细胞定位`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **HPA** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Human Protein Atlas (HPA) Database Integration**
- **Prerequisites**
- **When to Use**
- **Command Selection Guide**
- **Quick Start**
- **Map the ERBB2 gene symbol to its Ensembl ID**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Map the ERBB2 gene symbol to its Ensembl ID
uv run scripts/hpa_cli.py resolve-ensembl-id ERBB2 --output /tmp/erbb2_id.json

# Get subcellular location by Ensembl ID
uv run scripts/hpa_cli.py get-subcellular-location ENSG00000141736 --output /tmp/erbb2_location.json
```

```bash
uv run scripts/hpa_cli.py resolve-ensembl-id TP53 --output /tmp/tp53_id.json
```

```bash
uv run scripts/hpa_cli.py get-tissue-expression ENSG00000130234 \
  --tissues "duodenum,thyroid gland" --output /tmp/tissue_expr.json
```

## 📋 执行要点与最佳实践
- Map a gene symbol to its Ensembl ID for HPA queries.
- Retrieve the semi-quantitative protein abundance in normal human tissues and
- Find the specific organelles or subcellular structures where a protein has
- Check the consistency/agreement between RNA-seq consensus and protein
- Search for genes based on specific protein expression criteria (e.g.,
- Query eQTLs, pQTLs, or any variant-level associations. HPA provides
- Query gene expression in non-human species. HPA is strictly for human
- Retrieve purely quantitative RNA expression without interest in the protein

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。