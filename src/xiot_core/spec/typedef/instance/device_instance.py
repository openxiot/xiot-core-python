from __future__ import annotations
from typing import Dict, Optional

from xiot_core.spec.typedef.definition.urn.urn import Urn
from xiot_core.spec.typedef.instance.service import Service


class DeviceInstance:
    def __init__(self,
                 type_: Optional[Urn] = None,
                 description_: Optional[Dict[str, str]] = None,
                 services_: Optional[list[Service]] = None
                 ):
        self._type = type_
        self._description: Dict[str, str] = {}
        self._services: Dict[int, Service] = {}
        if description_ is not None:
            self._description = description_
        if services_ is not None:
            for s in services_:
                self._services[s.iid] = s

    # type 属性
    @property
    def type(self) -> Optional[Urn]:
        return self._type

    @type.setter
    def type(self, type_: Urn) -> None:
        self._type = type_

    # description 属性
    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Optional[Dict[str, str]]) -> None:
        if description is not None:
            self._description = description

    # services 属性
    @property
    def services(self) -> Dict[int, Service]:
        return self._services

    @services.setter
    def services(self, services: list[Service]) -> None:
        for s in services:
            self._services[s.iid] = s
