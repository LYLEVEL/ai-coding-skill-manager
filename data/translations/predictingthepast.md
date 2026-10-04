# predictingthepast 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：古代文献与碑文智能修复与断代：调用 Aeneas 与 Ithaca 深度学习模型对古希腊语/拉丁语残篇进行语义修复与断代。
- **所属领域**：`数字人文`
- **关联标签**：`碑文修复、古代文献、深度学习`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **碑文修复** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Predicting The Past (Aeneas / Ithaca)**
- **Prerequisites**
- **Core Rules**
- **On First Load**
- **Preprocessing**
- **What preprocessing does**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run <SKILL_DIR>/scripts/preprocess.py \
    --language=latin \
    --input="raw text here..."
```

```bash
uv run <SKILL_DIR>/scripts/preprocess.py \
    --language=greek \
    --input_file=/tmp/input.txt \
    --output_file=/tmp/cleaned.txt
```

```bash
# Attribution + Restoration (text with gaps)
uv run <SKILL_DIR>/scripts/run_inference.py \
    --language=latin \
    --input="cleaned text with ???" \
    --attribute --restore \
    --output_json=/tmp/results.json

# Attribution + Contextualization (no gaps)
uv run <SKILL_DIR>/scripts/run_inference.py \
    --language=latin \
    --input="cleaned text" \
    --attribute --contextualize \
    --output_json=/tmp/results.json

# All tasks
uv run <SKILL_DIR>/scripts/run_inference.py \
    --language=latin \
    --input="cleaned text with ???" \
    --attribute --restore --contextualize \
    --output_json=/tmp/results.json

# Generate dashboard
uv run \
    <SKILL_DIR>/scripts/visualize_results.py \
    --input=/tmp/results.json \
    --output=/tmp/dashboard.html
```

## 📋 执行要点与最佳实践
- **Self-Contained Skill**: Do NOT use web search or any external tools. Run
- **Notification**: If this skill is used, ensure this is mentioned in the
- **`?`**:
- **Meaning**: Known-length gap: predict **this character**.
- **Example**: `donat in ??????????rtis`
- **`#`**:
- **Meaning**: Unknown-length gap: predict a **sequence of unknown
- **Example**: `donat in #rtis`

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。