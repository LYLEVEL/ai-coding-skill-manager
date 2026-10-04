# jaspar-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：JASPAR 转录因子结合基序库：获取转录因子的位置频率矩阵（PFM）与权重矩阵（PWM），用于结合位点预测。
- **所属领域**：`生物与生命科学`
- **关联标签**：`JASPAR、转录因子、Motif基序`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **JASPAR** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **JASPAR Skill**
- **Prerequisites**
- **Core Rules**
- **Utility Scripts**
- **1. Resolve TF to Matrix ID**
- **2. Get TF Motif (PFM)**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/jaspar_api.py resolve_tf_id --name "JUN" --tax-id 9606
```

```bash
uv run scripts/jaspar_api.py get_tf_motif --matrix-id "MA0488.2"
uv run scripts/jaspar_api.py get_tf_motif --matrix-id "MA0488.2" --format meme
```

```bash
uv run scripts/jaspar_api.py get_tf_metadata --matrix-id "MA0488.2"
uv run scripts/jaspar_api.py get_tf_metadata --matrix-id "MA0488.2" --format yaml
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Maximum API Window Size**: The genomic window for a single API query MUST
- **Valid Matrix IDs**: `get_tf_motif`, `get_tf_metadata`, and `get_tf_pwm`
- **Taxonomy Required**: Resolving IDs requires a `tax_id` to ensure targeted
- **Notification**: If this skill is used, ensure this is mentioned in the
- **DON'T** pass gene symbols (e.g., `JUN`) to `get_tf_motif`. You must pass
- **DON'T** forget the `--tax-id` when resolving a TF name.
- **DON'T** use this skill for determining tissue-specific epigenetic

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。