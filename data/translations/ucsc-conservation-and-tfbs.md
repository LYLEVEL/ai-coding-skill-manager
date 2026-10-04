# ucsc-conservation-and-tfbs 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：UCSC 进化保守度与转录因子结合位点：抓取多物种进化保守评分（phyloP/phastCons）及 ENCODE 转录调控位点。
- **所属领域**：`生物与生命科学`
- **关联标签**：`UCSC、进化保守度、TFBS调控`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **UCSC** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Conservation Scores & TFBS Lookup (UCSC)**
- **Prerequisites**
- **Core Rules**
- **Utility Scripts**
- **Fetching Conservation for Specific Variants**
- **Fetching Regions and Conserved Elements**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/get_conservation.py --coordinates "chr1:215867804" "chr1:215867823" --output /tmp/cons_output.json
```

```bash
uv run scripts/get_conservation.py --coordinates "chr8:11748914-11749085" --conserved-elements --output /tmp/region_cons.json
```

```bash
# hg38 mammal (Hiller 470-way)
uv run scripts/get_conservation.py --coordinates "chr5:1045330-1046172" --collection mammal --output /tmp/mammal_cons.json

# hg19 with legacy 46-vertebrate alignment
uv run scripts/get_conservation.py --coordinates "chr5:1045330-1046172" --genome hg19 --collection vertebrate46 --output /tmp/vert46_cons.json
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Large Output Handling**: Always pass --output to redirect output to a
- **Notification**: If this skill is used, ensure this is mentioned in the
- **`vertebrate`** (default): UCSC 100-vertebrate Multiz alignment. phyloP:
- **`mammal`**: Hiller Lab 470-way mammalian alignment. phyloP:
- **`primate`**: UCSC 30-primate Multiz alignment. phyloP: `phyloP30way`,
- **`vertebrate`** (default): UCSC 100-vertebrate Multiz alignment. phyloP:
- **`vertebrate46`**: UCSC 46-vertebrate Multiz alignment (legacy). phyloP:

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。