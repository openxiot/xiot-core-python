from typing import Optional, Dict

from src.spec.typedef.definition.property.data.data_value import DataValue


class Vcombination(DataValue[Dict[int, object]]):
    def __init__(self, value: Optional[Dict[object, object]] = None):
        self._value: Dict[int, object] = {}
        if value is not None and isinstance(value, dict):
            for k, v in value.items():
                if isinstance(k, int):
                    self._value[k] = v

    def get_value(self, k: int) -> object:
        return self._value.get(k)

    def set_value(self, k: int, v: object) -> None:
        self._value[k] = v

    def raw_value(self) -> Dict[int, object]:
        return self._value

    @staticmethod
    def value_of(obj: object) -> Optional['Vcombination']:
        if isinstance(obj, dict):
            return Vcombination(obj)
        return None

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Vcombination):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(frozenset(self._value.items()))  # dict不可哈希，转frozenset