# -*- coding: utf-8 -*-
"""
多平台技能生命周期管理模块
支持 Google Antigravity、Anthropic Claude Code、OpenAI Codex
负责技能的创建、更新、禁用/启用切换、移入回收站、还原与永久删除
"""

import os
import json
import shutil
import subprocess
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from .config import (
    PLATFORM_ANTIGRAVITY,
    PLATFORM_CLAUDE,
    PLATFORM_CODEX,
    BUILTIN_SKILLS_DIR,
    GLOBAL_SKILLS_DIR,
    PLUGINS_DIR,
    TRASH_DIR,
    CLAUDE_GLOBAL_SKILLS_DIR,
    CLAUDE_TRASH_DIR,
    CODEX_GLOBAL_SKILLS_DIR,
    CODEX_TRASH_DIR,
    APP_ROOT
)
from .scanner import skill_scanner

class SkillManager:
    def __init__(self):
        pass

    def toggle_skill_status(self, skill_id: str, enable: Optional[bool] = None) -> Dict[str, Any]:
        """
        切换技能的启用/禁用状态
        通过重命名 SKILL.md <-> SKILL.md.disabled 实现安全可逆的禁用
        """
        all_skills = skill_scanner.scan_all_skills()
        target = next((s for s in all_skills if s["id"] == skill_id), None)
        if not target:
            # 兼容按 name 查找
            target = next((s for s in all_skills if s["name"].lower() == skill_id.lower()), None)
            
        if not target:
            return {"success": False, "message": f"未找到 ID 或名称为 {skill_id} 的技能"}

        skill_dir = Path(target["path"])
        file_normal = skill_dir / "SKILL.md"
        file_disabled = skill_dir / "SKILL.md.disabled"

        current_enabled = target["is_enabled"]
        target_enable = (not current_enabled) if enable is None else enable

        if target_enable == current_enabled:
            return {"success": True, "is_enabled": current_enabled, "message": "状态无需变更"}

        platform_label = target.get("platform_label", "系统")

        try:
            if target_enable:
                # 启用：将 disabled 改回正常
                if file_disabled.exists():
                    file_disabled.rename(file_normal)
                elif skill_dir.name.endswith(".disabled"):
                    new_dir = skill_dir.parent / skill_dir.name[:-9]
                    skill_dir.rename(new_dir)
                    skill_dir = new_dir
                return {
                    "success": True,
                    "is_enabled": True,
                    "message": f"[{platform_label}] 技能 [{target['name']}] 已成功启用"
                }
            else:
                # 禁用：将 SKILL.md 改为 SKILL.md.disabled
                if file_normal.exists():
                    file_normal.rename(file_disabled)
                return {
                    "success": True,
                    "is_enabled": False,
                    "message": f"[{platform_label}] 技能 [{target['name']}] 已安全禁用（已挂起）"
                }
        except Exception as e:
            return {"success": False, "message": f"切换状态失败: {str(e)}"}

    def create_skill(
        self,
        name: str,
        description: str,
        chinese_summary: str,
        category: str = "实用工具",
        tags: List[str] = None,
        content: str = "",
        target_type: str = "global",
        platform: str = PLATFORM_ANTIGRAVITY,
        workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        新建一个自定义技能，支持指定目标平台生态
        """
        name = name.strip().lower().replace(" ", "-")
        if not name:
            return {"success": False, "message": "技能英文名称不能为空"}

        ws = Path(workspace_path) if workspace_path else APP_ROOT

        # 确定目标父目录
        if platform == PLATFORM_CLAUDE:
            if target_type == "workspace":
                target_parent = ws / ".claude" / "skills"
            else:
                target_parent = CLAUDE_GLOBAL_SKILLS_DIR
        elif platform == PLATFORM_CODEX:
            if target_type == "workspace":
                target_parent = ws / ".codex" / "skills"
            else:
                target_parent = CODEX_GLOBAL_SKILLS_DIR
        else:
            # 默认 Antigravity
            if target_type == "workspace":
                target_parent = ws / ".agents" / "skills"
            else:
                target_parent = GLOBAL_SKILLS_DIR

        target_parent.mkdir(parents=True, exist_ok=True)
        target_dir = target_parent / name

        if target_dir.exists():
            return {"success": False, "message": f"目标目录已存在同名技能: {target_dir}"}

        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            skill_file = target_dir / "SKILL.md"

            # 组织 Markdown 内容
            default_content = content.strip() if content else f"# {name}\n\n## 概述\n{chinese_summary or description}\n\n## 执行指引\n- 步骤 1: 明确任务目标\n- 步骤 2: 规范执行操作\n"
            
            full_text = f"---\nname: {name}\ndescription: >-\n  {description or chinese_summary}\n---\n\n{default_content}\n"
            skill_file.write_text(full_text, encoding="utf-8")

            # 保存自定义中文元数据
            skill_scanner.update_custom_metadata(
                skill_name=name,
                summary=chinese_summary or description,
                category=category,
                tags=tags or ["自定义"]
            )

            platform_names = {PLATFORM_ANTIGRAVITY: "Antigravity", PLATFORM_CLAUDE: "Claude Code", PLATFORM_CODEX: "Codex"}

            return {
                "success": True,
                "message": f"[{platform_names.get(platform, platform)}] 技能 [{name}] 创建成功！",
                "path": str(target_dir)
            }
        except Exception as e:
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
            return {"success": False, "message": f"创建技能失败: {str(e)}"}

    def import_from_git(
        self,
        repo_url: str,
        custom_name: str = "",
        platform: str = PLATFORM_ANTIGRAVITY,
        target_type: str = "global"
    ) -> Dict[str, Any]:
        """
        从 Git 仓库克隆导入技能，支持 Antigravity / Claude Code / Codex
        """
        url = repo_url.strip()
        if not url:
            return {"success": False, "message": "Git 仓库 URL 不能为空"}

        # 提取技能目录名称
        if custom_name and custom_name.strip():
            name = custom_name.strip().lower().replace(" ", "-")
        else:
            clean_url = url.rstrip("/").rstrip(".git")
            parts = clean_url.split("/")
            name = parts[-1].strip().lower().replace(" ", "-") if parts else "imported-skill"

        import re
        name = re.sub(r"[^a-zA-Z0-9_\-]", "", name)
        if not name:
            name = f"skill-{int(datetime.datetime.now().timestamp())}"

        # 确定目标父目录
        if platform == PLATFORM_CLAUDE:
            target_parent = CLAUDE_GLOBAL_SKILLS_DIR
        elif platform == PLATFORM_CODEX:
            target_parent = CODEX_GLOBAL_SKILLS_DIR
        else:
            target_parent = GLOBAL_SKILLS_DIR

        target_parent.mkdir(parents=True, exist_ok=True)
        target_dir = target_parent / name

        if target_dir.exists():
            return {"success": False, "message": f"目标目录已存在同名技能: {name} ({target_dir})"}

        # 检查系统 git 命令
        git_cmd = shutil.which("git")
        if not git_cmd:
            return {"success": False, "message": "系统未检测到 git 命令，请先安装 Git 并配置到系统环境变量 PATH"}

        try:
            # 执行浅克隆 (depth=1)
            cmd = [git_cmd, "clone", "--depth", "1", url, str(target_dir)]
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                timeout=90
            )
            if res.returncode != 0:
                err_msg = res.stderr.strip() or res.stdout.strip() or "Git 克隆失败"
                if target_dir.exists():
                    shutil.rmtree(target_dir, ignore_errors=True)
                return {"success": False, "message": f"Git 克隆失败: {err_msg}"}

            # 检查是否有 SKILL.md 或变体
            skill_md = target_dir / "SKILL.md"
            if not skill_md.exists():
                for cand in target_dir.glob("*.md"):
                    if cand.name.lower() == "skill.md":
                        cand.rename(skill_md)
                        break

            # 如果仍然没有 SKILL.md，尝试从 README.md 派生
            if not skill_md.exists():
                readme_md = None
                for cand in target_dir.glob("*.md"):
                    if cand.name.lower() == "readme.md":
                        readme_md = cand
                        break

                readme_content = ""
                if readme_md and readme_md.exists():
                    readme_content = readme_md.read_text(encoding="utf-8", errors="ignore")

                default_desc = f"基于 Git 仓库导入的技能: {name}"
                first_heading = name
                if readme_content:
                    lines = [ln.strip() for ln in readme_content.splitlines() if ln.strip()]
                    for ln in lines:
                        if ln.startswith("# "):
                            first_heading = ln.replace("#", "").strip()
                            break

                skill_content = (
                    f"---\n"
                    f"name: {name}\n"
                    f"description: >-\n"
                    f"  {default_desc}\n"
                    f"---\n\n"
                    f"# {first_heading}\n\n"
                    f"{readme_content or default_desc}\n"
                )
                skill_md.write_text(skill_content, encoding="utf-8")

            # 读取技能以登记中文概要与标签
            parsed = skill_scanner.parse_skill_file(target_dir, "global", platform)
            summary = (parsed.get("chinese_summary") if parsed else "") or f"从 Git 仓库导入: {name}"
            skill_scanner.update_custom_metadata(
                skill_name=name,
                summary=summary,
                category="Git导入",
                tags=["Git导入", platform]
            )

            platform_names = {PLATFORM_ANTIGRAVITY: "Antigravity", PLATFORM_CLAUDE: "Claude Code", PLATFORM_CODEX: "Codex"}
            return {
                "success": True,
                "message": f"[{platform_names.get(platform, platform)}] 成功从 Git 导入技能 [{name}]！",
                "path": str(target_dir)
            }
        except subprocess.TimeoutExpired:
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
            return {"success": False, "message": "Git 克隆超时，请检查网络连接或仓库地址是否正确"}
        except Exception as e:
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
            return {"success": False, "message": f"导入失败: {str(e)}"}

    def delete_skill_to_trash(self, skill_id: str) -> Dict[str, Any]:
        """
        安全删除：将技能移动至本地回收站，防止误删
        """
        all_skills = skill_scanner.scan_all_skills()
        target = next((s for s in all_skills if s["id"] == skill_id), None)
        if not target:
            target = next((s for s in all_skills if s["name"].lower() == skill_id.lower()), None)
            
        if not target:
            return {"success": False, "message": f"未找到技能: {skill_id}"}

        src_dir = Path(target["path"])
        if not src_dir.exists():
            return {"success": False, "message": f"技能目录不存在: {src_dir}"}

        platform = target.get("platform", PLATFORM_ANTIGRAVITY)
        trash_dir = TRASH_DIR
        if platform == PLATFORM_CLAUDE:
            trash_dir = CLAUDE_TRASH_DIR
        elif platform == PLATFORM_CODEX:
            trash_dir = CODEX_TRASH_DIR
        trash_dir.mkdir(parents=True, exist_ok=True)

        try:
            now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            trash_subname = f"{now_str}_{platform}_{target['type']}_{target['name']}"
            dest_dir = trash_dir / trash_subname

            # 保存原始路径与平台信息，便于一键还原
            meta_info = {
                "original_path": str(src_dir),
                "original_name": target["name"],
                "skill_type": target["type"],
                "platform": platform,
                "platform_label": target.get("platform_label", ""),
                "deleted_at": datetime.datetime.now().isoformat()
            }

            shutil.move(str(src_dir), str(dest_dir))
            
            info_file = dest_dir / ".trash_meta.json"
            info_file.write_text(json.dumps(meta_info, ensure_ascii=False, indent=2), encoding="utf-8")

            return {
                "success": True,
                "message": f"技能 [{target['name']}] 已安全移至回收站，可随时还原",
                "trash_id": trash_subname
            }
        except Exception as e:
            return {"success": False, "message": f"移入回收站失败: {str(e)}"}

    def list_trash_items(self) -> List[Dict[str, Any]]:
        """获取全平台回收站列表"""
        items = []
        trash_dirs = [
            (TRASH_DIR, PLATFORM_ANTIGRAVITY),
            (CLAUDE_TRASH_DIR, PLATFORM_CLAUDE),
            (CODEX_TRASH_DIR, PLATFORM_CODEX)
        ]

        for t_dir, default_plat in trash_dirs:
            if not t_dir.exists():
                continue
            for d in sorted(t_dir.iterdir(), reverse=True):
                if d.is_dir():
                    meta_file = d / ".trash_meta.json"
                    orig_path = ""
                    orig_name = d.name
                    deleted_at = ""
                    platform = default_plat
                    platform_label = "Antigravity" if default_plat == PLATFORM_ANTIGRAVITY else ("Claude Code" if default_plat == PLATFORM_CLAUDE else "Codex")

                    if meta_file.exists():
                        try:
                            meta = json.loads(meta_file.read_text(encoding="utf-8"))
                            orig_path = meta.get("original_path", "")
                            orig_name = meta.get("original_name", orig_name)
                            deleted_at = meta.get("deleted_at", "")
                            platform = meta.get("platform", default_plat)
                            platform_label = meta.get("platform_label", platform_label)
                        except Exception:
                            pass
                    items.append({
                        "trash_id": d.name,
                        "name": orig_name,
                        "path": str(d),
                        "platform": platform,
                        "platform_label": platform_label,
                        "original_path": orig_path,
                        "deleted_at": deleted_at
                    })
        return items

    def restore_from_trash(self, trash_id: str) -> Dict[str, Any]:
        """从回收站还原技能"""
        # 在三大回收站寻找目标目录
        target_dir = None
        for t_dir in [TRASH_DIR, CLAUDE_TRASH_DIR, CODEX_TRASH_DIR]:
            cand = t_dir / trash_id
            if cand.exists():
                target_dir = cand
                break

        if not target_dir or not target_dir.exists():
            return {"success": False, "message": "回收站项不存在"}

        meta_file = target_dir / ".trash_meta.json"
        orig_path = None
        platform = PLATFORM_ANTIGRAVITY
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                orig_path = Path(meta.get("original_path"))
                platform = meta.get("platform", PLATFORM_ANTIGRAVITY)
                meta_file.unlink()  # 删除元数据文件
            except Exception:
                pass

        if not orig_path:
            if platform == PLATFORM_CLAUDE:
                orig_path = CLAUDE_GLOBAL_SKILLS_DIR / trash_id
            elif platform == PLATFORM_CODEX:
                orig_path = CODEX_GLOBAL_SKILLS_DIR / trash_id
            else:
                orig_path = GLOBAL_SKILLS_DIR / trash_id

        if orig_path.exists():
            return {"success": False, "message": f"原路径已存在同名目录: {orig_path}，无法直接还原"}

        try:
            orig_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target_dir), str(orig_path))
            return {"success": True, "message": f"技能已成功还原至: {orig_path}"}
        except Exception as e:
            return {"success": False, "message": f"还原失败: {str(e)}"}

    def purge_trash_item(self, trash_id: str) -> Dict[str, Any]:
        """彻底永久删除回收站项"""
        target_dir = None
        for t_dir in [TRASH_DIR, CLAUDE_TRASH_DIR, CODEX_TRASH_DIR]:
            cand = t_dir / trash_id
            if cand.exists():
                target_dir = cand
                break

        if not target_dir or not target_dir.exists():
            return {"success": False, "message": "回收站项不存在"}

        try:
            shutil.rmtree(target_dir, ignore_errors=True)
            return {"success": True, "message": "已从回收站彻底粉碎删除"}
        except Exception as e:
            return {"success": False, "message": f"删除失败: {str(e)}"}

    def save_original_skill(self, skill_name: str, new_content: str, skill_id: str = "") -> Dict[str, Any]:
        """保存用户编辑后的英文原始 SKILL.md 文档并写回对应物理磁盘"""
        all_skills = skill_scanner.scan_all_skills()
        target = None
        if skill_id:
            target = next((s for s in all_skills if s["id"] == skill_id), None)
        if not target:
            target = next((s for s in all_skills if s["name"].lower() == skill_name.strip().lower()), None)
            
        if not target:
            return {"success": False, "message": f"未找到技能: {skill_name}"}

        skill_dir = Path(target["path"])
        file_normal = skill_dir / "SKILL.md"
        file_disabled = skill_dir / "SKILL.md.disabled"

        target_file = file_disabled if (file_disabled.exists() and not file_normal.exists()) else file_normal

        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            stripped = new_content.strip()
            if stripped.startswith("---"):
                full_text = new_content
            else:
                existing_text = target_file.read_text(encoding="utf-8", errors="ignore") if target_file.exists() else ""
                import re
                fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", existing_text, re.DOTALL)
                if fm_match:
                    frontmatter = fm_match.group(0)
                    full_text = f"{frontmatter}\n{stripped}\n"
                else:
                    desc = target.get("description", "") or target.get("chinese_summary", "")
                    full_text = f"---\nname: {target['name']}\ndescription: >-\n  {desc}\n---\n\n{stripped}\n"

            target_file.write_text(full_text, encoding="utf-8")

            # 重新扫描更新缓存
            updated_skills = skill_scanner.scan_all_skills()
            updated_target = next((s for s in updated_skills if s["id"] == target["id"]), None)
            new_body = updated_target.get("body", stripped) if updated_target else stripped

            return {
                "success": True,
                "message": f"技能 [{skill_name}] 原文已成功写回本地文件: {target_file.name}",
                "body": new_body,
                "full_content": full_text,
                "path": str(target_file)
            }
        except Exception as e:
            return {"success": False, "message": f"保存原文失败: {str(e)}"}

    def open_skill_folder(self, identifier: str) -> Dict[str, Any]:
        """
        在操作系统资源管理器中打开技能所在文件夹，并定位高亮选中原始文件 (SKILL.md)
        """
        target_path = None
        target_file = None

        all_skills = skill_scanner.scan_all_skills()
        ident_clean = identifier.strip().lower()

        # 1. 优先在已扫描技能列表中匹配
        target = next((
            s for s in all_skills 
            if s["id"].lower() == ident_clean
            or s["name"].lower() == ident_clean
            or s.get("path", "").lower() == ident_clean
            or s.get("skill_file", "").lower() == ident_clean
        ), None)

        if target:
            target_path = Path(target["path"])
            if target.get("skill_file"):
                sf = Path(target["skill_file"])
                if sf.exists():
                    target_file = sf
        else:
            p = Path(identifier.strip())
            if p.exists():
                if p.is_file():
                    target_file = p
                    target_path = p.parent
                else:
                    target_path = p

        if not target_path or not target_path.exists():
            return {"success": False, "message": f"本地物理路径不存在: {identifier}"}

        # 2. 如果未确定具体文件，在目录中寻找首选文件
        if not target_file:
            candidates = ["SKILL.md", "skill.md", "SKILL.MD", "SKILL.md.disabled", "README.md", "readme.md"]
            for c in candidates:
                f = target_path / c
                if f.is_file():
                    target_file = f
                    break

        try:
            import sys
            opened_target = ""
            if sys.platform.startswith("win"):
                # Windows 关键修复：
                # 必须以纯字符串传递命令行，保证 /select, 在引号外，引号只包裹绝对路径
                if target_file and target_file.exists():
                    norm_file = os.path.normpath(str(target_file.resolve()))
                    cmd = f'explorer.exe /select,"{norm_file}"'
                    subprocess.Popen(cmd)
                    opened_target = norm_file
                else:
                    norm_dir = os.path.normpath(str(target_path.resolve()))
                    cmd = f'explorer.exe "{norm_dir}"'
                    subprocess.Popen(cmd)
                    opened_target = norm_dir
            elif sys.platform == "darwin":
                if target_file and target_file.exists():
                    subprocess.Popen(["open", "-R", str(target_file.resolve())])
                    opened_target = str(target_file)
                else:
                    subprocess.Popen(["open", str(target_path.resolve())])
                    opened_target = str(target_path)
            else:
                subprocess.Popen(["xdg-open", str(target_path.resolve())])
                opened_target = str(target_path)

            return {
                "success": True,
                "message": f"已唤起系统资源管理器并定位原始文件: {Path(opened_target).name}",
                "opened_path": opened_target
            }
        except Exception as e:
            return {"success": False, "message": f"打开文件夹失败: {str(e)}"}

skill_manager = SkillManager()
