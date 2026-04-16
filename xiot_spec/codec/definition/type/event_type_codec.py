from typing import Optional

from xiot_spec.codec.java.json_array import JsonArray
from xiot_spec.typedef.definition.urn.event_type import EventType


class EventTypeCodec:
    """严格对齐 Java 版 EventTypeCodec 逻辑"""
    # 私有构造函数（模拟Java的private构造）
    def __init__(self):
        raise NotImplementedError("该类不允许实例化")

    @staticmethod
    def decode(array: Optional[JsonArray]) -> Optional[list[EventType]]:
        if array is None:
            return None
        # 严格对齐Java stream -> filter -> map -> collect 逻辑
        result = []
        for x in array.stream():
            if isinstance(x, str):
                result.append(EventType.parse(x))
        return result

    @staticmethod
    def encode(list_: Optional[list[EventType]]) -> Optional[JsonArray]:
        if list_ is None:
            return None
        # 模拟Java: new JsonArray(list.stream().map(Urn::toString).collect(Collectors.tolist()))
        str_list = [str(urn) for urn in list_]
        return JsonArray(str_list)