from typing import Optional, Dict

from xiot_core.spec.typedef.definition.urn.action_type import ActionType
from xiot_core.spec.typedef.definition.urn.event_type import EventType
from xiot_core.spec.typedef.definition.urn.property_type import PropertyType
from xiot_core.spec.typedef.definition.urn.service_type import ServiceType


class ServiceDefinition:
    def __init__(self, type_: ServiceType,
                 description: Optional[Dict[str, str]] = None,
                 required_properties: Optional[list[PropertyType]] = None,
                 optional_properties: Optional[list[PropertyType]] = None,
                 required_actions: Optional[list[ActionType]] = None,
                 optional_actions: Optional[list[ActionType]] = None,
                 required_events: Optional[list[EventType]] = None,
                 optional_events: Optional[list[EventType]] = None):
        self._type = type_
        self._description = description if description is not None else {}

        self._required_properties: list[PropertyType] = []
        if required_properties:
            self._required_properties.extend(required_properties)

        self._optional_properties: list[PropertyType] = []
        if optional_properties:
            self._optional_properties.extend(optional_properties)

        self._required_actions: list[ActionType] = []
        if required_actions:
            self._required_actions.extend(required_actions)

        self._optional_actions: list[ActionType] = []
        if optional_actions:
            self._optional_actions.extend(optional_actions)

        self._required_events: list[EventType] = []
        if required_events:
            self._required_events.extend(required_events)

        self._optional_events: list[EventType] = []
        if optional_events:
            self._optional_events.extend(optional_events)

    @property
    def type(self) -> ServiceType:
        return self._type

    @type.setter
    def type(self, type_: ServiceType) -> None:
        self._type = type_

    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Dict[str, str]) -> None:
        self._description = description

    @property
    def required_properties(self) -> list[PropertyType]:
        return self._required_properties

    @property
    def optional_properties(self) -> list[PropertyType]:
        return self._optional_properties

    @property
    def required_actions(self) -> list[ActionType]:
        return self._required_actions

    @property
    def optional_actions(self) -> list[ActionType]:
        return self._optional_actions

    @property
    def required_events(self) -> list[EventType]:
        return self._required_events

    @property
    def optional_events(self) -> list[EventType]:
        return self._optional_events