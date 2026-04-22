from typing import Optional, Dict

from xiot_core.spec.typedef.definition.argument_definition import ArgumentDefinition
from xiot_core.spec.typedef.definition.urn.event_type import EventType


class EventDefinition:
    def __init__(self, type_: EventType, description: Optional[Dict[str, str]] = None, arguments: Optional[list[ArgumentDefinition]] = None):
        self._type = type_
        self._description = description if description is not None else {}
        self._arguments: list[ArgumentDefinition] = []
        if arguments:
            self._arguments.extend(arguments)

    @property
    def type(self) -> EventType:
        return self._type

    @type.setter
    def type(self, type_: EventType) -> None:
        self._type = type_

    @property
    def arguments(self) -> list[ArgumentDefinition]:
        return self._arguments

    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Dict[str, str]) -> None:
        self._description = description