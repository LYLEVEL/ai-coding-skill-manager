# reactome-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：Reactome 生物学信号通路数据库：执行基因列表通路富集分析、信号转导级联网络检索并导出通路拓扑图。
- **所属领域**：`生物与生命科学`
- **关联标签**：`Reactome、通路富集、信号转导`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **Reactome** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Reactome Analysis & Content Service**
- **Prerequisites**
- **Overview**
- **When to Use This Skill**
- **Common Species IDs**
- **Common Pathway IDs**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/reactome_analysis.py <command> [options] --output /tmp/out.json
```

```bash
uv run scripts/reactome_analysis.py --help
```

```bash
uv run scripts/reactome_analysis.py db-version --output /tmp/version.json
uv run scripts/reactome_analysis.py db-name --output /tmp/name.json
```

## 📋 执行要点与最佳实践
- Performing pathway enrichment (overrepresentation) analysis on gene/protein
- Retrieving analysis results using a token from previous enrichment
- Identifying which genes or proteins were not found in a pathway analysis
- Analyzing gene expression data against pathway annotations
- Mapping identifiers to Reactome entities across species
- Retrieving reaction participants (inputs, outputs, catalysts, regulators)
- Navigating pathway hierarchy and listing top-level pathways
- Finding which complexes or sets contain a protein

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。