# uv 使用指南与执行规范

> 本指南已针对 Antigravity 本地环境完成结构化汉化对齐，包含核心流程与操作规程。

## 📌 核心功能与定位
- **功能概要**：uv 高性能包管理器检测器：检测并自动安装配置 Python 极速包管理器 uv，确保依赖链路可用。
- **所属领域**：`开发环境`
- **关联标签**：`Python、uv、环境配置`

## 🚀 建议触发场景与调用规则
当智能体在对话或任务执行过程中遇到下列情形时，应当主动激活并调用此技能：
1. 需要执行与 **Python** 相关的业务流程或多步协作时；
2. 涉及规范化操作、流程分解或系统化排查的工程任务时；
3. 用户在会话中明确提及相关指令或触发词时。

## 📑 核心结构纲要 (原文档目录)
- **uv (Python Package Manager)**
- **Setup**

## 📋 执行要点与最佳实践
- **Unix/macOS**: `"$HOME/.local/bin/uv" --version`
- **Windows (PowerShell)**: `& "$HOME\.local\bin\uv.exe" --version`
- **Unix/macOS**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows (PowerShell)**: `powershell -ExecutionPolicy ByPass -c
- **Unix/macOS**: `export PATH="$HOME/.local/bin:$PATH" && uv --version`
- **Windows (PowerShell)**: `$env:PATH = "$HOME\.local\bin;" + $env:PATH;

## 💡 提示与说明
- 如需查看未经处理的原始英文规范，可点击上方 **【🇬🇧 英文原版】** 选项卡；
- 您也可以点击顶部 **【编辑】** 按钮，根据项目实际规范直接自定义修改本中文指南。