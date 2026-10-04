# protein-sequence-similarity-search 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：MMseqs2 / BLAST 蛋白同源序列检索：基于氨基酸序列快速搜索同源匹配物并推断蛋白质生化功能。
- **所属领域**：`生物与生命科学`
- **关联标签**：`MMseqs2、BLAST、同源搜索`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **MMseqs2** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Prerequisites**
- **Goal**
- **Core Rules**
- **Search Method Selection**
- **Instructions**
- **Path A: MMseqs2 Search (Default)**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```
    uv run scripts/mmseqs2_search.py <SEQUENCE_OR_FILE> -o <generated-filename.md> -j <generated-filename.json>
    ```

```
    uv run scripts/mmseqs2_search.py <SEQUENCE_OR_FILE> -o <generated-filename.md> -j <generated-filename.json> --include-mgnify
    ```

```
    uv run scripts/uniprot_blast.py <SEQUENCE_OR_FILE> -o <generated-filename.md> -j <generated-filename.json>
    ```

## 📋 执行要点与最佳实践
- **Strict Validation**: For BLAST, only use database codes listed in the
- **No Hallucinations**: If a script throws an error or returns no hits,
- **Do Not Parse Output Files**: Do not parse the JSON, a3m, or any other raw
- **Always State the Method**: Every report must clearly state whether the
- **Notification**: If this skill is used, ensure this is mentioned in the
- **Default:**
- **With mgnify:**
- Consult the **Available BLAST Databases** table below.

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。