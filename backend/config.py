# -*- coding: utf-8 -*-
"""
多平台路径与核心全局配置
支持 Google Antigravity、Anthropic Claude Code、OpenAI Codex 三大 AI 助手技能生态
"""

import os
import sys
import shutil
from pathlib import Path

# 基础目录配置
USER_HOME = Path.home()
GEMINI_DIR = USER_HOME / ".gemini"
CLAUDE_DIR = USER_HOME / ".claude"
CODEX_DIR = USER_HOME / ".codex"

# 平台标识常量
PLATFORM_ANTIGRAVITY = "antigravity"
PLATFORM_CLAUDE = "claude"
PLATFORM_CODEX = "codex"

SUPPORTED_PLATFORMS = [
    {
        "id": PLATFORM_ANTIGRAVITY,
        "name": "Antigravity",
        "vendor": "Google",
        "description": "Google Antigravity 智能编码助手",
        "icon": "orbit",
        "tag_color": "emerald"
    },
    {
        "id": PLATFORM_CLAUDE,
        "name": "Claude Code",
        "vendor": "Anthropic",
        "description": "Anthropic Claude Code 命令行助手",
        "icon": "bot",
        "tag_color": "amber"
    },
    {
        "id": PLATFORM_CODEX,
        "name": "Codex",
        "vendor": "OpenAI",
        "description": "OpenAI Codex 智能开发环境",
        "icon": "cpu",
        "tag_color": "indigo"
    }
]

# Antigravity 各层级技能路径
BUILTIN_SKILLS_DIR = GEMINI_DIR / "antigravity" / "builtin" / "skills"
GLOBAL_SKILLS_DIR = GEMINI_DIR / "config" / "skills"
PLUGINS_DIR = GEMINI_DIR / "config" / "plugins"
TRASH_DIR = GEMINI_DIR / "config" / ".skills_trash"
BRAIN_DIR = GEMINI_DIR / "antigravity" / "brain"

# Claude Code 技能路径
CLAUDE_GLOBAL_SKILLS_DIR = CLAUDE_DIR / "skills"
CLAUDE_PLUGINS_DIR = CLAUDE_DIR / "plugins" / "cache"
CLAUDE_TRASH_DIR = CLAUDE_DIR / ".skills_trash"

# Codex 技能路径
CODEX_BUILTIN_SKILLS_DIR = CODEX_DIR / "skills" / ".system"
CODEX_GLOBAL_SKILLS_DIR = CODEX_DIR / "skills"
CODEX_PLUGINS_DIR = CODEX_DIR / "plugins" / "cache"
CODEX_VENDOR_SKILLS_DIR = CODEX_DIR / "vendor_imports" / "skills" / "skills" / ".curated"
CODEX_TRASH_DIR = CODEX_DIR / ".skills_trash"

# 本工具程序包根目录（兼容 PyInstaller 冻结打包与源码运行）
if getattr(sys, 'frozen', False):
    APP_ROOT = Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent))
else:
    APP_ROOT = Path(__file__).resolve().parent.parent

# 用户持久化数据目录（存放在用户目录，避免安装至 Program Files 等系统目录下的权限写入问题）
DATA_DIR = GEMINI_DIR / "config" / "skill_manager_data"
METADATA_FILE = DATA_DIR / "skills_meta.json"
TELEMETRY_CACHE_FILE = DATA_DIR / "telemetry_cache.json"

# 确保必要的目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)
TRASH_DIR.mkdir(parents=True, exist_ok=True)
GLOBAL_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
CLAUDE_GLOBAL_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
CLAUDE_TRASH_DIR.mkdir(parents=True, exist_ok=True)
CODEX_GLOBAL_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
CODEX_TRASH_DIR.mkdir(parents=True, exist_ok=True)

# 如果安装包内置了预热好的 data/translations，首次启动时自动同步到用户数据目录
BUILTIN_DATA_DIR = APP_ROOT / "data"
if BUILTIN_DATA_DIR.exists() and BUILTIN_DATA_DIR != DATA_DIR:
    builtin_trans = BUILTIN_DATA_DIR / "translations"
    target_trans = DATA_DIR / "translations"
    target_trans.mkdir(parents=True, exist_ok=True)
    if builtin_trans.exists():
        for f in builtin_trans.glob("*.md"):
            dest_f = target_trans / f.name
            if not dest_f.exists():
                try:
                    shutil.copy2(f, dest_f)
                except Exception:
                    pass
    # 同步初始 skills_meta.json
    builtin_meta = BUILTIN_DATA_DIR / "skills_meta.json"
    if builtin_meta.exists() and not METADATA_FILE.exists():
        try:
            shutil.copy2(builtin_meta, METADATA_FILE)
        except Exception:
            pass
