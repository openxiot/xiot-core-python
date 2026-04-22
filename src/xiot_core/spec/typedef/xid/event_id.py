from __future__ import annotations
from typing import Optional
from .xid3 import XID3

class EventID(XID3):
    def __init__(self,
                 string: Optional[str] = None,
                 exception: bool = False,
                 device_id: Optional[str] = None,
                 siid: Optional[int] = None,
                 eiid: Optional[int] = None):
        # 处理构造参数
        if string is not None:
            super().__init__(value=string, exception=exception)
        elif device_id is not None and siid is not None and eiid is not None:
            super().__init__(did=device_id, siid=siid, iid=eiid)
        else:
            super().__init__()

    @property
    def eiid(self) -> int:
        return self.iid

    @staticmethod
    def parse(value: str) -> EventID:
        return EventID(string=value, exception=True)

    # 兼容Java风格的构造
    @classmethod
    def from_parts(cls, did: str, siid: int, eiid: int) -> EventID:
        return cls(device_id=did, siid=siid, eiid=eiid)