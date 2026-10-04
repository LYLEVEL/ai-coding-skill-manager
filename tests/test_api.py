# -*- coding: utf-8 -*-
"""
API 端点集成测试
"""

import sys
import unittest
from pathlib import Path
from starlette.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.server import app

class TestServerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_root_and_static(self):
        """测试静态主页加载"""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Antigravity Skill Manager", res.text)

    def test_02_get_skills_api(self):
        """测试获取技能列表 API"""
        res = self.client.get("/api/skills")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertGreater(data["total"], 10)
        
        # 验证返回字段结构
        first = data["data"][0]
        self.assertIn("chinese_summary", first)
        self.assertIn("is_enabled", first)
        self.assertIn("call_count", first)
        self.assertIn("session_hit_rate", first)

    def test_03_stats_overview_api(self):
        """测试概览统计 API"""
        res = self.client.get("/api/stats/overview")
        self.assertEqual(res.status_code, 200)
        json_data = res.json()
        self.assertTrue(json_data["success"])
        info = json_data["data"]
        self.assertGreater(info["total_skills"], 0)
        self.assertGreater(info["enabled_count"], 0)

    def test_04_metadata_update_api(self):
        """测试中文概要自定义更新 API"""
        payload = {
            "name": "brainstorming",
            "summary": "【自定义】头脑风暴与需求探索专用技能",
            "category": "需求与规划",
            "tags": ["头脑风暴", "自定义测试"]
        }
        res = self.client.post("/api/skills/metadata", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["success"])

        # 重新拉取验证已覆盖生效
        skills_res = self.client.get("/api/skills")
        target = next(s for s in skills_res.json()["data"] if s["name"] == "brainstorming")
        self.assertEqual(target["chinese_summary"], payload["summary"])

if __name__ == "__main__":
    unittest.main()
