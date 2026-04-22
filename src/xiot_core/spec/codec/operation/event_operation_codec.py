from typing import Optional, Dict, Any

from xiot_core.spec.codec.operation.abstract_operation_codec import AbstractOperationCodec
from xiot_core.spec.codec.operation.argument_operation_codec import ArgumentOperationCodec
from xiot_core.spec.typedef.operation.event_operation import EventOperation
from xiot_core.spec.typedef.status.status import Status
from xiot_core.spec.typedef.xid.event_id import EventID

class EventOperationCodec:
    """事件操作编解码器（对应Java EventOperationCodec）"""

    # 静态实例
    QUERY: AbstractOperationCodec = None
    RESULT: AbstractOperationCodec = None

    def __init__(self):
        # 初始化内部子类实例
        EventOperationCodec.QUERY = self.Query()
        EventOperationCodec.RESULT = self.Result()

    class Query(AbstractOperationCodec[EventOperation, Dict[str, Any]]):
        """Query子编解码器"""

        def decode_single(self, o: Dict[str, Any]) -> Optional[EventOperation]:
            if not isinstance(o, dict):
                return None

            eid_str = o.get("eid", "")
            oid = o.get("oid", None)
            arguments = o.get("arguments")

            eid = EventID.parse(eid_str)

            event = EventOperation(eid)
            event.oid = oid

            if arguments is not None:
                if isinstance(arguments, list):
                    event.arguments = ArgumentOperationCodec.decode(arguments)
                elif isinstance(arguments, dict):
                    event.arguments_compact = True
                    event.arguments = ArgumentOperationCodec.decode_dict(arguments)

            return event

        def encode_single(self, event: EventOperation) -> Optional[Dict[str, Any]]:
            if event.is_error:
                return None

            o: Dict[str, Any] = {}
            o["eid"] = str(event.eid)

            if event.oid is not None:
                o["oid"] = event.oid

            if len(event.arguments) > 0:
                o["arguments"] = ArgumentOperationCodec.encode_compact(
                    event.arguments_compact,
                    event.arguments.values()
                )

            return o

    class Result(AbstractOperationCodec[EventOperation, Dict[str, Any]]):
        """Result子编解码器"""

        def decode_single(self, o: Dict[str, Any]) -> Optional[EventOperation]:
            if not isinstance(o, dict):
                return None

            status = o.get("status", Status.COMPLETED)
            description = o.get("description", "")
            eid_str = o.get("eid", "")
            eid = EventID.parse(eid_str)

            operation = EventOperation(eid)
            operation.status = status

            if operation.is_error:
                operation.description = description

            return operation

        def encode_single(self, operation: EventOperation) -> Dict[str, Any]:
            o: Dict[str, Any] = {}
            o["eid"] = str(operation.eid)
            o["status"] = operation.status

            if not operation.is_completed:
                o["description"] = operation.description

            return o


# 初始化静态实例
EventOperationCodec()