from typing import Optional, List

from src.spec.typedef.definition.property.data.data_value import DataValue


class Varray(DataValue[List[object]]):
    def __init__(self, value: Optional[List[object]] = None):
        self._value = list(value) if value is not None else []

    def raw_value(self) -> List[object]:
        return self._value

    @staticmethod
    def value_of(obj: object) -> Optional['Varray']:
        if isinstance(obj, list):
            return Varray(obj)
        return None

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Varray):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(tuple(self._value))  # list不可哈希，转tuple