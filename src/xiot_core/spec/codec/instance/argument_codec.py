from typing import Optional, Any, Dict

from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.instance.argument import Argument


class ArgumentCodec:
    @staticmethod
    def decode(array: Optional[list[Any]]) -> list[Argument]:
        list_ = []
        if not array:
            return list_

        for o in array:
            if isinstance(o, int):
                list_.append(ArgumentCodec.decode_int(o))
            elif isinstance(o, dict):
                list_.append(ArgumentCodec.decode_dict(o))
        return list_

    @staticmethod
    def decode_int(piid: int) -> Argument:
        return Argument(piid, 1, 1)

    @staticmethod
    def decode_dict(o: Dict[str, Any]) -> Argument:
        piid = o[Spec.PIID]
        min_repeat = 0
        max_repeat = 0

        repeat = o.get(Spec.REPEAT, [])
        if repeat and len(repeat) == 2:
            min_repeat = repeat[0]
            max_repeat = repeat[1]

        return Argument(piid, min_repeat, max_repeat)

    @staticmethod
    def encode(arg: Argument) -> Dict[str, Any]:
        obj: Dict[str, Any] = {Spec.PIID: arg.piid}

        if arg.max_repeat > 0:
            obj[Spec.REPEAT] = [arg.min_repeat, arg.max_repeat]

        return obj

    @staticmethod
    def encode_collection(list_: list[Argument]) -> list[Dict[str, Any]]:
        return [ArgumentCodec.encode(def_) for def_ in list_]
