from typing import Dict, Any

from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.codec.instance.argument_codec import ArgumentCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.urn.action_type import ActionType
from xiot_core.spec.typedef.instance.argument import Argument
from xiot_core.support.typedef.controller.action_controller import ActionController


class ActionControllerCodec:
    @staticmethod
    def _decode(obj: Dict[str, Any]) -> ActionController:
        iid: int = obj.get(Spec.IID, -1)
        type_str: str = obj.get(Spec.TYPE, "")
        type_: ActionType = ActionType.parse(type_str)
        description: Dict[str, str] = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION))
        in_args: list[Argument] = ArgumentCodec.decode(obj.get(Spec.IN, []))
        out_args: list[Argument] = ArgumentCodec.decode(obj.get(Spec.OUT, []))
        return ActionController(iid, type_, description, in_args, out_args)

    @staticmethod
    def decode(array: list[Dict[str, Any]]) -> list[ActionController]:
        actions: list[ActionController] = []
        if array is not None:
            for item in array:
                actions.append(ActionControllerCodec._decode(item))
        return actions