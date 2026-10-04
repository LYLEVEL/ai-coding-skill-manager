# literature-search-biorxiv 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：bioRxiv / medRxiv 生物医学预印本搜索：按学科分类与时间段精准筛选生命科学与医学前沿预印本论文。
- **所属领域**：`学术检索`
- **关联标签**：`bioRxiv、医学预印本、文献下载`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **bioRxiv** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **bioRxiv and medRxiv Literature Search**
- **Prerequisites**
- **Search Strategy Guide (Read First)**
- **Core Rules**
- **Utility Scripts**
- **1. Search by Dates (`search_by_dates.py`)**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Broad category search over a 2-week period
uv run scripts/search_by_dates.py --server biorxiv \
  --start_date 2024-01-01 --end_date 2024-01-14 \
  --category neuroscience > results.json

# Deep keyword filtering using OR logic and including abstracts
uv run scripts/search_by_dates.py --server medrxiv \
  --start_date 2023-11-01 --end_date 2023-11-30 \
  --category infectious_diseases \
  --keywords "covid" "sars-cov-2" --match_logic OR \
  --include_abstracts > covid_papers.json

# Finding papers by a specific author in a narrow window
uv run scripts/search_by_dates.py \
  --start_date 2024-05-01 --end_date 2024-05-14 \
  --author "Smith" > smith_papers.json
```

```bash
uv run scripts/search_by_doi.py --server biorxiv \
  --doi "10.1101/2023.08.15.551388" \
  --include_abstracts > paper_info.json
```

## 📋 执行要点与最佳实践
- **A DOI** (e.g., from a citation): Use `search_by_doi.py`. Fast and
- **Approximate date + category**: Use `search_by_dates.py` with a 1–4 week
- **Only a topic or keywords, no date**: **Do NOT use this skill for
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Local Filtering (CRITICAL WARNING)**: Unlike arXiv, the bioRxiv API **does
- **Abstracts Excluded By Default**: To save context space in the resulting
- **Output Redirection**: Search commands output JSON arrays to standard
- **List Sources** If this skill is used, ensure this is mentioned in the

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。