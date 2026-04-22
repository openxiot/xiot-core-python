from typing import Optional

from xiot_core.spec.typedef.definition.urn.property_type import PropertyType


class PropertyTypeCodec:
    """严格对齐 Java 版 PropertyTypeCodec 逻辑"""
    def __init__(self):
        raise NotImplementedError("该类不允许实例化")

    @staticmethod
    def decode(array: Optional[list[ str]]) -> Optional[list[PropertyType]]:
        if array is None:
            return None
        result = []
        for x in array:
            if isinstance(x, str):
                result.append(PropertyType.parse(x))
        return result

    @staticmethod
    def encode(list_: Optional[list[PropertyType]]) -> Optional[list[str]]:
        if list_ is None:
            return None
        str_list = [str(urn) for urn in list_]
        return str_list