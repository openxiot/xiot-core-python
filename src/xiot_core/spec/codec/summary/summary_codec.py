from __future__ import annotations
from typing import Optional, Dict, Any, Collection

from xiot_core.spec.typedef.summary.summary import Summary


class SummaryCodec:
    """摘要编解码器（对应Java SummaryCodec）"""

    @staticmethod
    def decode_list(list_: list[Dict[str, Any]]) -> list[Summary]:
        """解码字典列表为Summary列表"""
        array: list[Summary] = []
        for item in list_:
            o = SummaryCodec.decode_single(item)
            if o is not None:
                array.append(o)
        return array

    @staticmethod
    def decode_single(obj: Optional[Dict[str, Any]]) -> Optional[Summary]:
        """解码单个字典为Summary"""
        if obj is None:
            return None

        type_ = obj.get("type", "")
        online = False
        online_value = obj.get("online")

        if online_value is not None:
            if isinstance(online_value, int):
                online = (online_value == 1)
            elif isinstance(online_value, bool):
                online = online_value

        parent_id = obj.get("parentId", None)
        root_id = obj.get("rootId", None)
        members = SummaryCodec.from_array(obj.get("members", []))
        protocol = obj.get("protocol", None)
        cloud_id = obj.get("cloudId", None)
        last_online = obj.get("lastOnline", 0)
        last_offline = obj.get("lastOffline", 0)

        summary = Summary()
        summary.type = type_
        summary.online = online
        summary.parent_id = parent_id
        summary.root_id = root_id
        summary.members = members
        summary.protocol = protocol
        summary.cloud_id = cloud_id

        if last_online > 0:
            summary.set_last_online(last_online)

        if last_offline > 0:
            summary.set_last_offline(last_offline)

        return summary

    @staticmethod
    def decode_array(array: Optional[list]) -> list[Summary]:
        """解码列表为Summary列表"""
        list_: list[Summary] = []
        if array is not None:
            for item in array:
                if isinstance(item, dict):
                    summary = SummaryCodec.decode_single(item)
                    if summary is not None:
                        list_.append(summary)
        return list_

    @staticmethod
    def encode_single(s: Summary) -> Dict[str, Any]:
        """编码单个Summary为字典"""
        o = {}

        if s.type is not None:
            o["type"] = str(s.type)

        if s.online is not None:
            o["online"] = s.online

        if s.parent_id is not None:
            o["parentId"] = s.parent_id

        if s.root_id is not None and s.root_id:
            o["rootId"] = s.root_id

        if s.cloud_id is not None:
            o["cloudId"] = s.cloud_id

        if s.members is not None:
            if len(s.members) > 0:
                o["members"] = s.members

        if s.protocol is not None:
            o["protocol"] = s.protocol

        if s.last_online is not None:
            o["lastOnline"] = s.last_online_time

        if s.last_offline is not None:
            o["lastOffline"] = s.last_offline_time

        return o

    @staticmethod
    def encode_collection(list_: Collection[Summary]) -> list:
        """编码Summary集合为列表"""
        return [SummaryCodec.encode_single(item) for item in list_]

    @staticmethod
    def from_array(array: Optional[list]) -> list[str]:
        """从列表解析字符串列表"""
        list_ = []
        if array is not None:
            for o in array:
                if isinstance(o, str):
                    list_.append(o)
        return list_

    @staticmethod
    def to_array(list_: list[str]) -> list:
        """字符串列表转为普通列表"""
        return list(list_)