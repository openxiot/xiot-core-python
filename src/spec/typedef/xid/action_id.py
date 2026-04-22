from __future__ import annotations
from typing import Optional
from .xid3 import XID3

class ActionID(XID3):
    def __init__(self,
                 string: Optional[str] = None,
                 exception: bool = False,
                 device_id: Optional[str] = None,
                 siid: Optional[int] = None,
                 aiid: Optional[int] = None):
        if string is not None:
            super().__init__(value=string, exception=exception)
        elif device_id is not None and siid is not None and aiid is not None:
            super().__init__(did=device_id, siid=siid, iid=aiid)
        else:
            super().__init__()

    @property
    def aiid(self) -> int:
        return self.iid

    @staticmethod
    def parse(value: str) -> ActionID:
        return ActionID(string=value, exception=True)