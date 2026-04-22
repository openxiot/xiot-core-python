from typing import Dict, Any

from src.spec.codec.definition.description_codec import DescriptionCodec
from src.spec.codec.instance.argument_codec import ArgumentCodec
from src.spec.typedef.constant.spec import Spec
from src.spec.typedef.definition.urn.event_type import EventType
from src.spec.typedef.instance.argument import Argument
from src.support.typedef.controller.event_controller import EventController


class EventControllerCodec:
    @staticmethod
    def decode(obj: Dict[str, Any]) -> EventController:
        iid: int = obj.get(Spec.IID, -1)
        type_str: str = obj.get(Spec.TYPE, "")
        type_: EventType = EventType.parse(type_str)
        description: Dict[str, str] = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION))
        arguments: list[Argument] = ArgumentCodec.decode(obj.get(Spec.ARGUMENTS, []))
        return EventController(iid, type_, description, arguments)

    @staticmethod
    def decode_array(array: list[Dict[str, Any]]) -> list[EventController]:
        events: list[EventController] = []
        if array is not None:
            for item in array:
                events.append(EventControllerCodec.decode(item))
        return events