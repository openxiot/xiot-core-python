import unittest
from xiot_spec.typedef.definition.urn.action_type import ActionType


class TestActionTypeParse(unittest.TestCase):
    """
    测试 ActionType.parse() 方法：
    字符串 → 解析 → 转回字符串 → 必须完全一致
    """

    def test_parse_and_to_string_should_match(self):
        # 测试用例：你可以随便加更多
        test_urn_strings = [
            "urn:homekit-spec:action:fan:00000001",
            "urn:miot-spec:action:light:00000002:modified:1",
            "urn:xiot:action:door:00000003:org:model:2",
        ]

        for urn_str in test_urn_strings:
            # 1. 解析
            action_type = ActionType.parse(urn_str)

            # 2. 转回字符串
            result_str = str(action_type)

            # 3. 断言必须相等
            self.assertEqual(
                urn_str,
                result_str,
                f"解析前后字符串不一致\n输入: {urn_str}\n输出: {result_str}"
            )


if __name__ == '__main__':
    unittest.main()