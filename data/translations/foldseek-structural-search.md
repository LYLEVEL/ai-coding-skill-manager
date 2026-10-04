# foldseek-structural-search 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：Foldseek 蛋白质三维结构极速比对：传入 PDB/CIF 结构坐标文件，在结构数据库中快速检索相似构象。
- **所属领域**：`生物与生命科学`
- **关联标签**：`Foldseek、结构比对、同源构象`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **Foldseek** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Prerequisites**
- **Goal**
- **Core Rules**
- **Instructions**
- *** If the API returns an error or the file is missing, inform the user clearly**

## 📋 执行要点与最佳实践
- **File Requirement**: This tool absolutely cannot search by sequence, name,
- **Strict Validation**: Never bypass the input validation or the database
- **Do Not Parse the JSON**: Rely entirely on the generated `.md` file for
- **No Raw Parsing**: Do not attempt to parse or read the raw 3D coordinates
- **Notification**: If this skill is used, ensure this is mentioned in the
- If the user provided a protein name, an amino acid sequence, or an
- Inform the user that Foldseek requires a physical 3D coordinate file,
- **Allowed List:** `afdb50`, `afdb-swissprot`, `pdb100`, `BFVD`,

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。