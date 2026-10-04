# literature-search-arxiv 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：arXiv 预印本学术文献检索：搜索计算机、物理、数学等最新科研论文元数据、摘要并下载全文 PDF。
- **所属领域**：`学术检索`
- **关联标签**：`arXiv、预印本、论文检索`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **arXiv** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **arXiv Search and Retrieval**
- **Prerequisites**
- **Core Rules**
- **Utility Scripts**
- **Reference**
- **Workflow**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/search_arxiv.py --query "au:einstein AND ti:relativity" \
  --max_results 5 2>/dev/null > /tmp/arxiv_search_results.json
```

```bash
uv run scripts/download_paper.py --id 1706.03762 --format pdf --output attention.pdf
```

```bash
uv run scripts/download_paper_source.py --id 2010.11645 --output source.tar.gz
```

## 📋 执行要点与最佳实践
- **Terms of Use**: You MUST respect arXiv's Terms of Use.
- Maximum 1 request every 3 seconds.
- The provided utility scripts handle rate limiting automatically. Always
- If this skill is used, ensure this is mentioned in the output AND list the
- `--query`: Search string. See
- `--id_list`: Comma-separated list of arXiv IDs to fetch directly (e.g.,
- `--start`: Pagination offset (default 0).
- `--max_results`: Number of results to return (default 10).

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。