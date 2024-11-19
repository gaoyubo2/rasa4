import unittest
import os

from component.config_loader import load_process_params_config, get_required_params


class TestProcessConfig(unittest.TestCase):

    def setUp(self):
        """在每个测试前运行，确保测试环境的准备工作"""
        self.config = load_process_params_config()

    def test_load_process_params_config(self):
        """测试配置文件加载功能"""
        # 确保加载的配置文件不是空的
        self.assertTrue(bool(self.config), "配置文件加载失败")

        # 确保包含 'sub_process_types' 键
        self.assertIn("sub_process_types", self.config, "'sub_process_types' 不在配置中")

    def test_get_required_params(self):
        """测试获取子工艺类型所需参数的功能"""
        # 测试不同的子工艺类型
        required_params_outer_circle = get_required_params("外圆", self.config)
        self.assertEqual(required_params_outer_circle, ["Cn", "L", "Tr", "Cr", "F"], "外圆所需参数不匹配")

        required_params_outer_cone = get_required_params("外锥面", self.config)
        self.assertEqual(required_params_outer_cone, ["R", "Tr", "Cn", "F", "G2G3", "PHi1", "L"],
                         "外锥面所需参数不匹配")

        required_params_outer_arc = get_required_params("外圆弧", self.config)
        self.assertEqual(required_params_outer_arc, ["Cn", "L", "Tr", "A", "F", "xDir", "zDir", "G71G73"],
                         "外圆弧所需参数不匹配")

    def test_get_required_params_with_invalid_type(self):
        """测试传入无效子工艺类型时的处理"""
        # 测试一个无效的子工艺类型
        required_params_invalid = get_required_params("无效工艺", self.config)
        self.assertEqual(required_params_invalid, [], "无效的子工艺类型应该返回空列表")


if __name__ == "__main__":
    unittest.main()
