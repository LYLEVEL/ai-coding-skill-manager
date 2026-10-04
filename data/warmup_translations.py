# -*- coding: utf-8 -*-
"""
高频技能中文使用指南预热脚本
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.scanner import skill_scanner
from backend.doc_translator import doc_translator

# 核心高频推荐技能
HOT_SKILLS = [
    "brainstorming",
    "writing-plans",
    "executing-plans",
    "test-driven-development",
    "systematic-debugging",
    "frontend-design",
    "subagent-driven-development",
    "using-git-worktrees",
    "verification-before-completion",
    "requesting-code-review"
]

def warmup():
    print("开始预热核心高频技能的中文指南翻译...")
    skills = skill_scanner.scan_all_skills()
    for name in HOT_SKILLS:
        target = next((s for s in skills if s["name"].lower() == name.lower()), None)
        if target and target.get("body"):
            cached = doc_translator.get_cached_translation(name)
            if not cached:
                print(f" -> 正在自动翻译: {name} (字数: {len(target['body'])})...")
                try:
                    res = doc_translator.translate_markdown(target["body"], skill_name=name)
                    print(f"    [OK] {name} 翻译完成并已缓存 (翻译后字数: {len(res)})")
                except Exception as e:
                    print(f"    [ERR] {name} 翻译失败: {e}")
            else:
                print(f" -> 已有缓存: {name}")
    print("核心技能中文指南预热完成！")

if __name__ == "__main__":
    warmup()
