# -*- coding: utf-8 -*-
"""
本地技能扫描与元数据解析模块
支持多平台统一扫描：Google Antigravity、Anthropic Claude Code、OpenAI Codex
解析 Frontmatter、文件状态、多语言对照与调用遥测
"""

import os
import json
import yaml
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import (
    PLATFORM_ANTIGRAVITY,
    PLATFORM_CLAUDE,
    PLATFORM_CODEX,
    SUPPORTED_PLATFORMS,
    BUILTIN_SKILLS_DIR,
    GLOBAL_SKILLS_DIR,
    PLUGINS_DIR,
    CLAUDE_GLOBAL_SKILLS_DIR,
    CLAUDE_PLUGINS_DIR,
    CODEX_BUILTIN_SKILLS_DIR,
    CODEX_GLOBAL_SKILLS_DIR,
    CODEX_PLUGINS_DIR,
    CODEX_VENDOR_SKILLS_DIR,
    METADATA_FILE,
    APP_ROOT
)
from .translator import get_chinese_summary
from .telemetry import telemetry_analyzer
from .doc_translator import doc_translator

class SkillScanner:
    def __init__(self):
        self.meta_store: Dict[str, Any] = {}
        self.load_custom_metadata()

    def load_custom_metadata(self):
        """读取用户自定义/覆盖的中文概要与元数据"""
        if METADATA_FILE.exists():
            try:
                with open(METADATA_FILE, "r", encoding="utf-8") as f:
                    self.meta_store = json.load(f)
            except Exception as e:
                print(f"[Scanner] 读取元数据文件失败: {e}")
                self.meta_store = {}

    def save_custom_metadata(self):
        """持久化自定义元数据"""
        try:
            with open(METADATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.meta_store, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Scanner] 保存元数据文件失败: {e}")

    def parse_skill_file(
        self,
        skill_dir: Path,
        skill_type: str,
        platform: str = PLATFORM_ANTIGRAVITY,
        plugin_name: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        解析指定技能目录下的 SKILL.md 或 SKILL.md.disabled
        """
        if not skill_dir.is_dir():
            return None

        # 检查是否为禁用状态
        is_enabled = True
        skill_file = skill_dir / "SKILL.md"
        disabled_file = skill_dir / "SKILL.md.disabled"

        if not skill_file.exists():
            if disabled_file.exists():
                skill_file = disabled_file
                is_enabled = False
            elif skill_dir.name.endswith(".disabled"):
                cand = skill_dir / "SKILL.md"
                if cand.exists():
                    skill_file = cand
                    is_enabled = False
                else:
                    return None
            else:
                return None

        # 读取内容与 YAML Frontmatter
        try:
            content = skill_file.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"[Scanner] 读取技能文件失败: {skill_file}: {e}")
            return None

        frontmatter = {}
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except Exception:
                    frontmatter = {}

        raw_name = frontmatter.get("name") or skill_dir.name.replace(".disabled", "")
        raw_desc = frontmatter.get("description") or ""

        # 查找或融合中文概要
        key = raw_name.lower().strip()
        custom_data = self.meta_store.get(key, {})
        default_zh = get_chinese_summary(raw_name, raw_desc)

        chinese_summary = custom_data.get("summary") or default_zh["summary"]
        category = custom_data.get("category") or default_zh["category"]
        tags = custom_data.get("tags") or default_zh["tags"]

        # 获取历史调用遥测数据 (Antigravity 具有完整日志分析)
        stats = telemetry_analyzer.get_skill_stats(raw_name)

        # 获取已缓存或原生的中文详细使用指南
        cached_zh_body = doc_translator.get_cached_translation(raw_name)
        is_native_chinese = sum(1 for c in body if '\u4e00' <= c <= '\u9fa5') > len(body) * 0.3 if body else False
        chinese_body = cached_zh_body or (body if is_native_chinese else "")

        # 获取物理文件添加/创建时间
        created_timestamp = 0
        try:
            stat_target = skill_file if (skill_file and skill_file.exists()) else skill_dir
            if stat_target and stat_target.exists():
                st = stat_target.stat()
                created_timestamp = st.st_ctime if st.st_ctime > 0 else st.st_mtime
        except Exception:
            created_timestamp = 0

        created_at_str = (
            datetime.datetime.fromtimestamp(created_timestamp).strftime("%Y-%m-%d %H:%M:%S")
            if created_timestamp > 0 else "未知"
        )

        platform_labels = {
            PLATFORM_ANTIGRAVITY: "Antigravity",
            PLATFORM_CLAUDE: "Claude Code",
            PLATFORM_CODEX: "Codex"
        }

        return {
            "id": f"{platform}:{skill_type}:{raw_name}",
            "name": raw_name,
            "platform": platform,
            "platform_label": platform_labels.get(platform, platform.capitalize()),
            "type": skill_type,  # builtin, global, plugin, workspace, vendor
            "plugin_name": plugin_name,
            "path": str(skill_dir),
            "skill_file": str(skill_file),
            "is_enabled": is_enabled,
            "description": raw_desc,
            "chinese_summary": chinese_summary,
            "category": category,
            "tags": tags,
            "body": body,
            "chinese_body": chinese_body,
            "has_chinese_doc": bool(chinese_body),
            "call_count": stats["call_count"],
            "session_hit_count": stats["session_hit_count"],
            "session_hit_rate": stats["session_hit_rate"],
            "call_share_rate": stats["call_share_rate"],
            "last_called_at": stats["last_called_at"],
            "created_at": created_at_str,
            "created_timestamp": created_timestamp,
            "has_scripts": (skill_dir / "scripts").exists(),
            "has_examples": (skill_dir / "examples").exists(),
            "has_references": (skill_dir / "references").exists(),
            "is_customized": key in self.meta_store
        }

    def _scan_directory_skills(
        self,
        base_dir: Path,
        skill_type: str,
        platform: str,
        plugin_name: str = "",
        recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """安全扫描指定目录下的技能目录"""
        results: List[Dict[str, Any]] = []
        if not base_dir.exists() or not base_dir.is_dir():
            return results

        try:
            # 检查 base_dir 本身是否就是一个技能
            if (base_dir / "SKILL.md").exists() or (base_dir / "SKILL.md.disabled").exists():
                s = self.parse_skill_file(base_dir, skill_type=skill_type, platform=platform, plugin_name=plugin_name)
                if s:
                    results.append(s)
                return results

            # 遍历直接子目录
            for item in sorted(base_dir.iterdir()):
                if not item.is_dir():
                    continue
                # 跳过隐藏缓存和系统锁目录（除非是系统技能目录）
                if item.name.startswith(".") and item.name != ".system":
                    continue

                if (item / "SKILL.md").exists() or (item / "SKILL.md.disabled").exists() or item.name.endswith(".disabled"):
                    s = self.parse_skill_file(item, skill_type=skill_type, platform=platform, plugin_name=plugin_name)
                    if s:
                        results.append(s)
                elif recursive:
                    # 递归一层（例如 plugins/<plugin>/skills/<skill> 或 vendor/skills/<skill>）
                    for sub in sorted(item.iterdir()):
                        if sub.is_dir() and ((sub / "SKILL.md").exists() or (sub / "SKILL.md.disabled").exists() or sub.name.endswith(".disabled")):
                            s = self.parse_skill_file(sub, skill_type=skill_type, platform=platform, plugin_name=item.name)
                            if s:
                                results.append(s)
        except Exception as e:
            print(f"[Scanner] 扫描目录异常 {base_dir}: {e}")
        return results

    def scan_all_skills(self, workspace_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        全面扫描 Antigravity、Claude Code、Codex 跨平台技能
        """
        self.load_custom_metadata()
        skills: List[Dict[str, Any]] = []
        seen_ids = set()

        def add_skills(new_skills: List[Dict[str, Any]]):
            for s in new_skills:
                if s and s["id"] not in seen_ids:
                    skills.append(s)
                    seen_ids.add(s["id"])

        # ==========================================
        # 1. 扫描 Google Antigravity 技能
        # ==========================================
        add_skills(self._scan_directory_skills(BUILTIN_SKILLS_DIR, "builtin", PLATFORM_ANTIGRAVITY))
        add_skills(self._scan_directory_skills(GLOBAL_SKILLS_DIR, "global", PLATFORM_ANTIGRAVITY))
        # Antigravity 插件目录 plugins/<name>/skills
        if PLUGINS_DIR.exists():
            for p_dir in sorted(PLUGINS_DIR.iterdir()):
                if p_dir.is_dir():
                    p_skills = p_dir / "skills"
                    if p_skills.exists():
                        add_skills(self._scan_directory_skills(p_skills, "plugin", PLATFORM_ANTIGRAVITY, plugin_name=p_dir.name, recursive=True))

        # ==========================================
        # 2. 扫描 Anthropic Claude Code 技能
        # ==========================================
        add_skills(self._scan_directory_skills(CLAUDE_GLOBAL_SKILLS_DIR, "global", PLATFORM_CLAUDE))
        if CLAUDE_PLUGINS_DIR.exists():
            add_skills(self._scan_directory_skills(CLAUDE_PLUGINS_DIR, "plugin", PLATFORM_CLAUDE, recursive=True))

        # ==========================================
        # 3. 扫描 OpenAI Codex 技能
        # ==========================================
        add_skills(self._scan_directory_skills(CODEX_BUILTIN_SKILLS_DIR, "builtin", PLATFORM_CODEX))
        # Codex Global (过滤掉 .system 子目录以免重复)
        if CODEX_GLOBAL_SKILLS_DIR.exists():
            for item in sorted(CODEX_GLOBAL_SKILLS_DIR.iterdir()):
                if item.is_dir() and item.name != ".system":
                    if (item / "SKILL.md").exists() or (item / "SKILL.md.disabled").exists() or item.name.endswith(".disabled"):
                        s = self.parse_skill_file(item, skill_type="global", platform=PLATFORM_CODEX)
                        if s:
                            add_skills([s])
        if CODEX_PLUGINS_DIR.exists():
            add_skills(self._scan_directory_skills(CODEX_PLUGINS_DIR, "plugin", PLATFORM_CODEX, recursive=True))
        if CODEX_VENDOR_SKILLS_DIR.exists():
            add_skills(self._scan_directory_skills(CODEX_VENDOR_SKILLS_DIR, "vendor", PLATFORM_CODEX, recursive=True))

        # ==========================================
        # 4. 扫描当前工作区技能 (Workspace)
        # ==========================================
        ws_candidates = []
        if workspace_path:
            ws_candidates.append(Path(workspace_path))
        ws_candidates.append(APP_ROOT)

        for ws in ws_candidates:
            # Antigravity 工作区
            for cand in [ws / ".agents" / "skills", ws / ".agent" / "skills"]:
                add_skills(self._scan_directory_skills(cand, "workspace", PLATFORM_ANTIGRAVITY))
            # Claude 工作区
            add_skills(self._scan_directory_skills(ws / ".claude" / "skills", "workspace", PLATFORM_CLAUDE))
            # Codex 工作区
            add_skills(self._scan_directory_skills(ws / ".codex" / "skills", "workspace", PLATFORM_CODEX))

        return skills

    def update_custom_metadata(self, skill_name: str, summary: str = "", category: str = "", tags: List[str] = None):
        """保存用户针对指定技能自定义的中文描述与标签"""
        key = skill_name.lower().strip()
        data = self.meta_store.setdefault(key, {})
        if summary:
            data["summary"] = summary
        if category:
            data["category"] = category
        if tags is not None:
            data["tags"] = tags
        self.save_custom_metadata()

skill_scanner = SkillScanner()
