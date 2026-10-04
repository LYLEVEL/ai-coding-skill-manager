# embl-ebi-ols 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：EMBL-EBI 本体查找服务 (OLS)：跨 250+ 生物医学本体库（GO、DOID、HP）检索标准受控词汇与层级拓扑。
- **所属领域**：`生物与生命科学`
- **关联标签**：`生物本体、受控词汇、知识拓扑`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **生物本体** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **EMBL-EBI Ontology Lookup Service (OLS)**
- **Prerequisites**
- **Core Rules**
- **When to Use — Quick Recipes**
- **Utility Scripts**
- **Reference**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/search_ols.py --query "diabetes" \
  --rows 5 --output /tmp/ols_search_results.json 2>/dev/null
```

```bash
uv run scripts/suggest_ols.py --query "diabet" --rows 5 \
  --output /tmp/ols_suggest.json 2>/dev/null
```

```bash
uv run scripts/get_term.py --obo_id "GO:0005634" \
  --output /tmp/ols_term.json 2>/dev/null
```

## 📋 执行要点与最佳实践
- [!IMPORTANT] **Use the Utility Scripts**: You MUST ALWAYS use the provided
- **Rate Limiting & Resilience**: You MUST respect EBI's Terms of Use with a
- **Notification**: If this skill is used, ensure this is mentioned in the
- **Definition** of a disease, phenotype, or term → `get_term.py --obo_id <ID>
- **Subtypes** or **children** of a term → `get_term.py --obo_id <ID>
- **Parent** of a term → `get_term.py --obo_id <ID> --relations parents`
- **Ancestors** / disease **categories** / **classified under** → `get_term.py
- **Root terms** of an ontology → `get_term.py --ontology <id> --roots`

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。