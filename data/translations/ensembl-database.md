# ensembl-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：Ensembl 基因组与序列数据库：转换基因/转录本/蛋白编号，抓取序列外显子结构并预测突变后果（VEP）。
- **所属领域**：`生物与生命科学`
- **关联标签**：`Ensembl、基因结构、VEP注释`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **Ensembl** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Ensembl Database: ID Mapping and Genomic Features**
- **Prerequisites**
- **Overview**
- **Core Rules**
- **Available Commands**
- **Parsing Outputs**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/ensembl_api.py resolve-gene TP53 --species human --output tp53.json
uv run scripts/ensembl_api.py resolve-gene PCL2 --output pcl2.json # Falls back to synonym resolution
```

```bash
uv run scripts/ensembl_api.py map-id ENSG00000141510 --external-db UniProt --output uniprot_map.json
uv run scripts/ensembl_api.py map-id ENST00000269305 --external-db RefSeq_mRNA --output refseq_map.json
```

```bash
uv run scripts/ensembl_api.py get-sequence 17:7661779-7687550 --species human --output seq.txt
uv run scripts/ensembl_api.py get-sequence chr9:21971100-21971200 --assembly GRCh37 --output seq_grch37.txt
```

## 📋 执行要点与最佳实践
- **ENSG (Gene):** Stable identifier for a human gene. Other species will have
- **ENST (Transcript):** Stable identifier for a transcript (splicing
- **ENSP (Protein):** Stable identifier for a translated protein.
- **MANE Select:** The consensus primary transcript agreed upon by Ensembl and
- **Canonical:** Ensembl's representative transcript (used if MANE is not
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Default Species:** If the species is absent or ambiguous in the prompt,
- **Primary Transcripts:** When listing transcripts for a gene, only return

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。