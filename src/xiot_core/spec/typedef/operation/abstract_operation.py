from __future__ import annotations
from typing import Optional

from xiot_core.spec.typedef.status.abstract_status import AbstractStatus
from xiot_core.spec.typedef.status.status import Status


class AbstractOperation(AbstractStatus):
    def __init__(self,
                 status: int = Status.COMPLETED,
                 description: Optional[str] = None):
        super().__init__(status, description)

    def to_string(self, pretty: bool, tab: bool) -> str:
        raise NotImplementedError("Subclasses must implement to_string method")

    @property
    def did(self) -> str:
        return ""

    @property
    def siid(self) -> int:
        return 0

    @property
    def iid(self) -> int:
        return 0

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, AbstractOperation):
            return False
        return self.to_string(False, False) == other.to_string(False, False)

    def __str__(self) -> str:
        return self.to_string(False, False)