# workflow-skill-creator 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：工作流技能提炼器：将刚刚完成的会话操作流程自动萃取、总结并封装为可复用的新 Skill 规范。
- **所属领域**：`核心基础`
- **关联标签**：`技能提炼、流程沉淀、复用封装`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **技能提炼** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **Workflow-to-Skill Distiller**
- **Phase 1: Brainstorming (MANDATORY)**
- **Round 1: Understand the Workflow**
- **Round 2: Flexibility and Error Handling**
- **Round 3: Dependencies and Resources**
- **Round 4: Scope and Shape**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```markdown
## Workflow

### 1. Step Name
- Description of what to do
- Which skill to use and how

### 2. Next Step
...
```

```markdown
---
name: {skill-name}
description: >-
  {description}
---

# {Skill Title}

## Overview
{Brief description of what the skill does.}

## Dependencies
{List of required skills, if any.}

## Quick Start
{Minimal example to get started.}

## Utility Scripts (if CLI-based)
{Document each subcommand with examples.}

## Workflow (if instruction-only)
{Numbered steps with clear instructions.}

## Rate Limiting (if applicable)
{Document rate limits and how they are enforced.}

## Common Mistakes
{List 2-3 common pitfalls.}
```

## 📋 执行要点与最佳实践
- If code is needed: "Some of these steps involve [fetching data from an
- If no code is needed: "This workflow is entirely about following a set
- [ ] What is the workflow's purpose and scope?
- [ ] What are the inputs and outputs?
- [ ] Which steps are strict vs. flexible?
- [ ] Which existing skills should be referenced?
- [ ] What new scripts (if any) are needed?
- [ ] What rate limits apply?

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。