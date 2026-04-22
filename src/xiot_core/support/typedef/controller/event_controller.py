from typing import Dict

from xiot_core.spec.typedef.definition.urn.event_type import EventType
from xiot_core.spec.typedef.instance.argument import Argument
from xiot_core.spec.typedef.instance.event import Event
from xiot_core.spec.typedef.operation.event_operation import EventOperation


class EventController(Event):
    def __init__(self,
                 iid: int,
                 type_: EventType,
                 description: Dict[str, str] = None,
                 arguments: list[Argument] = None):
        super().__init__()
        if description is None:
            description = {}
        if arguments is None:
            arguments = []
        self._iid = iid
        self._type = type_
        self._description = description
        self.arguments = arguments

    def handle_event_occurred(self, o: EventOperation) -> None:
        pass