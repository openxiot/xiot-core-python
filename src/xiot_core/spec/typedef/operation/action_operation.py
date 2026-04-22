from __future__ import annotations
from typing import Optional, Collection, Dict

from xiot_core.spec.typedef.operation.abstract_operation import AbstractOperation
from xiot_core.spec.typedef.operation.argument_operation import ArgumentOperation
from xiot_core.spec.typedef.status.status import Status
from xiot_core.spec.typedef.xid.action_id import ActionID


class ActionOperation(AbstractOperation):
    def __init__(self,
                 aid: Optional[ActionID | str] = None,
                 did: Optional[str] = None,
                 siid: Optional[int] = None,
                 aiid: Optional[int] = None,
                 oid: Optional[str] = None,
                 in_args: Optional[Collection[ArgumentOperation]] = None,
                 out_args: Optional[Collection[ArgumentOperation]] = None,
                 status: int = Status.COMPLETED,
                 description: Optional[str] = None):
        super().__init__(status, description)
        self._aid: Optional[ActionID] = None
        self._oid: Optional[str] = oid
        self._in: Dict[int, ArgumentOperation] = {}
        self._out: Dict[int, ArgumentOperation] = {}
        self._arguments_compact: bool = False

        # 初始化aid
        if isinstance(aid, str):
            self._aid = ActionID(string=aid)
        elif isinstance(aid, ActionID):
            self._aid = aid
        elif did and siid and aiid:
            self._aid = ActionID(device_id=did, siid=siid, aiid=aiid)

        # 初始化参数
        if in_args:
            self.arguments_in = in_args
        if out_args:
            self.arguments_out = out_args

        # 校验aid有效性
        if self._aid and self._aid.invalid:
            self.status = Status.AID_INVALID

    # 拷贝构造
    @classmethod
    def from_other(cls, other: ActionOperation) -> ActionOperation:
        instance = cls()
        instance._aid = ActionID(device_id=other.did, siid=other.siid, aiid=other.iid)
        instance._oid = other.oid
        # 深拷贝in参数
        for iid, arg in other.arguments_in.items():
            instance._in[iid] = ArgumentOperation(piid=arg.piid, values=arg.values)
        return instance

    def set_did(self, did: str) -> ActionOperation:
        if self._aid:
            self._aid.did = did
        return self

    @property
    def did(self) -> str:
        return self._aid.did if self._aid else ""

    @property
    def siid(self) -> int:
        return self._aid.siid if self._aid else 0

    @property
    def iid(self) -> int:
        return self._aid.iid if self._aid else 0

    @property
    def aid(self) -> Optional[ActionID]:
        return self._aid

    @property
    def oid(self) -> Optional[str]:
        return self._oid

    @oid.setter
    def oid(self, oid: str):
        self._oid = oid

    @property
    def arguments_in(self) -> Dict[int, ArgumentOperation]:
        return self._in

    @arguments_in.setter
    def arguments_in(self, arguments: Collection[ArgumentOperation]):
        for a in arguments:
            self._in[a.piid] = a

    @property
    def arguments_out(self) -> Dict[int, ArgumentOperation]:
        return self._out

    @arguments_out.setter
    def arguments_out(self, arguments: Collection[ArgumentOperation]):
        for a in arguments:
            self._out[a.piid] = a

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

        if self._aid:
            b.append(str(self._aid))

        if len(self._in) > 0:
            b.append(" =>")
            if not pretty:
                b.append(" ")
            b.append(ArgumentOperation.to_string(self._in, pretty, tab))

        b.append(";")
        return "".join(b)

    def __hash__(self) -> int:
        return hash(str(self._aid)) if self._aid else 0

    def __str__(self) -> str:
        return self.to_string(True, False)