from typing import Dict

from src.spec.typedef.definition.urn.event_type import EventType
from src.spec.typedef.instance.argument import Argument
from src.spec.typedef.instance.event import Event
from src.spec.typedef.operation.event_operation import EventOperation


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