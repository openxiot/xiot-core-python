from typing import Optional

from xiot_core.spec.typedef.definition.urn.service_type import ServiceType


class ServiceTypeCodec:
    """严格对齐 Java 版 ServiceTypeCodec 逻辑"""
    def __init__(self):
        raise NotImplementedError("该类不允许实例化")

    @staticmethod
    def decode(array: Optional[list[str]]) -> Optional[list[ServiceType]]:
        if array is None:
            return None
        result = []
        for x in array:
            if isinstance(x, str):
                result.append(ServiceType.parse(x))
        return result

    @staticmethod
    def encode(list_: Optional[list[ServiceType]]) -> Optional[list[str]]:
        if list_ is None:
            return None
        str_list = [str(urn) for urn in list_]
        return str_list