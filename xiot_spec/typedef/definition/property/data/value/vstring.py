from typing import Optional, Any

from xiot_spec.typedef.definition.property.data.data_value import DataValue


class Vstring(DataValue[str]):
    def __init__(self, value: str = ""):
        self._value = value if isinstance(value, str) else ""

    def raw_value(self) -> str:
        return self._value

    @staticmethod
    def value_of(obj: Any) -> Optional['Vstring']:
        if isinstance(obj, str):
            return Vstring(obj)
        return None

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(other, Vstring):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)