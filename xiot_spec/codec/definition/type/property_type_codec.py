from typing import Optional

from xiot_spec.codec.java.json_array import JsonArray
from xiot_spec.typedef.definition.urn.property_type import PropertyType


class PropertyTypeCodec:
    """严格对齐 Java 版 PropertyTypeCodec 逻辑"""
    def __init__(self):
        raise NotImplementedError("该类不允许实例化")

    @staticmethod
    def decode(array: Optional[JsonArray]) -> Optional[list[PropertyType]]:
        if array is None:
            return None
        result = []
        for x in array.stream():
            if isinstance(x, str):
                result.append(PropertyType.parse(x))
        return result

    @staticmethod
    def encode(list_: Optional[list[PropertyType]]) -> Optional[JsonArray]:
        if list_ is None:
            return None
        str_list = [str(urn) for urn in list_]
        return JsonArray(str_list)