# pymol 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：PyMOL 分子结构渲染与空间分析：生成高质量蛋白质 3D 构象渲染图、空间结构对齐与结合位点残基标注。
- **所属领域**：`生物与生命科学`
- **关联标签**：`PyMOL、分子渲染、空间对齐`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **PyMOL** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **PyMOL**
- **Prerequisites**
- **Overview**
- **Setup (Agent Instructions)**
- **Core Rules**
- **Quick Start**

## 💻 关键配置与代码示例
以下为本技能内置的规范执行代码与操作模板：

```python
# /// script
# requires-python = ">=3.10, <3.13"
# dependencies = [
#     "pymol-open-source-whl",
# ]
# ///

import os
import sys

# Set environment variable for headless rendering
os.environ["PYOPENGL_PLATFORM"] = "osmesa"

import pymol # pytype: disable=import-error
pymol.pymol_argv = ["pymol", "-cq"]
pymol.finish_launching()

from pymol import cmd # pytype: disable=import-error

cmd.load("AF-P00520-F1-model_v4.cif", "structure")
cmd.show("cartoon")
cmd.color("green", "ss h")
cmd.color("yellow", "ss s")
cmd.color("gray", "ss l+''")
cmd.orient()
cmd.set("ray_opaque_background", 1)
cmd.png("output/render.png", width=1200, height=900, dpi=150)
cmd.save("output/session.pse")
cmd.quit()
```

## 📋 执行要点与最佳实践
- The user wants to run AlphaFold predictions.
- The user wants docking or molecular dynamics simulations.
- The user only has a sequence and no structure file — fetch the structure
- **Output paths must be absolute or relative to the user's project root.**
- **Software rendering only.** Use `cmd.png()` for output. Never use
- **Always save a `.pse` session file** alongside any PNG output. This lets
- **Always call `cmd.quit()`** at the end of every PyMOL script. Omitting it
- **Init boilerplate is mandatory.** Every PyMOL script must begin with the

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。