import json

with open('data/raw_skills.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for i, item in enumerate(items):
    desc = item['desc'].replace('\n', ' ').strip()
    print(f"{i+1:2d}. [{item['type']:7s}] {item['name']:35s} | {desc[:60]}...")
