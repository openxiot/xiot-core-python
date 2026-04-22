from typing import Dict, Callable, Awaitable

from xiot_core.spec.typedef.operation.action_operation import ActionOperation
from xiot_core.spec.typedef.operation.argument_operation import ArgumentOperation


class ActionInvokerWrapper:
    def __init__(
            self,
            did: str,
            siid: int,
            operator: Callable[[ActionOperation], Awaitable[ActionOperation]]
    ):
        self._did = did
        self._siid = siid
        self._operator = operator

    async def call(self, iid: int, arguments: Dict[int, ArgumentOperation]) -> Dict[int, ArgumentOperation]:
        operation = ActionOperation(did = self._did, siid = self._siid, aiid = iid)
        operation.arguments_in = list(arguments.values())

        try:
            result = await self._operator(operation)
            if result.is_not_error:
                return result.arguments_out
            else:
                raise Exception(f"Property set failed: {result.status}, {result.description}")
        except Exception as e:
            raise Exception(f"Action invoke error: {e}")
