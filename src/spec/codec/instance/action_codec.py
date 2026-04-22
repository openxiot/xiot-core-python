from typing import Dict, Any, Optional

from src.spec.codec.definition.description_codec import DescriptionCodec
from src.spec.codec.instance.argument_codec import ArgumentCodec
from src.spec.typedef.constant.spec import Spec
from src.spec.typedef.definition.urn.action_type import ActionType
from src.spec.typedef.instance.action import Action

class ActionCodec:
    @staticmethod
    def decode_dict(obj: Dict[str, Any]) -> Action:
        iid = obj.get(Spec.IID, -1)
        type_ = ActionType.parse(obj.get(Spec.TYPE, ""))
        description = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION, {}))
        in_ = ArgumentCodec.decode(obj.get(Spec.IN))
        out = ArgumentCodec.decode(obj.get(Spec.OUT))
        action = Action(iid, type_)
        action.description = description
        action.arguments_in = in_
        action.arguments_out = out
        return action

    @staticmethod
    def decode_array(array: Optional[list[Any]]) -> list[Action]:
        actions = []
        if not array:
            return actions

        for i in range(len(array)):
            actions.append(ActionCodec.decode_dict(array[i]))
        return actions

    @staticmethod
    def encode(action: Action) -> Dict[str, Any]:
        o: Dict[str, Any] = {
            Spec.IID: action.iid,
            Spec.TYPE: str(action.type)
        }

        if len(action.description) > 0:
            o[Spec.DESCRIPTION] = DescriptionCodec.encode(action.description)

        if len(action.arguments_in) > 0:
            o[Spec.IN] = ArgumentCodec.encode_collection(list(action.arguments_in.values()))

        if len(action.arguments_out) > 0:
            o[Spec.OUT] = ArgumentCodec.encode_collection(list(action.arguments_out.values()))

        return o
