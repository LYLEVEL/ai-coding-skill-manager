# string-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：STRING 蛋白质相互作用网络库 (PPI)：检索已知与预测的蛋白质互作关联、网络置信度评分与功能富集。
- **所属领域**：`生物与生命科学`
- **关联标签**：`STRING、PPI互作、互作网络`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **STRING** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **STRING Database Skill**
- **Prerequisites**
- **Core Rules**
- **Tool Execution**
- **Feature Domains (Progressive Disclosure)**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/string_cli.py <command> [options] --output /tmp/out.tsv
```

## 📋 执行要点与最佳实践
- **[Mapping Identifiers](references/mapping.md)** - Map common protein names
- **[Interactions & Network](references/interactions.md)** - Find interacting
- **[Enrichment & Functional Annotations](references/enrichment.md)** -
- **[Values/Ranks Enrichment](references/valuesranks.md)** - Submit full

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。