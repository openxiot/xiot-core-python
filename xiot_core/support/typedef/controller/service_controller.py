from typing import Dict

from xiot_core.spec.typedef.definition.urn.service_type import ServiceType
from xiot_core.spec.typedef.instance.service import Service
from xiot_core.spec.typedef.operation.event_operation import EventOperation
from xiot_core.spec.typedef.operation.property_operation import PropertyOperation
from xiot_core.spec.typedef.status.abstract_status import IotError
from xiot_core.spec.typedef.status.status import Status
from xiot_core.support.typedef.controller.action_controller import ActionController
from xiot_core.support.typedef.controller.event_controller import EventController
from xiot_core.support.typedef.controller.property_controller import PropertyController


class ServiceController(Service):

    def __init__(self,
                 iid: int,
                 type_: ServiceType,
                 description: Dict[str, str] = None,
                 properties: list[PropertyController[object]] = None,
                 actions: list[ActionController] = None,
                 events: list[EventController] = None):
        super().__init__(iid, type_)
        if description is None:
            description = {}
        if properties is None:
            properties = []
        if actions is None:
            actions = []
        if events is None:
            events = []

        self._description = description
        self._properties: Dict[int, PropertyController] = {}
        self._actions: Dict[int, ActionController] = {}
        self._events: Dict[int, EventController] = {}

        for p in properties:
            self._properties[p.iid] = p
        for a in actions:
            self._actions[a.iid] = a
        for e in events:
            self._events[e.iid] = e

    def handle_property_changed(self, o: PropertyOperation) -> None:
        p = self._properties.get(o.pid.piid)
        if p is not None:
            p.handle_property_changed(o)
        else:
            raise IotError(Status.PROPERTY_NOT_FOUND, f"property not found: {o.siid}")

    def handle_event_occurred(self, o: EventOperation) -> None:
        e = self._events.get(o.iid)
        if e is not None:
            e.handle_event_occurred(o)
        else:
            raise ValueError(f"update failed, property not found: {o.iid}")