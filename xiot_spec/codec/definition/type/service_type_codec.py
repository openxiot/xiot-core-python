from typing import Optional

from xiot_spec.codec.java.json_array import JsonArray
from xiot_spec.typedef.definition.urn.service_type import ServiceType


class ServiceTypeCodec:
    """严格对齐 Java 版 ServiceTypeCodec 逻辑"""
    def __init__(self):
        raise NotImplementedError("该类不允许实例化")

    @staticmethod
    def decode(array: Optional[JsonArray]) -> Optional[list[ServiceType]]:
        if array is None:
            return None
        result = []
        for x in array.stream():
            if isinstance(x, str):
                result.append(ServiceType.parse(x))
        return result

    @staticmethod
    def encode(list_: Optional[list[ServiceType]]) -> Optional[JsonArray]:
        if list_ is None:
            return None
        str_list = [str(urn) for urn in list_]
        return JsonArray(str_list)