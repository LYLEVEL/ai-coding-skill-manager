# ncbi-sequence-fetch 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：NCBI 序列自动抓取：通过 E-utilities 工具根据 Accession 序列号拉取核酸与蛋白质 FASTA 完整序列。
- **所属领域**：`生物与生命科学`
- **关联标签**：`NCBI、FASTA下载、序列检索`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **NCBI** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **NCBI Sequence Fetch**
- **Prerequisites**
- **Core Rules**
- **Overview**
- **Utility Scripts**
- **1. Fetch Protein by Accession**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/ncbi_fetch.py fetch-protein XP_022033624 -o /tmp/result.json
uv run scripts/ncbi_fetch.py fetch-protein NP_001234567 ABC12345.1
```

```bash
uv run scripts/ncbi_fetch.py fetch-nucleotide MK034466 -o /tmp/result.json
```

```bash
uv run scripts/ncbi_fetch.py cds-translate MK034466 -o /tmp/result.json
uv run scripts/ncbi_fetch.py cds-translate HQ662330 --target-length 1043
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **API Key Support**: If the user provides an `NCBI_API_KEY` in their
- **Notification**: If this skill is used, ensure this is mentioned in the
- `fetch-protein` — Direct protein accession lookup (GenPept, RefSeq)
- `fetch-nucleotide` — Direct nucleotide accession lookup
- `cds-translate` — Fetch CDS and translate to protein (3 methods)
- `search` — Free-text search of any NCBI database
- `elink` — Follow cross-database links (PubMed→Protein, etc.)

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。