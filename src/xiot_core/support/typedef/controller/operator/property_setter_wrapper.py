from typing import Callable, Awaitable

from xiot_core.spec.typedef.operation.property_operation import PropertyOperation


class PropertySetterWrapper:
    def __init__(
            self,
            did: str,
            siid: int,
            operator: Callable[[PropertyOperation], Awaitable[PropertyOperation]]
    ):
        self._did = did
        self._siid = siid
        self._operator = operator

    async def call(self, iid: int, value: object) -> None:
        operation = PropertyOperation(did=self._did, siid=self._siid, piid=iid, value=value)
        result: PropertyOperation = await self._operator(operation)
        try:
            if result.is_error:
                raise Exception(f"Property set failed: {result.status}, {result.description}")
        except Exception as e:
            raise Exception(f"Property set error: {e}")
