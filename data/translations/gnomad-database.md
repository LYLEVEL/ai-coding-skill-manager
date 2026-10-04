# gnomad-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：gnomAD 人群突变频率与基因耐受性库：查询人类群体等位基因频率及功能缺失不耐受指标（pLI / LOEUF）。
- **所属领域**：`生物与生命科学`
- **关联标签**：`gnomAD、人群频率、基因耐受性`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **gnomAD** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **gnomAD Database**
- **Prerequisites**
- **Core Rules**
- **Utility Scripts**
- **By variant ID:**
- **By rsID (e.g., rs1800562):**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# By variant ID:
uv run scripts/get_variant_frequency.py --variant_id {variant_id} [--dataset {dataset}] --output variant_frequency.json

# By rsID (e.g., rs1800562):
uv run scripts/get_variant_frequency.py --rsid {rsid} [--dataset {dataset}] --output variant_frequency.json
```

```bash
uv run scripts/get_gene_constraint.py --gene {gene_symbol} --output {gene_symbol}_constraint.json
```

```bash
# By region:
uv run scripts/search_variants.py --chrom {chrom} --start {start} --end {end} --output region_variants.json
# By gene:
uv run scripts/search_variants.py --gene {gene_symbol} --consequence {pLoF|missense} --output {gene_symbol}_variants.json
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Notification**: If this skill is used, ensure this is mentioned in the

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。