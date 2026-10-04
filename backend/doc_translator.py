# -*- coding: utf-8 -*-
"""
Microsoft Edge 官方翻译引擎模块 (Edge Translator API)
全面改用微软 Edge 官方翻译端口：https://edge.microsoft.com/translate/translatetext
支持原生多段落批量数组传输、代码块保护、高并发、无 429 限流、国内极速直连
"""

import os
import re
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, List

from .config import DATA_DIR
from .translator import get_chinese_summary

TRANSLATIONS_DIR = DATA_DIR / "translations"
TRANSLATIONS_DIR.mkdir(parents=True, exist_ok=True)

EDGE_TRANSLATE_URL = "https://edge.microsoft.com/translate/translatetext?from=en&to=zh-Hans"

EDGE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

class EdgeDocTranslator:
    def __init__(self):
        pass

    def get_cache_path(self, skill_name: str) -> Path:
        safe_name = skill_name.strip().lower().replace("/", "_").replace("\\", "_").replace(":", "_")
        return TRANSLATIONS_DIR / f"{safe_name}.md"

    def get_cached_translation(self, skill_name: str) -> Optional[str]:
        cache_file = self.get_cache_path(skill_name)
        if cache_file.exists():
            try:
                content = cache_file.read_text(encoding="utf-8")
                if content and len(content.strip()) > 30:
                    return content
            except Exception:
                return None
        return None

    def save_translation(self, skill_name: str, content: str):
        cache_file = self.get_cache_path(skill_name)
        try:
            cache_file.write_text(content, encoding="utf-8")
        except Exception as e:
            print(f"[EdgeTranslator] 保存翻译失败: {e}")

    def translate_texts_with_edge(self, texts: List[str], max_retries: int = 2) -> List[str]:
        """
        调用微软 Edge 官方接口批量翻译文本列表
        支持单次批量数组传输，无需任何第三方 Key，响应极快
        """
        if not texts:
            return []

        payload = json.dumps(texts).encode("utf-8")
        req = urllib.request.Request(EDGE_TRANSLATE_URL, data=payload, headers=EDGE_HEADERS)

        for attempt in range(max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    results = []
                    for item in resp_data:
                        trans = item.get("translations", [{}])[0].get("text", "")
                        results.append(trans)
                    if len(results) == len(texts):
                        return results
            except Exception as e:
                if attempt == max_retries:
                    print(f"[EdgeTranslator] Edge 翻译请求失败: {e}")
                    return texts
                time.sleep(0.5)

        return texts

    def translate_markdown(self, markdown_text: str, skill_name: str = "") -> str:
        """
        基于 Microsoft Edge 端口的 Markdown 无损智能翻译
        1. 保护全部代码块 ```...``` 与特殊指令
        2. 将普通 Markdown 段落作为数组直接传递给 Edge 接口批量翻译
        3. 回填代码块，保留结构化排版
        4. 缓存到本地永久生效
        """
        if not markdown_text or not markdown_text.strip():
            return "（暂无指南正文内容）"

        # 检查是否已包含大量中文（例如原生中文技能）
        chinese_char_count = sum(1 for c in markdown_text if '\u4e00' <= c <= '\u9fa5')
        if chinese_char_count > len(markdown_text) * 0.35:
            if skill_name:
                self.save_translation(skill_name, markdown_text)
            return markdown_text

        # 1. 抽取并保护多行代码块 ``` ... ```
        code_blocks = {}
        def code_block_repl(match):
            idx = len(code_blocks)
            key = f"__EDGE_CODE_BLOCK_{idx}__"
            code_blocks[key] = match.group(0)
            return f"\n\n{key}\n\n"

        text_protected = re.sub(r'```[\s\S]*?```', code_block_repl, markdown_text)

        # 2. 按空行切分为段落列表
        raw_paragraphs = [p for p in text_protected.split("\n\n") if p.strip()]

        # 3. 区分需要翻译的段落和代码块占位符
        texts_to_translate = []
        mapping_indices = []

        for i, p in enumerate(raw_paragraphs):
            p_strip = p.strip()
            if p_strip.startswith("__EDGE_CODE_BLOCK_") and p_strip.endswith("__"):
                continue
            texts_to_translate.append(p)
            mapping_indices.append(i)

        # 4. 调用 Edge 官方接口批量翻译（若文本较多分块发送，每块最多 30 个段落）
        chunk_size = 25
        translated_map = {}

        for start_idx in range(0, len(texts_to_translate), chunk_size):
            chunk = texts_to_translate[start_idx : start_idx + chunk_size]
            chunk_indices = mapping_indices[start_idx : start_idx + chunk_size]
            
            trans_chunk = self.translate_texts_with_edge(chunk)
            for idx, trans_text in zip(chunk_indices, trans_chunk):
                translated_map[idx] = trans_text

        # 5. 组合最终段落
        final_paragraphs = []
        for i, p in enumerate(raw_paragraphs):
            if i in translated_map:
                final_paragraphs.append(translated_map[i])
            else:
                final_paragraphs.append(p)

        full_translated = "\n\n".join(final_paragraphs)

        # 6. 回填代码块 ```...```
        for key, orig in code_blocks.items():
            full_translated = full_translated.replace(key, orig)

        # 7. 持久化缓存
        if skill_name:
            self.save_translation(skill_name, full_translated)

        return full_translated

doc_translator = EdgeDocTranslator()
