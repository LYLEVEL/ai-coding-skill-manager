# -*- coding: utf-8 -*-
"""
自动化测试与功能验证套件
"""

import sys
import unittest
from pathlib import Path

# 确保能导入 backend
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.scanner import skill_scanner
from backend.telemetry import telemetry_analyzer
from backend.manager import skill_manager
from backend.config import GLOBAL_SKILLS_DIR, TRASH_DIR

class TestSkillManager(unittest.TestCase):
    def setUp(self):
        self.test_skill_name = "test-demo-verify-skill"
        self.test_skill_dir = GLOBAL_SKILLS_DIR / self.test_skill_name

    def tearDown(self):
        # 清理可能残留的测试目录
        if self.test_skill_dir.exists():
            import shutil
            shutil.rmtree(self.test_skill_dir, ignore_errors=True)

    def test_01_scanner_and_telemetry(self):
        """测试技能发现与调用率日志分析"""
        tele_res = telemetry_analyzer.scan_brain_logs(force_full=False)
        self.assertGreater(tele_res["total_sessions"], 0, "Brain 历史会话数应大于 0")
        
        skills = skill_scanner.scan_all_skills()
        self.assertGreater(len(skills), 10, "本地扫描出的技能数应大于 10")
        
        # 验证是否包含中文概要
        sample = next(s for s in skills if s["name"] == "brainstorming")
        self.assertTrue(len(sample["chinese_summary"]) > 0, "应具有中文功能概要")
        self.assertEqual(sample["type"], "global")

    def test_02_create_toggle_trash_lifecycle(self):
        """测试技能的新建、禁用、启用、回收站、还原与彻底删除完整生命周期"""
        # 1. 新建
        create_res = skill_manager.create_skill(
            name=self.test_skill_name,
            description="A test skill for verification",
            chinese_summary="测试验证技能：用于验证自动化生命周期管理",
            category="自动化测试",
            tags=["测试", "CI"],
            content="# 测试技能\n\n测试正文内容",
            target_type="global"
        )
        self.assertTrue(create_res["success"], f"新建失败: {create_res.get('message')}")
        self.assertTrue((self.test_skill_dir / "SKILL.md").exists(), "SKILL.md 应该存在")

        skill_id = f"global:{self.test_skill_name}"

        # 2. 禁用
        toggle_res = skill_manager.toggle_skill_status(skill_id, enable=False)
        self.assertTrue(toggle_res["success"])
        self.assertFalse(toggle_res["is_enabled"])
        self.assertTrue((self.test_skill_dir / "SKILL.md.disabled").exists(), "文件应被重命名为 SKILL.md.disabled")
        self.assertFalse((self.test_skill_dir / "SKILL.md").exists(), "原 SKILL.md 不应存在")

        # 3. 启用
        toggle_res2 = skill_manager.toggle_skill_status(skill_id, enable=True)
        self.assertTrue(toggle_res2["success"])
        self.assertTrue(toggle_res2["is_enabled"])
        self.assertTrue((self.test_skill_dir / "SKILL.md").exists(), "SKILL.md 应该恢复")
        self.assertFalse((self.test_skill_dir / "SKILL.md.disabled").exists())

        # 4. 移入回收站
        del_res = skill_manager.delete_skill_to_trash(skill_id)
        self.assertTrue(del_res["success"])
        trash_id = del_res["trash_id"]
        self.assertFalse(self.test_skill_dir.exists(), "原技能目录应已被移动")
        
        # 5. 回收站中检查
        trash_items = skill_manager.list_trash_items()
        self.assertTrue(any(item["trash_id"] == trash_id for item in trash_items))

        # 6. 从回收站还原
        restore_res = skill_manager.restore_from_trash(trash_id)
        self.assertTrue(restore_res["success"])
        self.assertTrue(self.test_skill_dir.exists(), "还原后原技能目录应恢复")

        # 7. 再次移入回收站并彻底删除
        del_res2 = skill_manager.delete_skill_to_trash(skill_id)
        self.assertTrue(del_res2["success"])
        trash_id2 = del_res2["trash_id"]

        purge_res = skill_manager.purge_trash_item(trash_id2)
        self.assertTrue(purge_res["success"])
        self.assertFalse((TRASH_DIR / trash_id2).exists(), "回收站项应被彻底物理删除")

if __name__ == "__main__":
    unittest.main()
