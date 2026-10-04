# opentargets-database 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：Open Targets 药物靶点识别平台：分析疾病与靶点的遗传学证据、多组学关联度、成药性及临床在研药物。
- **所属领域**：`生物与生命科学`
- **关联标签**：`OpenTargets、新药靶点、成药性`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **OpenTargets** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Open Targets Database Skill**
- **Overview**
- **Prerequisites**
- **Core Rules**
- **Quick Reference**
- **L2G Query Usage**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```bash
uv run scripts/query_opentargets.py --output /tmp/opentargets_results.json [OPTIONS] COMMAND [ARGS]...
```

```bash
uv run scripts/query_opentargets.py custom-query \
  query drugsForDisease($id: String!) {
    disease(efoId: $id) {
      name
      drugAndClinicalCandidates {
        count
        rows {
          maxClinicalStage
          drug {
            id
            name
          }
        }
      }
    }
  }' \
--variables '{"id": "EFO_1001006"}'
--output '/tmp/opentargets_result.json'
```

## 📋 执行要点与最佳实践
- **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
- **Output Flag**: The `--output` flag is always required as output can be
- **Notification**: If this skill is used, ensure this is mentioned in the
- `--output PATH`: **Required**. Path to write the JSON output file.
- `--limit N`: Limit the number of items returned in arrays (default is 50).
- `--page-size N`: Set the API pagination size (default is 200). Increase if
- **`get-gwas-studies`** *`disease_id`*: Fetches all GWAS studies associated
- **`get-study-credible-sets`** *`study_id`*: Fetches all credible sets for a

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。