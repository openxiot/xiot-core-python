from __future__ import annotations

from typing import Optional

class ServiceID:
    def __init__(self,
                 value: Optional[str] = None,
                 exception: bool = False,
                 device_id: Optional[str] = None,
                 siid: Optional[int] = None):
        self._did: str = ""
        self._siid: int = 0
        self._valid: bool = True

        if value is not None:
            self._init_from_value(value, exception)
        elif device_id is not None and siid is not None:
            self._did = device_id
            self._siid = siid

    def _init_from_value(self, value: str, exception: bool) -> None:
        if value is None:
            self._fail("value is null", exception)
            return

        id_parts = value.split(".")
        if len(id_parts) != 2:
            self._fail(f"value invalid: {value}", exception)
            return

        self._did = id_parts[0]
        try:
            self._siid = int(id_parts[1])
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

    def did(self, did: str) -> ServiceID:
        self._did = did
        return self

    @property
    def did_value(self) -> str:
        return self._did

    @property
    def siid(self) -> int:
        return self._siid

    def __str__(self) -> str:
        if self._valid:
            return f"{self._did}.{self._siid}"
        return ""

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, ServiceID):
            return False
        return (self._siid == other._siid and
                self._valid == other._valid and
                self._did == other._did)

    def __hash__(self) -> int:
        return hash((self._valid, self._did, self._siid))

    @staticmethod
    def parse(value: str) -> ServiceID:
        return ServiceID(value=value, exception=True)