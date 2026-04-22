from typing import Optional

from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.argument_definition import ArgumentDefinition
from xiot_core.spec.typedef.definition.urn.property_type import PropertyType


class ArgumentDefinitionCodec:
    @staticmethod
    def decode(array: list[dict]) -> list[ArgumentDefinition]:
        list_: list[ArgumentDefinition] = []
        if array is None:
            return list_

        for obj in array:
            if isinstance(obj, str):
                arg = ArgumentDefinitionCodec.decode_str(obj)
                if arg:
                    list_.append(arg)
            elif isinstance(obj, dict):
                arg = ArgumentDefinitionCodec.decode_dict(obj)
                if arg:
                    list_.append(arg)
        return list_

    @staticmethod
    def decode_str(type_str: str) -> Optional[ArgumentDefinition]:
        return ArgumentDefinition(PropertyType.parse(type_str), 1, 1)

    @staticmethod
    def decode_dict(obj: dict) -> Optional[ArgumentDefinition]:
        type_str = obj.get(Spec.PROPERTY, "")
        type_ = PropertyType.parse(type_str)
        repeat: list[int] | None = obj.get(Spec.REPEAT)

        if repeat is None:
            return None

        if len(repeat) != 2:
            return None

        min_rep = repeat[0]
        max_rep = repeat[1]
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