from __future__ import annotations
from typing import Optional
from .xid3 import XID3

class PropertyID(XID3):
    def __init__(self,
                 string: Optional[str] = None,
                 exception: bool = False,
                 device_id: Optional[str] = None,
                 siid: Optional[int] = None,
                 piid: Optional[int] = None):
        if string is not None:
            super().__init__(value=string, exception=exception)
        elif device_id is not None and siid is not None and piid is not None:
            super().__init__(did=device_id, siid=siid, iid=piid)
        else:
            super().__init__()

    @property
    def piid(self) -> int:
        return self.iid

    @staticmethod
    def parse(value: str) -> PropertyID:
        return PropertyID(string=value, exception=True)