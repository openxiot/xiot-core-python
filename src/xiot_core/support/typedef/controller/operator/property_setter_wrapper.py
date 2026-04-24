from typing import Callable, Awaitable

from xiot_core.spec.typedef.operation.property_operation import PropertyOperation


class PropertySetterWrapper:
    def __init__(
            self,
            did: str,
            siid: int,
            operator: Callable[[PropertyOperation], Awaitable[PropertyOperation]],
            context: object
    ):
        self._did = did
        self._siid = siid
        self._operator = operator
        self._context = context

    async def call(self, iid: int, value: object) -> None:
        operation = PropertyOperation(did=self._did, siid=self._siid, piid=iid, value=value)
        operation.context = self._context
        result: PropertyOperation = await self._operator(operation)
        if result.is_error:
            raise ValueError(f"Property set failed: {result.status}, {result.description}")