from __future__ import annotations
from typing import Optional, Any

from xiot_spec.typedef.operation.abstract_operation import AbstractOperation
from xiot_spec.typedef.status.status import Status
from xiot_spec.typedef.xid.property_id import PropertyID


class PropertyOperation(AbstractOperation):
    def __init__(self,
                 pid: Optional[PropertyID | str] = None,
                 did: Optional[str] = None,
                 siid: Optional[int] = None,
                 piid: Optional[int] = None,
                 value: Optional[Any] = None,
                 status: Optional[int] = None,
                 description: Optional[str] = None):
        super().__init__()
        self._pid: Optional[PropertyID] = None
        self._value: Optional[Any] = None
        self._arguments_compact: bool = False

        # 处理构造参数
        if status is not None and description is not None:
            super().__init__(status, description)

        # 初始化pid
        if isinstance(pid, str):
            self._pid = PropertyID(string=pid)
        elif isinstance(pid, PropertyID):
            self._pid = pid
        elif did and siid and piid:
            self._pid = PropertyID(device_id=did, siid=siid, piid=piid)

        # 初始化value
        if value is not None:
            self._value = value

        # 校验pid有效性
        if self._pid and self._pid.invalid:
            self.status = Status.PID_INVALID

    @property
    def did(self) -> str:
        return self._pid.did if self._pid else ""

    @did.setter
    def did(self, did: str):
        if self._pid:
            self._pid.did = did

    @property
    def siid(self) -> int:
        return self._pid.siid if self._pid else 0

    @property
    def iid(self) -> int:
        return self._pid.iid if self._pid else 0

    @property
    def pid(self) -> Optional[PropertyID]:
        return self._pid

    @property
    def value(self) -> Optional[Any]:
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    def set_value_multi(self, *value: Any) -> PropertyOperation:
        self._value = list(value)
        return self

    @property
    def arguments_compact(self) -> bool:
        return self._arguments_compact

    def set_arguments_compact(self, arguments_compact: bool) -> PropertyOperation:
        self._arguments_compact = arguments_compact
        return self

    def to_string(self, pretty: bool, tab: bool) -> str:
        b = []
        if tab:
            b.append("    ")

        if self._pid:
            b.append(str(self._pid))
        b.append(" => ")

        if isinstance(self._value, str):
            b.append(f'"{self._value}"')
        elif self._value is not None:
            b.append(str(self._value))
        else:
            b.append("null")

        b.append(";")
        return "".join(b)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, PropertyOperation):
            return False
        if not super().__eq__(other):
            return False
        return (self._pid == other._pid and
                self._value == other._value)

    def __hash__(self) -> int:
        return hash((self._pid, self._value))

    def __str__(self) -> str:
        return self.to_string(True, False)