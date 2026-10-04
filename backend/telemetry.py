# -*- coding: utf-8 -*-
"""
调用率与调用历史遥测分析模块
负责解析 Antigravity Brain 目录下的 transcript.jsonl，提取技能的调用频次、命中会话及最近调用时间
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from .config import BRAIN_DIR, TELEMETRY_CACHE_FILE

# 匹配技能路径的通用正则表达式（兼容斜杠/反斜杠/转义反斜杠）
SKILL_PATH_PATTERN = re.compile(
    r'skills(?:/|\\\\|\\)+([a-zA-Z0-9_\-\.]+)(?:/|\\\\|\\)+SKILL\.md',
    re.IGNORECASE
)

class TelemetryAnalyzer:
    def __init__(self):
        self.cache: Dict[str, Any] = {
            "total_sessions": 0,
            "skills": {},  # skill_name -> {call_count, sessions: [], last_called_at}
            "file_mtimes": {} # transcript_path -> mtime
        }
        self.load_cache()

    def load_cache(self):
        if TELEMETRY_CACHE_FILE.exists():
            try:
                with open(TELEMETRY_CACHE_FILE, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
            except Exception as e:
                print(f"[Telemetry] 缓存读取失败，重新构建: {e}")
                self.cache = {"total_sessions": 0, "skills": {}, "file_mtimes": {}}

    def save_cache(self):
        try:
            with open(TELEMETRY_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Telemetry] 缓存保存失败: {e}")

    def scan_brain_logs(self, force_full: bool = False) -> Dict[str, Any]:
        """
        扫描 brain 目录下的会话日志并更新调用数据
        """
        if not BRAIN_DIR.exists():
            return {"total_sessions": 0, "skills": {}}

        if force_full:
            self.cache = {"total_sessions": 0, "skills": {}, "file_mtimes": {}}

        skills_stats = self.cache.setdefault("skills", {})
        file_mtimes = self.cache.setdefault("file_mtimes", {})
        
        session_dirs = [d for d in BRAIN_DIR.iterdir() if d.is_dir()]
        total_sessions = len(session_dirs)
        self.cache["total_sessions"] = total_sessions

        updated_files_count = 0

        for s_dir in session_dirs:
            session_id = s_dir.name
            transcript_file = s_dir / ".system_generated" / "logs" / "transcript.jsonl"
            if not transcript_file.exists():
                continue

            try:
                stat = transcript_file.stat()
                mtime = stat.st_mtime
                file_key = str(transcript_file)

                # 增量优化：如果未变动则跳过
                if not force_full and file_mtimes.get(file_key) == mtime:
                    continue

                file_mtimes[file_key] = mtime
                updated_files_count += 1

                with open(transcript_file, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if not line.strip() or "SKILL.md" not in line:
                            continue
                        
                        try:
                            # 仅统计 MODEL 产生的 tool_calls 调用（精准真实触发，避免搜索和响应文本重复干扰）
                            if '"tool_calls"' not in line:
                                continue
                            
                            item = json.loads(line)
                            created_at = item.get("created_at") or ""
                            tool_calls = item.get("tool_calls") or []
                            
                            for call in tool_calls:
                                name = call.get("name")
                                if name in ("view_file", "read_file"):
                                    args = call.get("args") or {}
                                    raw_path = str(args.get("AbsolutePath") or args.get("path") or "")
                                    match = SKILL_PATH_PATTERN.search(raw_path)
                                    if match:
                                        skill_name = match.group(1).lower()
                                        stat_item = skills_stats.setdefault(skill_name, {
                                            "call_count": 0,
                                            "sessions": [],
                                            "last_called_at": ""
                                        })
                                        stat_item["call_count"] += 1
                                        if session_id not in stat_item["sessions"]:
                                            stat_item["sessions"].append(session_id)
                                        if created_at and (not stat_item["last_called_at"] or created_at > stat_item["last_called_at"]):
                                            stat_item["last_called_at"] = created_at
                        except Exception:
                            continue
            except Exception:
                continue

        # 计算比率指标
        total_calls_all = sum(s.get("call_count", 0) for s in skills_stats.values())
        
        result_stats = {}
        for s_name, data in skills_stats.items():
            hit_sessions = len(data.get("sessions", []))
            call_rate = round((hit_sessions / max(total_sessions, 1)) * 100, 2)
            share_rate = round((data.get("call_count", 0) / max(total_calls_all, 1)) * 100, 2)
            
            result_stats[s_name] = {
                "call_count": data.get("call_count", 0),
                "session_hit_count": hit_sessions,
                "session_hit_rate": f"{call_rate}%",
                "call_share_rate": f"{share_rate}%",
                "last_called_at": data.get("last_called_at", "-")
            }

        self.save_cache()
        return {
            "total_sessions": total_sessions,
            "total_calls": total_calls_all,
            "updated_files_count": updated_files_count,
            "skills": result_stats
        }

    def get_skill_stats(self, skill_name: str) -> Dict[str, Any]:
        s_name = skill_name.lower().strip()
        data = self.cache.get("skills", {}).get(s_name, {})
        total_sessions = max(self.cache.get("total_sessions", 1), 1)
        total_calls_all = sum(s.get("call_count", 0) for s in self.cache.get("skills", {}).values())
        
        hit_sessions = len(data.get("sessions", []))
        call_count = data.get("call_count", 0)
        call_rate = round((hit_sessions / total_sessions) * 100, 2)
        share_rate = round((call_count / max(total_calls_all, 1)) * 100, 2)
        
        return {
            "call_count": call_count,
            "session_hit_count": hit_sessions,
            "session_hit_rate": f"{call_rate}%",
            "call_share_rate": f"{share_rate}%",
            "last_called_at": data.get("last_called_at", "-")
        }

telemetry_analyzer = TelemetryAnalyzer()
