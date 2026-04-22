from typing import Optional

from .urn import Urn
from .urn_type import UrnType

class EventType(Urn):
    """Event类型的URN实现"""

    def __init__(
        self,
        ns: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[int | str] = None,
        string: Optional[str] = None,
        exception: bool = False
    ):
        # 重载构造逻辑
        if ns is not None and name is not None and value is not None:
            super().__init__(ns=ns, type_=UrnType.EVENT, name=name, value=value)
        elif string is not None:
            super().__init__(t=UrnType.EVENT, string=string, exception=exception)
        else:
            super().__init__()

    @staticmethod
    def parse(string: str) -> "EventType":
        """解析字符串为EventType（抛异常）"""
        return EventType(string=string, exception=True)