from __future__ import annotations
from typing import Optional

class XID3:
    def __init__(self,
                 did: Optional[str] = None,
                 siid: Optional[int] = None,
                 iid: Optional[int] = None,
                 value: Optional[str] = None,
                 exception: bool = False):
        self._did: str = ""
        self._siid: int = 0
        self._iid: int = 0
        self._valid: bool = True

        # 处理不同构造参数组合
        if value is not None:
            self._init_from_value(value, exception)
        elif did is not None and siid is not None and iid is not None:
            self._did = did
            self._siid = siid
            self._iid = iid

    def _init_from_value(self, value: str, exception: bool) -> None:
        if value is None:
            self._fail("value is null", exception)
            return

        id_parts = value.split(".")
        if len(id_parts) != 3:
            self._fail(f"value invalid: {value}", exception)
            return

        self._did = id_parts[0]
        try:
            self._siid = int(id_parts[1])
            self._iid = int(id_parts[2])
        except ValueError as e:
            self._fail(f"value invalid: {e}", exception)

    def _fail(self, msg: str, exception: bool) -> None:
        if exception:
            raise ValueError(msg)
        self._valid = False

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def invalid(self) -> bool:
        return not self._valid

    @property
    def did(self) -> str:  # 避免与方法名冲突，加后缀
        return self._did

    @did.setter
    def did(self, did: str):
        self._did = did

    @property
    def siid(self) -> int:
        return self._siid

    @property
    def iid(self) -> int:
        return self._iid

    def __str__(self) -> str:
        if self.invalid:
            return ""
        return f"{self._did}.{self._siid}.{self._iid}"

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, XID3):
            return False
        return (self._siid == other._siid and
                self._iid == other._iid and
                self._valid == other._valid and
                self._did == other._did)

    def __hash__(self) -> int:
        return hash((self._valid, self._did, self._siid, self._iid))