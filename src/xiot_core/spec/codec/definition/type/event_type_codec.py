from typing import Optional

from xiot_core.spec.typedef.definition.urn.event_type import EventType


class EventTypeCodec:
    """严格对齐 Java 版 EventTypeCodec 逻辑"""
    # 私有构造函数（模拟Java的private构造）
    def __init__(self):
        raise NotImplementedError("该类不允许实例化")

    @staticmethod
    def decode(array: Optional[list[str]]) -> Optional[list[EventType]]:
        if array is None:
            return None
        result = []
        for x in array:
            if isinstance(x, str):
                result.append(EventType.parse(x))
        return result

    @staticmethod
    def encode(list_: Optional[list[EventType]]) -> Optional[list[str]]:
        if list_ is None:
            return None
        str_list = [str(urn) for urn in list_]
        return str_list