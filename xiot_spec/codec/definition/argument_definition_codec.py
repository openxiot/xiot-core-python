from typing import Optional, Union

from xiot_spec.codec.java.json_array import JsonArray
from xiot_spec.codec.java.json_object import JsonObject
from xiot_spec.typedef.constant.spec import Spec
from xiot_spec.typedef.definition.argument_definition import ArgumentDefinition
from xiot_spec.typedef.definition.urn.property_type import PropertyType


class ArgumentDefinitionCodec:
    @staticmethod
    def decode(array: JsonArray) -> list[ArgumentDefinition]:
        list_: list[ArgumentDefinition] = []
        if array is None:
            return list_

        for obj in array:
            if isinstance(obj, str):
                arg = ArgumentDefinitionCodec.decode_str(obj)
                if arg:
                    list_.append(arg)
            elif isinstance(obj, JsonObject):
                arg = ArgumentDefinitionCodec.decode_dict(obj)
                if arg:
                    list_.append(arg)
        return list_

    @staticmethod
    def decode_str(type_str: str) -> Optional[ArgumentDefinition]:
        return ArgumentDefinition(PropertyType.parse(type_str), 1, 1)

    @staticmethod
    def decode_dict(obj: JsonObject) -> Optional[ArgumentDefinition]:
        type_str = obj.opt_string(Spec.PROPERTY, "")
        type_ = PropertyType.parse(type_str)
        repeat: JsonArray | None = obj.get_json_array(Spec.REPEAT)

        if repeat is None:
            return None

        if repeat.size() != 2:
            return None

        min_rep = repeat.get(0)
        max_rep = repeat.get(1)
        if not isinstance(min_rep, int) or not isinstance(max_rep, int):
            return None

        return ArgumentDefinition(type_, min_rep, max_rep)

    @staticmethod
    def encode(def_: ArgumentDefinition) -> dict:
        repeat = [def_.min_repeat, def_.max_repeat]
        return {
            Spec.PROPERTY: str(def_.type),
            Spec.REPEAT: repeat
        }

    @staticmethod
    def encode_list(list_: list[ArgumentDefinition]) -> list[dict]:
        return [ArgumentDefinitionCodec.encode(def_) for def_ in list_]