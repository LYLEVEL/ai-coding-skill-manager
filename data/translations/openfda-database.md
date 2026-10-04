# openfda-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：openFDA 药品与食品安全监管库：查询 FDA 药品不良反应报告、处方说明书、召回事件及医疗器械审批。
- **所属领域**：`生物与生命科学`
- **关联标签**：`openFDA、药物安全、不良反应`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **openFDA** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **openFDA Search and Query**
- **Prerequisites**
- **Core Rules**
- **Utility Script**
- **1. Search**
- **2. Count**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/openfda_query.py {search,count,download} --output <file> [options]
```

```bash
uv run scripts/openfda_query.py search \
  --category drug --endpoint event \
  --search "patient.drug.medicinalproduct:aspirin" \
  --limit 5 --output /tmp/fda_results.json
```

```json
{"status": "success", "output": "/tmp/fda_results.json", "results_in_file": 5, "total_matching": 601477}
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Rate Limiting**: Respect openFDA rate limits. Without API key: 240
- **Always Use `--output`**: All subcommands require `--output <file>` to
- **Notification**: If this skill is used, ensure this is mentioned in the
- `--output`: Output file for full JSON results (required).
- `--category`: API category — `drug`, `device`, `food`, `tobacco`, `other`,
- `--endpoint`: Endpoint within the category (e.g., `event`, `label`, `510k`).
- `--search`: Query string (e.g.,

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。