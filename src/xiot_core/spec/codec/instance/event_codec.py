from typing import Dict, Any, Optional

from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.codec.instance.argument_codec import ArgumentCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.urn.event_type import EventType
from xiot_core.spec.typedef.instance.event import Event


class EventCodec:
    @staticmethod
    def decode_dict(obj: Dict[str, Any]) -> Event:
        iid = obj.get(Spec.IID, -1)
        type_ = EventType.parse(obj.get(Spec.TYPE, ""))
        description = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION, {}))
        arguments = ArgumentCodec.decode(obj.get(Spec.ARGUMENTS))
        event = Event(iid, type_)
        event.description = description
        event.arguments = arguments
        return event

    @staticmethod
    def decode_array(array: Optional[list[Any]]) -> list[Event]:
        events = []
        if not array:
            return events

        for i in range(len(array)):
            events.append(EventCodec.decode_dict(array[i]))
        return events

    @staticmethod
    def encode(event: Event) -> Dict[str, Any]:
        o: Dict[str, Any] = {
            Spec.IID: event.iid,
            Spec.TYPE: str(event.type)
        }

        if len(event.description) > 0:
            o[Spec.DESCRIPTION] = DescriptionCodec.encode(event.description)

        if len(event.arguments) > 0:
            o[Spec.ARGUMENTS] = ArgumentCodec.encode_collection(list(event.arguments.values()))

        return o

