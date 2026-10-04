# pubchem-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：PubChem 化学分子与生物活性库：根据 CID/SMILES/化学名检索化合物物化性质、化学结构与生物测试数据。
- **所属领域**：`生物与生命科学`
- **关联标签**：`PubChem、化合物、小分子结构`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **PubChem** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **PubChem Database**
- **Prerequisites**
- **Quick Start**
- **Core Rules**
- **Core Capabilities**
- **OR**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/pubchem_api.py resolve --name "aspirin" --output result.json
```

```bash
uv run scripts/pubchem_api.py resolve --name "ibuprofen" --output result.json
# OR
uv run scripts/pubchem_api.py resolve --inchi "InChI=1S/C3/c1-3-2/i1+1" --output result.json
```

```bash
uv run scripts/pubchem_api.py properties --cid 2244 --output result.json
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- Read the generated JSON output file, and process it with jq or code.
- **Verify Facts**: ALWAYS verify information retrieved from memory with a
- **Notification**: If this skill is used, ensure this is mentioned in the
- **Search for parent/neutral molecule**: If searching for an ion or salt, try
- **Deconstruct complex formulas**: If a complex formula returns no results,
- **Use substructure or similarity search**: If you have a SMILES string or
- **Custom/Complex Queries**: For more details, read

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。