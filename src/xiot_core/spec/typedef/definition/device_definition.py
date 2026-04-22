from typing import Optional, Dict

from xiot_core.spec.typedef.definition.urn.device_type import DeviceType


class DeviceDefinition:
    def __init__(self, category: str, type_: DeviceType, description: Optional[Dict[str, str]] = None):
        self._category = category
        self._type = type_
        self._description = description if description is not None else {}

    @property
    def category(self) -> str:
        return self._category

    @property
    def type(self) -> DeviceType:
        return self._type

    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Dict[str, str]) -> None:
        self._description = description