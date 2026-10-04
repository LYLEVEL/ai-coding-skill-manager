# protein-sequence-msa 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：Clustal Omega 蛋白质多序列比对：执行多条蛋白质序列的同源比对，分析序列保守区域与核心催化残基。
- **所属领域**：`生物与生命科学`
- **关联标签**：`多序列比对、ClustalOmega、保守性分析`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **多序列比对** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Prerequisites**
- **Core Rules**
- **Goal**
- **Instructions**
- **References**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```
    >Sequence_1_Name
    MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQ
    QRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
    >Sequence_2_Name
    MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQ
    QRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
    ```

```bash
    uv run scripts/msa_align.py <INPUT_FASTA> -o <OUTPUT_FILE>
    ```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the alignment using
- **Notification**: If this skill is used, ensure this is mentioned in the
- **Always state the method:** Every report must clearly state that the
- **No Hallucinations**: Do NOT invent alignments or conservation metrics.
- **Identity Metric Options:** The choice of denominator determines how
- **Pairwise - Sequence Coverage:** `(Identical Residue Matches) /
- **Pairwise - Global Identity:** `(Identical Residue Matches) /
- **Pairwise - Overlap Identity:** `(Identical Residue Matches) /

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。