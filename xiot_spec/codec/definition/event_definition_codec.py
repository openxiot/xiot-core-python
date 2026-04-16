from typing import Dict, Any

from xiot_spec.codec.definition.argument_definition_codec import ArgumentDefinitionCodec
from xiot_spec.codec.definition.description_codec import DescriptionCodec
from xiot_spec.codec.java.json_array import JsonArray
from xiot_spec.typedef.constant.spec import Spec
from xiot_spec.typedef.definition.event_definition import EventDefinition
from xiot_spec.typedef.definition.urn.event_type import EventType

class EventDefinitionCodec:
    @staticmethod
    def decode_list(array: list[dict]) -> list[EventDefinition]:
        return [EventDefinitionCodec.decode(obj) for obj in array]

    @staticmethod
    def decode(obj: dict) -> EventDefinition:
        type_str = obj.get(Spec.TYPE, "")
        type_ = EventType.parse(type_str)
        desc = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION))

        array = obj.get(Spec.ARGUMENTS, [])
        args = ArgumentDefinitionCodec.decode(JsonArray(array))

        return EventDefinition(type_, desc, args)

    @staticmethod
    def encode_list(list_: list[EventDefinition]) -> list[dict]:
        return [EventDefinitionCodec.encode(def_) for def_ in list_]

    @staticmethod
    def encode(def_: EventDefinition) -> dict:
        obj: Dict[str, Any] = {}
        obj[Spec.TYPE] = str(def_.type)
        obj[Spec.DESCRIPTION] = DescriptionCodec.encode(def_.description)

        arguments = def_.arguments
        if arguments:
            obj[Spec.IN] = ArgumentDefinitionCodec.encode_list(arguments)

        return obj