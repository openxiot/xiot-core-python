from __future__ import annotations
from typing import Dict, Collection, Optional

from xiot_core.spec.typedef.definition.urn.action_type import ActionType
from xiot_core.spec.typedef.instance.argument import Argument


class Action:
    def __init__(self, iid: int = 0, type_: Optional[ActionType] = None):
        self._iid = iid
        self._type = type_
        self._description: Dict[str, str] = {}
        self._in: Dict[int, Argument] = {}
        self._out: Dict[int, Argument] = {}

    # iid 属性
    @property
    def iid(self) -> int:
        return self._iid

    @iid.setter
    def iid(self, iid: int) -> None:
        self._iid = iid

    # type 属性
    @property
    def type(self) -> Optional[ActionType]:
        return self._type

    @type.setter
    def type(self, type_: ActionType) -> None:
        self._type = type_

    # description 属性
    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Optional[Dict[str, str]]) -> None:
        if description is not None:
            self._description = description

    # in 属性（避免关键字冲突，用in_args）
    @property
    def arguments_in(self) -> Dict[int, Argument]:
        return self._in

    @arguments_in.setter
    def arguments_in(self, args: Collection[Argument]) -> None:
        for a in args:
            self._in[a.piid] = a

    # out 属性
    @property
    def arguments_out(self) -> Dict[int, Argument]:
        return self._out

    @arguments_out.setter
    def arguments_out(self, out_args: Collection[Argument]) -> None:
        for a in out_args:
            self._out[a.piid] = a

    # 比较方法
    def compare_to(self, other: Action) -> int:
        return self._iid - other.iid