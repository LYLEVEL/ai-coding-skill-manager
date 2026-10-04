# -*- coding: utf-8 -*-
"""
FastAPI 后端服务入口与 API 路由
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import APP_ROOT, SUPPORTED_PLATFORMS, PLATFORM_ANTIGRAVITY
from .scanner import skill_scanner
from .telemetry import telemetry_analyzer
from .manager import skill_manager
from .doc_translator import doc_translator

app = FastAPI(title="AI Coding Skill Manager", version="2.0.0")

# 启用 CORS 跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局兜底异常处理器，确保所有非预期错误始终以 JSON 返回，避免前端解析出现 Unexpected token"""
    import traceback
    tb = traceback.format_exc()
    print(f"[API ERROR] {request.method} {request.url.path}: {exc}\n{tb}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"服务器内部处理异常: {str(exc)}",
            "detail": str(exc)
        }
    )

# 请求模型定义
class ToggleRequest(BaseModel):
    skill_id: str
    enable: Optional[bool] = None

class CreateSkillRequest(BaseModel):
    name: str
    description: str = ""
    chinese_summary: str = ""
    category: str = "实用工具"
    tags: List[str] = []
    content: str = ""
    target_type: str = "global"
    platform: str = "antigravity"

class DeleteRequest(BaseModel):
    skill_id: str

class TrashActionRequest(BaseModel):
    trash_id: str

class MetaUpdateRequest(BaseModel):
    name: str
    summary: str
    category: str = ""
    tags: List[str] = []

class GitImportRequest(BaseModel):
    repo_url: str
    custom_name: str = ""
    platform: str = "antigravity"
    target_type: str = "global"

class TranslateRequest(BaseModel):
    skill_name: str
    force: bool = False

class SaveDocRequest(BaseModel):
    skill_name: str
    content: str
    skill_id: str = ""

class OpenFolderRequest(BaseModel):
    path: str = ""
    skill_name: str = ""

# API 接口路由
@app.get("/api/skills")
async def get_skills(workspace_path: Optional[str] = None):
    """获取所有技能列表"""
    skills = skill_scanner.scan_all_skills(workspace_path)
    return {"success": True, "data": skills, "total": len(skills)}

@app.get("/api/platforms")
async def get_platforms():
    """获取所有受支持的 AI Coding 平台生态及技能数量分布"""
    skills = skill_scanner.scan_all_skills()
    from collections import Counter
    counts = Counter(s.get("platform", "antigravity") for s in skills)
    enabled_counts = Counter(s.get("platform", "antigravity") for s in skills if s.get("is_enabled"))

    platforms = []
    for p in SUPPORTED_PLATFORMS:
        pid = p["id"]
        total = counts[pid]
        enabled = enabled_counts[pid]
        platforms.append({
            **p,
            "total": total,
            "enabled": enabled,
            "disabled": total - enabled
        })
    return {
        "success": True,
        "platforms": platforms,
        "total_all": len(skills),
        "enabled_all": sum(1 for s in skills if s.get("is_enabled"))
    }

@app.post("/api/scan")
async def scan_skills(force_full: bool = False):
    """触发全量/增量日志统计与目录重新扫描"""
    tele_res = telemetry_analyzer.scan_brain_logs(force_full=force_full)
    skills = skill_scanner.scan_all_skills()
    return {
        "success": True,
        "telemetry": tele_res,
        "skills": skills,
        "total": len(skills)
    }

@app.get("/api/stats/overview")
async def get_overview_stats():
    """获取仪表盘概览统计指标"""
    skills = skill_scanner.scan_all_skills()
    total = len(skills)
    enabled_count = sum(1 for s in skills if s["is_enabled"])
    disabled_count = total - enabled_count

    type_counts = {}
    platform_counts = {}
    for s in skills:
        t = s["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
        p = s.get("platform", "antigravity")
        platform_counts[p] = platform_counts.get(p, 0) + 1

    total_calls = sum(s["call_count"] for s in skills)
    top_skills = sorted(skills, key=lambda x: x["call_count"], reverse=True)[:6]

    return {
        "success": True,
        "data": {
            "total_skills": total,
            "enabled_count": enabled_count,
            "disabled_count": disabled_count,
            "total_calls": total_calls,
            "type_counts": type_counts,
            "platform_counts": platform_counts,
            "top_skills": top_skills,
            "brain_sessions": telemetry_analyzer.cache.get("total_sessions", 0)
        }
    }

@app.post("/api/skills/toggle")
async def toggle_skill(payload: ToggleRequest):
    """切换技能的启用/禁用状态"""
    result = skill_manager.toggle_skill_status(payload.skill_id, payload.enable)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/api/skills/create")
async def create_skill(payload: CreateSkillRequest):
    """新建自定义技能"""
    result = skill_manager.create_skill(
        name=payload.name,
        description=payload.description,
        chinese_summary=payload.chinese_summary,
        category=payload.category,
        tags=payload.tags,
        content=payload.content,
        target_type=payload.target_type,
        platform=payload.platform
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/api/skills/delete")
async def delete_skill(payload: DeleteRequest):
    """移入回收站"""
    result = skill_manager.delete_skill_to_trash(payload.skill_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/api/trash")
async def get_trash():
    """查看回收站列表"""
    items = skill_manager.list_trash_items()
    return {"success": True, "data": items}

@app.post("/api/trash/restore")
async def restore_trash(payload: TrashActionRequest):
    """从回收站还原"""
    result = skill_manager.restore_from_trash(payload.trash_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/api/trash/purge")
async def purge_trash(payload: TrashActionRequest):
    """彻底删除回收站项目"""
    result = skill_manager.purge_trash_item(payload.trash_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/api/skills/metadata")
async def update_metadata(payload: MetaUpdateRequest):
    """保存中文概要和标签覆盖"""
    skill_scanner.update_custom_metadata(
        skill_name=payload.name,
        summary=payload.summary,
        category=payload.category,
        tags=payload.tags
    )
    return {"success": True, "message": "中文概要与元数据已更新"}

@app.post("/api/skills/import-git")
async def import_git(payload: GitImportRequest):
    """从 Git 导入技能"""
    result = skill_manager.import_from_git(
        repo_url=payload.repo_url,
        custom_name=payload.custom_name,
        platform=payload.platform,
        target_type=payload.target_type
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

import anyio

@app.post("/api/skills/translate")
async def translate_skill_doc(payload: TranslateRequest):
    """获取或即时自动翻译指定技能的 Markdown 详细指南"""
    name = payload.skill_name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="技能名称不能为空")

    # 1. 检查本地是否有缓存
    if not payload.force:
        cached = doc_translator.get_cached_translation(name)
        if cached:
            return {"success": True, "chinese_body": cached, "from_cache": True}

    # 2. 获取技能原始 body
    skills = skill_scanner.scan_all_skills()
    target = next((s for s in skills if s["name"].lower() == name.lower()), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"未找到技能: {name}")

    orig_body = target.get("body", "")
    if not orig_body:
        return {"success": True, "chinese_body": "（该技能暂无指南正文）", "from_cache": False}

    # 3. 异步线程执行智能翻译与缓存，绝不阻塞 Web 服务事件循环
    translated_md = await anyio.to_thread.run_sync(
        doc_translator.translate_markdown, orig_body, target["name"]
    )
    return {
        "success": True,
        "chinese_body": translated_md,
        "from_cache": False
    }

@app.post("/api/skills/save-doc-translation")
async def save_doc_translation(payload: SaveDocRequest):
    """保存用户编辑后的中文使用指南"""
    name = payload.skill_name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="技能名称不能为空")
    doc_translator.save_translation(name, payload.content)
    return {"success": True, "message": f"技能 [{name}] 的中文使用指南已成功保存！"}

@app.post("/api/skills/save-original-doc")
async def save_original_doc(payload: SaveDocRequest):
    """保存用户编辑后的英文原始 SKILL.md 文档"""
    name = payload.skill_name.strip()
    if not name and not payload.skill_id:
        raise HTTPException(status_code=400, detail="技能名称不能为空")
    result = skill_manager.save_original_skill(name, payload.content, skill_id=payload.skill_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/api/skills/open-folder")
async def open_folder(payload: OpenFolderRequest):
    """在操作系统文件资源管理器中打开并定位原始文件"""
    ident = payload.path.strip() or payload.skill_name.strip()
    if not ident:
        raise HTTPException(status_code=400, detail="路径或技能名不能为空")
    result = skill_manager.open_skill_folder(ident)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.post("/api/app/exit")
async def exit_app():
    """安全退出整个后端应用进程"""
    def do_exit():
        time.sleep(0.4)
        os._exit(0)
    import threading
    import time
    threading.Thread(target=do_exit, daemon=True).start()
    return {"success": True, "message": "服务已安全退出"}

# 静态资源托管
STATIC_DIR = APP_ROOT / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "AI Coding Skill Manager 后端已就绪，正在准备前端..."}
