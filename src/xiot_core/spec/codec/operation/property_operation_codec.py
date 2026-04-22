from __future__ import annotations
from typing import Optional, Dict, Any

from xiot_core.spec.codec.operation.abstract_operation_codec import AbstractOperationCodec
from xiot_core.spec.codec.operation.combination_value_codec import CombinationValueCodec
from xiot_core.spec.typedef.operation.property_operation import PropertyOperation
from xiot_core.spec.typedef.status.status import Status


class PropertyOperationCodec:
    """属性操作编解码器（对应Java PropertyOperationCodec）"""

    class Get:
        """Get子编解码器"""

        QUERY: AbstractOperationCodec = None
        RESULT: AbstractOperationCodec = None

        def __init__(self):
            PropertyOperationCodec.Get.QUERY = self.Query()
            PropertyOperationCodec.Get.RESULT = self.Result()

        class Query(AbstractOperationCodec[PropertyOperation, str]):
            """Get-Query子编解码器"""

            def decode_single(self, o: Any) -> Optional[PropertyOperation]:
                if not isinstance(o, str):
                    return None
                return PropertyOperation(o)

            def encode_single(self, p: PropertyOperation) -> Optional[str]:
                if p.is_error:
                    return None
                return str(p.pid)

        class Result(AbstractOperationCodec[PropertyOperation, Dict[str, Any]]):
            """Get-Result子编解码器"""

            def decode_single(self, o: Any) -> Optional[PropertyOperation]:
                if not isinstance(o, dict):
                    return None

                obj = o
                pid = obj.get("pid")
                value = obj.get("value")
                status = obj.get("status", Status.COMPLETED)

                p = PropertyOperation(pid)
                p.status = status

                if p.is_error:
                    p.description = obj.get("description", "")
                else:
                    if isinstance(value, list):
                        v = CombinationValueCodec.decode_array(value)
                        if v is not None:
                            p.value = v
                        # else:
                        #     p.value = ElementValueCodec.decode(value)
                    elif isinstance(value, dict):
                        p.arguments_compact = True
                        p.value = CombinationValueCodec.decode_dict(value)
                    else:
                        p.value = value

                return p

            def encode_single(self, p: PropertyOperation) -> Dict[str, Any]:
                obj = {"pid": str(p.pid)}

                if p.is_error:
                    obj["status"] = p.status
                    obj["description"] = p.description
                else:
                    if isinstance(p.value, dict):
                        obj["value"] = CombinationValueCodec.encode_compact(
                            p.arguments_compact,
                            p.value
                        )
                    else:
                        obj["value"] = p.value

                    # if isinstance(p.value, list):
                    #     obj["value"] = ElementValueCodec.encode(p.value)
                    # elif isinstance(p.value, dict):
                    #     obj["value"] = CombinationValueCodec.encode_compact(
                    #         p.arguments_compact,
                    #         p.value
                    #     )
                    # else:
                    #     obj["value"] = p.value

                return obj

    class Set:
        """Set子编解码器"""

        QUERY: AbstractOperationCodec = None
        RESULT: AbstractOperationCodec = None

        def __init__(self):
            PropertyOperationCodec.Set.QUERY = self.Query()
            PropertyOperationCodec.Set.RESULT = self.Result()

        class Query(AbstractOperationCodec[PropertyOperation, Dict[str, Any]]):
            """Set-Query子编解码器"""

            def decode_single(self, o: Any) -> Optional[PropertyOperation]:
                if not isinstance(o, dict):
                    return None

                obj = o
                pid = obj.get("pid")
                value = obj.get("value")

                p = PropertyOperation(pid)
                if isinstance(value, list):
                    v = CombinationValueCodec.decode_array(value)
                    if v is not None:
                        p.value = v
                    # else:
                    #     p.value = ElementValueCodec.decode(value)
                elif isinstance(value, dict):
                    p.arguments_compact = True
                    p.value = CombinationValueCodec.decode_dict(value)
                else:
                    p.value = value

                return p

            def encode_single(self, p: PropertyOperation) -> Optional[Dict[str, Any]]:
                if p.is_error:
                    return None

                o = {"pid": str(p.pid)}
                # if isinstance(p.value, list):
                #     o["value"] = ElementValueCodec.encode(p.value)
                if isinstance(p.value, dict):
                    o["value"] = CombinationValueCodec.encode_compact(
                        p.arguments_compact,
                        p.value
                    )
                else:
                    o["value"] = p.value

                return o

        class Result(AbstractOperationCodec[PropertyOperation, Dict[str, Any]]):
            """Set-Result子编解码器"""

            def decode_single(self, o: Any) -> Optional[PropertyOperation]:
                if not isinstance(o, dict):
                    return None

                obj = o
                pid = obj.get("pid", "")
                status = obj.get("status", 0)

                p = PropertyOperation(pid)
                p.status = status

                if not p.is_completed():
                    p.description = obj.get("description", "")

                return p

            def encode_single(self, p: PropertyOperation) -> Dict[str, Any]:
                obj = {
                    "pid": str(p.pid),
                    "status": p.status
                }
                if not p.is_completed():
                    obj["description"] = p.description
                return obj

    class Notify:
        """Notify子编解码器"""

        QUERY: AbstractOperationCodec = None
        RESULT: AbstractOperationCodec = None

        def __init__(self):
            PropertyOperationCodec.Notify.QUERY = self.Query()
            PropertyOperationCodec.Notify.RESULT = self.Result()

        class Query(AbstractOperationCodec[PropertyOperation, Dict[str, Any]]):
            """Notify-Query子编解码器"""

            def decode_single(self, o: Any) -> Optional[PropertyOperation]:
                if not isinstance(o, dict):
                    return None

                obj = o
                pid = obj.get("pid")
                value = obj.get("value")
                status = obj.get("status", 0)
                description = obj.get("description", "")

                p = PropertyOperation(pid)
                p.status = status
                p.description = description

                if value is not None:
                    if isinstance(value, list):
                        v = CombinationValueCodec.decode_array(value)
                        if v is not None:
                            p.value = v
                        # else:
                        #     p.value = ElementValueCodec.decode(value)
                    elif isinstance(value, dict):
                        p.arguments_compact = True
                        p.value = CombinationValueCodec.decode_dict(value)
                    else:
                        p.value = value

                return p

            def encode_single(self, p: PropertyOperation) -> Dict[str, Any]:
                o = {"pid": str(p.pid)}

                if not p.is_completed:
                    o["status"] = p.status
                    o["description"] = p.description

                if p.value is not None:
                    # if isinstance(p.value, list):
                    #     o["value"] = ElementValueCodec.encode(p.value)
                    if isinstance(p.value, dict):
                        o["value"] = CombinationValueCodec.encode_compact(
                            p.arguments_compact,
                            p.value
                        )
                    else:
                        o["value"] = p.value

                return o

        class Result(AbstractOperationCodec[PropertyOperation, Dict[str, Any]]):
            """Notify-Result子编解码器"""

            def decode_single(self, o: Any) -> Optional[PropertyOperation]:
                if not isinstance(o, dict):
                    return None

                obj = o
                pid = obj.get("pid", "")
                status = obj.get("status", Status.COMPLETED)

                p = PropertyOperation(pid)
                p.status(status)

                if p.is_error():
                    p.description(obj.get("description", ""))

                return p

            def encode_single(self, p: PropertyOperation) -> Dict[str, Any]:
                obj = {
                    "pid": str(p.pid),
                    "status": p.status
                }
                if p.is_error():
                    obj["description"] = p.description
                return obj


# 初始化静态实例
PropertyOperationCodec.Get()
PropertyOperationCodec.Set()
PropertyOperationCodec.Notify()