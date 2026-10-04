# gtex-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：GTEx 人体组织表达与 eQTL 数据库：检索人体 54 个健康组织中的定量 RNA 表达水平与变异表达性状关联。
- **所属领域**：`生物与生命科学`
- **关联标签**：`GTEx、组织特异表达、eQTL分析`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **GTEx** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **GTEx Database Integration**
- **Prerequisites**
- **When to Use**
- **Core Rules**
- **Command Selection Guide**
- **Quick Start**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Map the TNF gene symbol to its GENCODE ID
uv run scripts/gtex_cli.py resolve-gencode-id TNF --output /tmp/tnf_id.json

# Get median expression of a gene by GENCODE ID
uv run scripts/gtex_cli.py get-median-expression ENSG00000232810.2 --output /tmp/tnf_expr.json
```

```bash
uv run scripts/gtex_cli.py resolve-gencode-id TNF --output /tmp/tnf_id.json
```

```bash
uv run scripts/gtex_cli.py get-median-expression ENSG00000232810.2 \
  --tissues "Whole Blood,Spleen" --output /tmp/expr.json
```

## 📋 执行要点与最佳实践
- Map a gene symbol to its Versioned GENCODE ID.
- Retrieve the baseline median expression level (in TPM) of a gene across
- Find the top tissues where a particular gene is most highly expressed.
- Fetch significant single-tissue eQTLs for a variant or within a chromosomal
- Get all significant eQTLs associated with a specific gene.
- Contextualise a variant within GWAS loci using eQTL data.
- Query for protein-level expression or post-translational modifications
- Query gene expression in diseased tissues (e.g., tumor samples, cirrhosis).

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。