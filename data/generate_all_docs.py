# -*- coding: utf-8 -*-
"""
为全部 69 个技能一次性生成并缓存结构化中文详细使用指南
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.scanner import skill_scanner
from backend.doc_translator import doc_translator

def run_generate_all():
    skills = skill_scanner.scan_all_skills()
    print(f"开始检查并补齐全部 {len(skills)} 个技能的本地中文详细指南...")
    count = 0
    for s in skills:
        name = s["name"]
        cached = doc_translator.get_cached_translation(name)
        if not cached or len(cached.strip()) < 40:
            doc_translator.translate_markdown(s.get("body", ""), skill_name=name)
            count += 1
            print(f" [+] 已完成中文指南生成与缓存: {name}")
    print(f" 全部技能中文详细使用指南补齐完成！新处理技能数: {count}")

if __name__ == "__main__":
    run_generate_all()
