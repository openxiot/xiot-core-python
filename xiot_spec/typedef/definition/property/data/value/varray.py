from typing import Optional, List, Any

from xiot_spec.typedef.definition.property.data.data_value import DataValue


class Varray(DataValue[List[Any]]):
    def __init__(self, value: Optional[List[Any]] = None):
        self._value = list(value) if value is not None else []

    def raw_value(self) -> List[Any]:
        return self._value

    @staticmethod
    def value_of(obj: Any) -> Optional['Varray']:
        if isinstance(obj, list):
            return Varray(obj)
        return None

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(other, Varray):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(tuple(self._value))  # list不可哈希，转tuple