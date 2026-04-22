from typing import Optional

from src.spec.typedef.definition.property.data.data_value import DataValue


class Vbool(DataValue[bool]):
    def __init__(self, value: bool = False):
        self._value = value

    def raw_value(self) -> bool:
        return self._value

    def int_value(self) -> int:
        return 1 if self._value else 0

    @staticmethod
    def value_of(obj: object) -> Optional['Vbool']:
        if isinstance(obj, bool):
            return Vbool(obj)
        if isinstance(obj, int):
            return Vbool(obj == 1)
        return None

    def __str__(self) -> str:
        return str(self._value)