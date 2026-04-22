#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目根目录统一启动单元测试的脚本
Python 3.10+
"""

import unittest
import sys

def run_all_tests() -> None:
    """批量运行所有 codec 单元测试"""
    # 测试模块路径

    test_modules = [
        "tests.xiot_core.spec.codec.definition.test_action_definition_codec",
        "tests.xiot_core.spec.codec.definition.test_event_definition_codec",
        "tests.xiot_core.spec.codec.definition.test_property_definition_codec",
        "tests.xiot_core.spec.codec.definition.test_service_definition_codec",
        "tests.xiot_core.spec.codec.instance.test_device_instance_codec",
        "tests.xiot_core.spec.codec.operation.test_action_operation_codec",
        "tests.xiot_core.spec.codec.operation.test_event_operation_codec",
        "tests.xiot_core.spec.codec.operation.test_property_operation_codec",
        "tests.xiot_core.spec.codec.shadow.test_shadow_codec",
        "tests.xiot_core.spec.codec.summary.test_summary_codec",
        "tests.xiot_core.spec.typedef.definition.type.test_action_type"
    ]

    # 加载所有测试
    suite = unittest.TestSuite()
    for module in test_modules:
        try:
            # 导入测试模块
            test_mod = __import__(module, fromlist=[""])
            # 加载测试用例
            loader = unittest.TestLoader()
            suite.addTests(loader.loadTestsFromModule(test_mod))
        except Exception as e:
            print(f"加载测试 {module} 失败: {e}", file=sys.stderr)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 退出码（CI/CD 可用）
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    run_all_tests()