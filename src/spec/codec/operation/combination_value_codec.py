from __future__ import annotations

from typing import Dict, Optional, Any


class CombinationValueCodec:
    """组合值编解码器（对应Java CombinationValueCodec）"""

    @staticmethod
    def decode_array(array: Optional[list]) -> Optional[Dict[int, Any]]:
        """解码列表为组合值字典"""
        members: Dict[int, Any] = {}
        if array is None:
            return members

        for item in array:
            if not isinstance(item, dict):
                return None  # 非对象则无效，返回null

            piid = item.get("piid", 0)
            value = item.get("value")

            if piid is None or value is None:
                return None  # piid/value缺失则无效

            # 嵌套解析
            if isinstance(value, list):
                value = CombinationValueCodec.decode_array(value)
            elif isinstance(value, dict):
                value = CombinationValueCodec.decode_dict(value)

            members[piid] = value

        return members

    @staticmethod
    def decode_dict(obj: Dict[str, Any]) -> Dict[int, Any]:
        """解码字典为组合值字典"""
        members: Dict[int, Any] = {}
        for k, v in obj.items():
            if k.startswith("#"):
                piid_str = k[1:]
                piid = int(piid_str)

                # 嵌套解析
                if isinstance(v, dict):
                    v = CombinationValueCodec.decode_dict(v)
                elif isinstance(v, list):
                    v = CombinationValueCodec.decode_array(v)

                members[piid] = v
        return members

    @staticmethod
    def encode(members: Dict[int, Any]) -> list | dict:
        """编码组合值（默认非紧凑模式）"""
        return CombinationValueCodec.encode_compact(False, members)

    @staticmethod
    def encode_compact(compact: bool, members: Dict[Any, Any]) -> list | dict:
        """编码组合值（支持紧凑/非紧凑模式）"""
        if compact:
            o: Dict[str, Any] = {}
            for k, v in members.items():
                # 嵌套编码
                if isinstance(v, dict):
                    v = CombinationValueCodec.encode_compact(compact, v)
                o[f"#{k}"] = v
            return o
        else:
            array = []
            for k, v in members.items():
                # 嵌套编码
                if isinstance(v, dict):
                    v = CombinationValueCodec.encode_compact(compact, v)
                array.append({"piid": k, "value": v})
            return array