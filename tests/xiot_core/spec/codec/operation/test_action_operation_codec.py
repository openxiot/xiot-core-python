import json
import os
import pathlib
import unittest

from xiot_core.spec.codec.operation.action_operation_codec import ActionOperationCodec

class TestActionOperationCodec(unittest.TestCase):
    def test_codec(self) -> None:
        """Test ActionOperationCodec"""
        self._decode_requests("/operation/action/request")
        self._decode_results("/operation/action/response")

    def _decode_requests(self, resource: str) -> None:
        # 获取项目根目录（适配不同运行环境）
        home_path = pathlib.Path(os.getcwd())
        # 拼接resources目录路径（模拟Java的resources/spec路径）
        resource_path = home_path / "resources" / "spec" / resource.strip("/")

        # 验证路径是目录
        if not resource_path.is_dir():
            raise ValueError(f"invalid folder: {resource}")

        # 遍历目录下所有文件
        for file_path in resource_path.iterdir():
            if file_path.is_file() and file_path.suffix == ".json":
                self._decode_request(file_path)

    def _decode_request(self, file_path: pathlib.Path) -> None:
        """测试单个JSON文件的编解码一致性"""
        print(f"check: {file_path.name}")

        # 验证是文件且不是目录
        if file_path.is_dir():
            raise ValueError(f"invalid file: {file_path.name}")

        # 读取JSON文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            original_json = json.load(f)

        # 编解码测试
        operation = ActionOperationCodec.QUERY.decode(original_json['actions'])
        encoded_json = {"actions": ActionOperationCodec.QUERY.encode(operation)}

        # print("old => ", original_json)
        # print("new => ", encoded_json)

        # 断言编解码前后内容一致
        self.assertEqual(original_json, encoded_json,f"编解码不一致: {file_path.name}")

    def _decode_results(self, resource: str) -> None:
        # 获取项目根目录（适配不同运行环境）
        home_path = pathlib.Path(os.getcwd())
        # 拼接resources目录路径（模拟Java的resources/spec路径）
        resource_path = home_path / "resources" / "spec" / resource.strip("/")

        # 验证路径是目录
        if not resource_path.is_dir():
            raise ValueError(f"invalid folder: {resource}")

        # 遍历目录下所有文件
        for file_path in resource_path.iterdir():
            if file_path.is_file() and file_path.suffix == ".json":
                self._decode_result(file_path)

    def _decode_result(self, file_path: pathlib.Path) -> None:
        """测试单个JSON文件的编解码一致性"""
        print(f"check: {file_path.name}")

        # 验证是文件且不是目录
        if file_path.is_dir():
            raise ValueError(f"invalid file: {file_path.name}")

        # 读取JSON文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            original_json = json.load(f)

        # 编解码测试
        operation = ActionOperationCodec.RESULT.decode(original_json['actions'])
        encoded_json = {"actions": ActionOperationCodec.RESULT.encode(operation)}

        # print("old => ", original_json)
        # print("new => ", encoded_json)

        # 断言编解码前后内容一致
        self.assertEqual(original_json, encoded_json,f"编解码不一致: {file_path.name}")

if __name__ == "__main__":
    unittest.main()