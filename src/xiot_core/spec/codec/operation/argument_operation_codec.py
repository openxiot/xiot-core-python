from __future__ import annotations
from typing import Optional, Dict, Any

from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.operation.argument_operation import ArgumentOperation


class ArgumentOperationCodec:
    """参数操作编解码器（对应Java ArgumentOperationCodec）"""

    @staticmethod
    def decode(array: Optional[list]) -> list[ArgumentOperation]:
        """解码列表为ArgumentOperation列表"""
        list_ = []
        if array is not None:
            for item in array:
                if isinstance(item, int):
                    list_.append(ArgumentOperationCodec.decode_int(item))
                    continue
                if isinstance(item, dict):
                    list_.append(ArgumentOperationCodec.decode_item(item))
        return list_

    @staticmethod
    def decode_int(piid: int) -> ArgumentOperation:
        """从整数解码ArgumentOperation"""
        return ArgumentOperation(piid)

    @staticmethod
    def decode_dict(obj: Dict[str, Any]) -> list[ArgumentOperation]:
        """从字典解码ArgumentOperation集合"""
        arguments = []
        for k, v in obj.items():
            if k.startswith("#"):
                iid: int = int(k[1:])
                if isinstance(v, list):
                    arguments.append(ArgumentOperationCodec.decode_argument(iid, v))
        return arguments

    @staticmethod
    def decode_item(obj: Dict[str, Any]) -> ArgumentOperation:
        """解码单个字典项为ArgumentOperation"""
        piid: int = obj.get(Spec.PIID, 0)
        values: list[Any] = obj.get(Spec.VALUES, [])
        return ArgumentOperationCodec.decode_argument(piid, values)

    @staticmethod
    def decode_argument(piid: int, values: list) -> ArgumentOperation:
        """解码参数（兼容字符串/整数piid）"""
        if isinstance(piid, str):
            piid = int(piid)
        return ArgumentOperation(piid = piid, values = values)

    @staticmethod
    def encode_single(argument: ArgumentOperation) -> Dict[str, Any]:
        """编码单个ArgumentOperation为字典"""
        obj: Dict[str, Any] = {Spec.PIID: argument.piid}
        if argument.values is not None:
            obj[Spec.VALUES] = argument.values
        return obj

    @staticmethod
    def encode(list_: list[ArgumentOperation]) -> list | dict:
        """编码参数列表（默认非紧凑模式）"""
        return ArgumentOperationCodec.encode_compact(False, list_)

    @staticmethod
    def encode_compact(compact: bool, list_: list[ArgumentOperation]) -> list | dict:
        """编码参数列表（支持紧凑/非紧凑模式）"""
        if compact:
            obj = {}
            for a in list_:
                obj[f"#{a.piid}"] = a.values
            return obj
        else:
            array = []
            for a in list_:
                array.append(ArgumentOperationCodec.encode_single(a))
            return array