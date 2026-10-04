import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from backend.scanner import skill_scanner

skills = skill_scanner.scan_all_skills()

all_pass = True
for s in skills:
    zh = s.get('chinese_summary', '')
    chinese_char_count = sum(1 for c in zh if '\u4e00' <= c <= '\u9fa5')
    if chinese_char_count < 6 or "功能简要" in zh:
        print(f"[FAIL] {s['name']} - 中文字数: {chinese_char_count}, 内容: {zh}")
        all_pass = False

if all_pass:
    print(f"[SUCCESS] 全部 {len(skills)} 个技能均具备完整纯正的中文功能概要！")
else:
    print("[FAIL] 仍有技能未完全汉化")
