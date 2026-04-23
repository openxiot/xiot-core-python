from xiot_core.spec.codec.definition.argument_definition_codec import ArgumentDefinitionCodec
from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.action_definition import ActionDefinition
from xiot_core.spec.typedef.definition.urn.action_type import ActionType


class ActionDefinitionCodec:
    @staticmethod
    def decode_list(array: list[dict]) -> list[ActionDefinition]:
        return [ActionDefinitionCodec.decode(obj) for obj in array]

    @staticmethod
    def decode(obj: dict) -> ActionDefinition:
        type_str = obj.get(Spec.TYPE, "")
        type_ = ActionType.parse(type_str)
        desc = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION))

        in_array = obj.get(Spec.IN, [])

        in_args = ArgumentDefinitionCodec.decode(in_array)

        out_array = obj.get(Spec.OUT, [])
        out_args = ArgumentDefinitionCodec.decode(out_array)

        return ActionDefinition(type_, desc, in_args, out_args)

    @staticmethod
    def encode_list(list_: list[ActionDefinition]) -> list[dict]:
        return [ActionDefinitionCodec.encode(def_) for def_ in list_]

    @staticmethod
    def encode(def_: ActionDefinition) -> dict:
        obj: dict[str, object] = {
            Spec.TYPE: str(def_.type),
            Spec.DESCRIPTION: DescriptionCodec.encode(def_.description)
        }

        in_args = def_.in_args
        if in_args:
            obj[Spec.IN] = ArgumentDefinitionCodec.encode_list(in_args)

        out_args = def_.out_args
        if out_args:
            obj[Spec.OUT] = ArgumentDefinitionCodec.encode_list(out_args)

        return obj