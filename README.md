# AI Coding Skill Manager (AI Coding 技能管理器)

专为本地 AI Coding 环境打造的全生态可视化技能库管理工具。支持 **Antigravity**、**Claude Code** 与 **Codex** 的 Skill 多层级扫描、被调用率遥测分析、双语对照翻译与同步编辑、直接写回、以及通过 Web 网页进行添加、扫描、禁用、删除与安全回收站还原。

---

## ✨ 核心特性

1. **多层级技能全量扫描识别**：
   - 自动探测并归类：系统内置（Builtin）、全局配置（Global）、插件技能（Plugins）以及工作区（Workspace）中的所有 Skills。
   - 自动识别并解析 YAML Frontmatter 元数据及文档正文。

2. **智能中文功能概要**：
   - 内置高质量中文知识库映射，覆盖开发工作流、需求规划、TDD测试、架构审查、前端UI、生信分析等常用技能。
   - 提取并提炼清晰的中文功能说明与场景标签。
   - 支持在 Web 界面上即时编辑自定义中文概要，数据持久化保存在本地。

3. **被调用率深度遥测（Telemetry）**：
   - 自动分析本地 `~/.gemini/antigravity/brain/*/transcript.jsonl` 会话历史日志。
   - 统计每个技能的**总被调用次数**、**会话命中率（Session Hit Rate）**、**总调用占比**以及**最后调用时间**。
   - 采用增量文件指纹缓存技术，毫秒级快速重扫描。

4. **网页端全生命周期控制**：
   - **一键扫描刷新**：重新探测目录变更与历史日志增量。
   - **安全启用/禁用（Toggle）**：通过安全的 `SKILL.md` 与 `SKILL.md.disabled` 无侵入互转，Antigravity 即刻响应。
   - **可视化新建**：表单配置名称、中文概要、Markdown指引，一键生成标准规范 Skill。
   - **Git 仓库一键导入**：输入 GitHub/GitLab 仓库链接，浅克隆安装至全局技能库。
   - **安全删除与回收站**：删除后进入专属回收站，支持随时一键还原或彻底粉碎；对系统内置核心技能启用防误删保护。

---

## 🚀 极速启动

双击根目录下的 **`start.bat`**（或右键运行 `start.ps1`）：
脚本将自动初始化虚拟环境、安装轻量依赖并启动服务，随后在你的默认浏览器中自动打开：
```
http://127.0.0.1:8765
```

### 手动命令行启动

```powershell
# 1. 激活虚拟环境
.\.venv\Scripts\activate

# 2. 运行管理服务
python run.py
```

---

## 🛠️ 项目结构

```
antigravity skill/
├── backend/
│   ├── config.py             # 核心路径配置（Builtin, Global, Plugins, Trash, Brain）
│   ├── scanner.py            # 本地技能探测与 YAML Frontmatter 解析
│   ├── telemetry.py          # 会话日志深度解析与调用率计算器
│   ├── manager.py            # 技能创建、状态切换、回收站、Git导入
│   ├── translator.py         # 中文功能概要知识库与映射引擎
│   └── server.py             # FastAPI RESTful API 与静态服务路由
├── static/
│   ├── index.html            # 现代精致 Web 控制台（Vue 3 + Tailwind CSS + Lucide）
│   └── app.js                # 前端交互、状态管理与筛选排序逻辑
├── tests/
│   ├── test_all.py           # 扫描、生命周期、回收站完整单元测试
│   └── test_api.py           # REST API 端点集成测试
├── requirements.txt          # 依赖清单
├── start.bat                 # Windows 一键启动脚本
├── start.ps1                 # PowerShell 启动脚本
└── run.py                    # 服务运行入口
```

---

## 🧪 自动化测试验证

项目内置了完备的自动化测试：
```powershell
.\.venv\Scripts\python tests\test_all.py
.\.venv\Scripts\python tests\test_api.py
```
全部测试通过，保障在真实 Antigravity 环境下运行稳定可靠。
