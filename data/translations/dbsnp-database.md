# dbsnp-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：NCBI dbSNP 短突变位点数据库：根据 rsID 查询单核苷酸多态性（SNP）、等位基因频率与 GRCh38 基因组坐标。
- **所属领域**：`生物与生命科学`
- **关联标签**：`dbSNP、SNP变异、等位基因频率`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **dbSNP** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **dbSNP Database Integration**
- **Prerequisites**
- **Core Rules**
- **When to Use**
- **Command Selection Guide**
- **Quick Start**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
# Look up variant rs7412: type, gene, clinical significance, MAF
uv run scripts/dbsnp_cli.py get-variant rs7412 --output /tmp/rs7412.json

# Find the rsID for a variant at chr8:19962213 C>T
uv run scripts/dbsnp_cli.py resolve-variant 8 19962213 C T \
  --output /tmp/resolve.json
```

```bash
uv run scripts/dbsnp_cli.py get-variant rs268 --output /tmp/rs268.json
uv run scripts/dbsnp_cli.py get-variant 268 --assembly GCF_000001405.40 \
  --output /tmp/rs268.json
```

```bash
uv run scripts/dbsnp_cli.py resolve-variant 8 19962213 C T \
  --output /tmp/resolve.json
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided wrapper script
- **Command Choice**: Do NOT use `search-region` to find the rsID of a
- **Output Size**: Avoid using `--full` on `get-variant` unless specifically
- **Shell Safety**: Always wrap HGVS strings in single quotes to prevent shell
- **Notification**: If this skill is used, ensure this is mentioned in the
- Map a genomic variant to its canonical rsID (from VCF coordinates or HGVS
- Retrieve summary data for an rsID: variant type, gene associations, clinical
- Convert an rsID back to genomic coordinates on a specific assembly.

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。