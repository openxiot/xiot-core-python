from __future__ import annotations
from typing import Optional, Any

class Shadow:
    def __init__(self,
                 did: str,
                 siid: int,
                 piid: int,
                 value: Any):
        self._did: str = did
        self._siid: int = siid
        self._piid: int = piid
        self._value: Any = value
        self._status: int = 0
        self._description: Optional[str] = None

    # 简化构造（无did）
    @classmethod
    def from_siid_piid_value(cls, siid: int, piid: int, value: Any) -> Shadow:
        return cls("", siid, piid, value)

    @property
    def did(self) -> str:
        return self._did

    @did.setter
    def did(self, did: str):
        self._did = did

    @property
    def siid(self) -> int:
        return self._siid

    @siid.setter
    def siid(self, siid: int):
        self._siid = siid

    @property
    def piid(self) -> int:
        return self._piid

    @piid.setter
    def piid(self, piid: int):
        self._piid = piid
        return self

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, status: int):
        self._status = status

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description