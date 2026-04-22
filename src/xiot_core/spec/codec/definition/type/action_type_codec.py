from typing import Optional

from xiot_core.spec.typedef.definition.urn.action_type import ActionType


class ActionTypeCodec:
    """严格对齐 Java 版 ActionTypeCodec 逻辑"""
    def __init__(self):
        raise NotImplementedError("该类不允许实例化")

    @staticmethod
    def decode(array: Optional[list[str]]) -> Optional[list[ActionType]]:
        if array is None:
            return None
        result = []
        for x in array:
            if isinstance(x, str):
                result.append(ActionType.parse(x))
        return result

    @staticmethod
    def encode(list_: Optional[list[ActionType]]) -> Optional[list[str]]:
        if list_ is None:
            return None
        str_list = [str(urn) for urn in list_]
        return str_list