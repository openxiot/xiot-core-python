from typing import Optional, Dict, Any

from xiot_spec.typedef.definition.property.data.data_value import DataValue


class Vcombination(DataValue[Dict[int, Any]]):
    def __init__(self, value: Optional[Dict[Any, Any]] = None):
        self._value: Dict[int, Any] = {}
        if value is not None and isinstance(value, dict):
            for k, v in value.items():
                if isinstance(k, int):
                    self._value[k] = v

    def get_value(self, k: int) -> Any:
        return self._value.get(k)

    def set_value(self, k: int, v: Any) -> None:
        self._value[k] = v

    def raw_value(self) -> Dict[int, Any]:
        return self._value

    @staticmethod
    def value_of(obj: Any) -> Optional['Vcombination']:
        if isinstance(obj, dict):
            return Vcombination(obj)
        return None

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(other, Vcombination):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(frozenset(self._value.items()))  # dict不可哈希，转frozenset