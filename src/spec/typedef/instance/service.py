from __future__ import annotations
from typing import Dict, Optional

from src.spec.typedef.definition.urn.service_type import ServiceType
from src.spec.typedef.instance.action import Action
from src.spec.typedef.instance.event import Event
from src.spec.typedef.instance.property import Property

class Service:
    def __init__(self, iid: int = 0, type_: Optional[ServiceType] = None):
        self._iid = iid
        self._type = type_
        self._description: Dict[str, str] = {}
        self._properties: Dict[int, Property[object]] = {}
        self._actions: Dict[int, Action] = {}
        self._events: Dict[int, Event] = {}

    # iid 属性
    @property
    def iid(self) -> int:
        return self._iid

    @iid.setter
    def iid(self, iid: int) -> None:
        self._iid = iid

    # type 属性
    @property
    def type(self) -> Optional[ServiceType]:
        return self._type

    @type.setter
    def type(self, type_: ServiceType) -> None:
        self._type = type_

    # description 属性
    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Optional[Dict[str, str]]) -> None:
        if description is not None:
            self._description = description

    # properties 属性
    @property
    def properties(self) -> Dict[int, Property[object]]:
        return self._properties

    @properties.setter
    def properties(self, properties: list[Property[object]]) -> None:
        for p in properties:
            self._properties[p.iid] = p

    # actions 属性
    @property
    def actions(self) -> Dict[int, Action]:
        return self._actions

    @actions.setter
    def actions(self, actions: list[Action]) -> None:
        for a in actions:
            self._actions[a.iid] = a

    # events 属性
    @property
    def events(self) -> Dict[int, Event]:
        return self._events

    @events.setter
    def events(self, events: list[Event]) -> None:
        for e in events:
            self._events[e.iid] = e

    # 比较方法
    def compare_to(self, other: Service) -> int:
        return self._iid - other.iid

    @classmethod
    def from_type_str(cls, type_str: str) -> Service:
        """对应Java的 Service(String type) 构造方法"""
        instance = cls()
        instance.type = ServiceType.parse(type_str)
        return instance