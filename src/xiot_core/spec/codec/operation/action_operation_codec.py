from typing import Optional, Dict, Any

from xiot_core.spec.codec.operation.abstract_operation_codec import AbstractOperationCodec
from xiot_core.spec.codec.operation.argument_operation_codec import ArgumentOperationCodec
from xiot_core.spec.typedef.operation.action_operation import ActionOperation
from xiot_core.spec.typedef.status.status import Status
from xiot_core.spec.typedef.xid.action_id import ActionID


class ActionOperationCodec:
    """动作操作编解码器（对应Java ActionOperationCodec）"""

    QUERY: AbstractOperationCodec  = None
    RESULT: AbstractOperationCodec = None

    def __init__(self):
        ActionOperationCodec.QUERY = self.Query()
        ActionOperationCodec.RESULT = self.Result()

    class Query(AbstractOperationCodec[ActionOperation, Dict[str, Any]]):
        """Query子编解码器"""

        def decode_single(self, o: Any) -> Optional[ActionOperation]:
            if not isinstance(o, dict):
                return None

            obj = o
            aid_str = obj.get("aid", "")
            aid = ActionID.parse(aid_str)
            oid = obj.get("oid", None)

            operation = ActionOperation(aid)
            operation.oid = oid

            in_ = obj.get("in")
            if in_ is not None:
                if isinstance(in_, list):
                    operation.arguments_in = ArgumentOperationCodec.decode(in_)
                elif isinstance(in_, dict):
                    operation.arguments_compact = True
                    operation.arguments_in = ArgumentOperationCodec.decode_dict(in_)

            return operation

        def encode_single(self, action: ActionOperation) -> Optional[Dict[str, Any]]:
            if action.is_error:
                return None

            o: Dict[str, Any] = {
                "aid": str(action.aid)
            }

            if action.oid is not None:
                o["oid"] = action.oid

            if action.arguments_in:
                o["in"] = ArgumentOperationCodec.encode_compact(
                    action.arguments_compact,
                    list(action.arguments_in.values())
                )

            return o

    class Result(AbstractOperationCodec[ActionOperation, Dict[str, Any]]):
        """Result子编解码器"""

        def decode_single(self, o: Any) -> Optional[ActionOperation]:
            if not isinstance(o, dict):
                return None

            obj = o
            status = obj.get("status", Status.COMPLETED)
            description = obj.get("description", "")
            aid_str = obj.get("aid", "")
            oid = obj.get("oid", None)
            out = obj.get("out")

            action = ActionOperation(aid_str)
            action.status = status
            action.oid = oid

            if action.is_completed:
                if out is not None:
                    if isinstance(out, list):
                        action.arguments_out = ArgumentOperationCodec.decode(out)
                    elif isinstance(out, dict):
                        action.arguments_compact = True
                        action.arguments_out = ArgumentOperationCodec.decode_dict(out)
            else:
                action.status = status
                action.description = description

            return action

        def encode_single(self, action: ActionOperation) -> Dict[str, Any]:
            o: Dict[str, Any] = {
                "aid": str(action.aid),
                "status": action.status
            }

            if action.oid is not None:
                o["oid"] = action.oid

            if action.is_completed:
                if len(action.arguments_out) > 0:
                    o["out"] = ArgumentOperationCodec.encode_compact(
                        action.arguments_compact,
                        list(action.arguments_out.values())
                    )
            else:
                o["description"] = action.description

            return o


# 初始化静态实例
ActionOperationCodec()