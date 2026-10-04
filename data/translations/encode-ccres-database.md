# encode-ccres-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：ENCODE 顺式调控元件库 (cCREs)：查询人类各细胞类型的候选启动子、增强子及 ChIP-seq 组蛋白修饰峰图。
- **所属领域**：`生物与生命科学`
- **关联标签**：`ENCODE、增强子、顺式调控`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **ENCODE** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **ENCODE Database Skill**
- **Prerequisites**
- **Core Rules**
- **Quick Start**
- **Search cCREs by coordinates**
- **Get details for a specific cCRE**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Search cCREs by coordinates
uv run scripts/screen_api.py search --chromosome chr11 \
  --start 5205263 --end 5207263 \
  --output /tmp/search.json

# Get details for a specific cCRE
uv run scripts/screen_api.py details EH38E2941922 \
  --output /tmp/details.json
```

```bash
uv run scripts/screen_api.py biosamples --output /tmp/biosamples.json
# Use jq to filter for Type A biosamples
jq '.data.ccREBiosampleQuery.biosamples[] | select(.is_type_a == true) | .displayname' /tmp/biosamples.json
```

```bash
    uv run scripts/screen_api.py search \
        --chromosome chr11 --start 5205263 --end 5207263 \
        --output /tmp/search.json
    ```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Parsing Output**: Do NOT use `cat` to read the entire JSON output file
- **Notification**: If this skill is used, ensure this is mentioned in the
- `search`: Search cCREs by coordinates, accessions, or epigenetic signals.
- `nearby-genes`: Find nearby genes for given cCRE accessions.
- `details`: Get detailed information and biosample-specific max Z-scores for
- `biosamples`: Get biosample metadata for an assembly.
- `orthologs`: Get orthologous cCREs in another assembly.

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。