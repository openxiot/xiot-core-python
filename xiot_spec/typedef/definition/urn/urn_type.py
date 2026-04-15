from enum import Enum


class UrnType(Enum):
    """URN 类型枚举"""
    UNDEFINED = "undefined"
    PROPERTY = "property"
    ACTION = "action"
    EVENT = "event"
    SERVICE = "service"
    DEVICE = "device"
    GROUP = "group"
    FORMAT = "format"
    UNIT = "unit"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_string(s: str) -> "UrnType":
        """从字符串转换为UrnType枚举"""
        if s is None:
            return UrnType.UNDEFINED
        for t in UrnType:
            if t.value == s:
                return t
        return UrnType.UNDEFINED