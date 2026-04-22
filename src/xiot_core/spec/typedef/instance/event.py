from __future__ import annotations
from typing import Dict, Collection, Optional

from xiot_core.spec.typedef.definition.urn.event_type import EventType
from xiot_core.spec.typedef.instance.argument import Argument


class Event:
    def __init__(self, iid: int = 0, type_: Optional[EventType] = None):
        self._iid = iid
        self._type = type_
        self._description: Dict[str, str] = {}
        self._arguments: Dict[int, Argument] = {}

    # iid 属性
    @property
    def iid(self) -> int:
        return self._iid

    @iid.setter
    def iid(self, instance_id: int) -> None:
        self._iid = instance_id

    @property
    def type(self) -> Optional[EventType]:
        return self._type

    @type.setter
    def type(self, type_: EventType) -> None:
        self._type = type_

    # description 属性
    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Optional[Dict[str, str]]) -> None:
        if description is not None:
            self._description = description

    # arguments 属性
    @property
    def arguments(self) -> Dict[int, Argument]:
        return self._arguments

    @arguments.setter
    def arguments(self, arguments: Collection[Argument]) -> None:
        """批量设置arguments（对应Java的arguments(Collection)方法）"""
        for a in arguments:
            self._arguments[a.piid] = a

    # 比较方法（对应Java compareTo）
    def compare_to(self, other: Event) -> int:
        return self._iid - other.iid