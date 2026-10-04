# unibind-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：UniBind 实验转录因子结合位点库：提供经过直接实验验证的直接 TF-DNA 结合位点坐标与 BED/FASTA 数据下载。
- **所属领域**：`生物与生命科学`
- **关联标签**：`UniBind、结合位点、ChIP验证`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **UniBind** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **UniBind Database Skill**
- **Prerequisites**
- **Quick Start**
- **Core Rules**
- **Utility Scripts**
- **1. List Species**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run <SKILL DIR>/scripts/unibind_api.py list_species
```

```bash
uv run <SKILL DIR>/scripts/unibind_api.py list_species
```

```bash
uv run <SKILL DIR>/scripts/unibind_api.py list_collections
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Output**: Query commands print JSON to stdout. Most responses are compact
- **Large Results**: `list_cell_lines` and `list_tfs` produce large output.
- **Saving to File**: Use `--output <path>` when you need to reference the
- **Pagination**: Use `--page` and `--page-size` (max 1000) to chunk large
- **Ordering**: Use `--order field_name` (prefix with `-` for descending) on
- **Notification**: If this skill is used, ensure this is mentioned in the
- `--species` (e.g., "Homo sapiens")

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。