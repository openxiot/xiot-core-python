from __future__ import annotations
from typing import Optional, Dict, Collection
from .abstract_operation import AbstractOperation
from .argument_operation import ArgumentOperation
from ..status.status import Status
from ..xid.event_id import EventID


class EventOperation(AbstractOperation):
    def __init__(self,
                 eid: Optional[EventID | str] = None,
                 did: Optional[str] = None,
                 siid: Optional[int] = None,
                 eiid: Optional[int] = None,
                 arguments: Optional[Collection[ArgumentOperation]] = None):
        super().__init__()
        self._eid: EventID
        self._oid: Optional[str] = None
        self._arguments: Dict[int, ArgumentOperation] = {}
        self._arguments_compact: bool = False

        # 处理不同构造参数组合
        if isinstance(eid, str):
            self._eid = EventID(string=eid)
        elif isinstance(eid, EventID):
            self._eid = eid
        elif did and siid and eiid:
            self._eid = EventID(device_id=did, siid=siid, eiid=eiid)
        else:
            raise ValueError("Invalid constructor arguments")

        # 设置参数
        if arguments:
            self.set_arguments(arguments)

        # 校验eid有效性
        if self._eid.invalid:
            self.status = Status.AID_INVALID

    @property
    def eid(self) -> EventID:
        return self._eid

    @property
    def oid(self) -> Optional[str]:
        return self._oid

    @oid.setter
    def oid(self, oid: str):
        self._oid = oid

    @property
    def arguments(self) -> Dict[int, ArgumentOperation]:
        return self._arguments

    @arguments.setter
    def arguments(self, list_args: Collection[ArgumentOperation]):
        if list_args:
            for a in list_args:
                self._arguments[a.piid] = a

    @property
    def did(self) -> str:
        return self._eid.did

    @property
    def siid(self) -> int:
        return self._eid.siid

    @property
    def iid(self) -> int:
        return self._eid.iid

    @property
    def arguments_compact(self) -> bool:
        return self._arguments_compact

    @arguments_compact.setter
    def arguments_compact(self, arguments_compact: bool):
        self._arguments_compact = arguments_compact

    def to_string(self, pretty: bool, tab: bool) -> str:
        b = []
        if tab:
            b.append("    ")

        b.append(str(self._eid))
        b.append(" =>")

        if not pretty:
            b.append(" ")

        b.append(ArgumentOperation.to_string(self._arguments, pretty, tab))
        b.append(";")

        return "".join(b)

    def __str__(self) -> str:
        return self.to_string(False, False)