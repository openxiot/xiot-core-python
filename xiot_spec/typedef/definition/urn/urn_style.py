from enum import Enum


class UrnStyle(Enum):
    """URN 样式枚举"""
    SPEC = "SPEC"
    V1 = "V1"
    V2 = "V2"
    V2_TEMPLATE = "V2_TEMPLATE"
    XIOT = "XIOT"