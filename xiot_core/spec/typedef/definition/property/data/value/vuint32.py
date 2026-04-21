from typing import Optional

from xiot_core.spec.typedef.definition.property.data.data_value import DataValue


class Vuint32(DataValue[int]):
    def __init__(self, value: int = 0):
        if isinstance(value, int):
            self._value = int(value)
        else:
            self._value = 0

    def less_equals(self, max_value: DataValue) -> bool:
        if not isinstance(max_value, Vuint32):
            return False
        return self._value <= max_value._value

    def validate(self, min_value: DataValue, max_value: DataValue) -> bool:
        if not (isinstance(min_value, Vuint32) and isinstance(max_value, Vuint32)):
            return False
        min_v = min_value._value
        max_v = max_value._value
        return min_v <= self._value <= max_v

    def validate_with_step(self, min_value: DataValue, max_value: DataValue, step: DataValue) -> bool:
        if not (isinstance(min_value, Vuint32) and isinstance(max_value, Vuint32) and isinstance(step, Vuint32)):
            return False
        min_v = min_value._value
        max_v = max_value._value
        step_v = step._value

        v = min_v
        while v <= max_v:
            if v == self._value:
                return True
            v += step_v
        return False

    def raw_value(self) -> int:
        return self._value

    @staticmethod
    def value_of(obj: object) -> Optional['Vuint32']:
        if isinstance(obj, int):
            return Vuint32(int(obj))
        return None

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Vuint32):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)