from typing import Optional, Any

from xiot_spec.typedef.definition.property.data.data_value import DataValue


class Vint8(DataValue[int]):
    def __init__(self, value: int = 0):
        if isinstance(value, int):
            self._value = int(value)
        else:
            self._value = 0

    def less_equals(self, max_value: DataValue) -> bool:
        if not isinstance(max_value, Vint8):
            return False
        return self._value <= max_value._value

    def validate(self, min_value: DataValue, max_value: DataValue) -> bool:
        if not (isinstance(min_value, Vint8) and isinstance(max_value, Vint8)):
            return False
        min_v = min_value._value
        max_v = max_value._value
        if self._value < min_v or self._value > max_v:
            print(f"Vint8.validate failed: {self._value} min: {min_value} max: {max_value}")
            return False
        return True

    def validate_with_step(self, min_value: DataValue, max_value: DataValue, step: DataValue) -> bool:
        if not (isinstance(min_value, Vint8) and isinstance(max_value, Vint8) and isinstance(step, Vint8)):
            return False
        min_v = min_value._value
        max_v = max_value._value
        step_v = step._value

        v = min_v
        while v <= max_v:
            if v == self._value:
                return True
            v += step_v

        print(f"Vint8.validate failed: {self._value} min: {min_v} max: {max_v} step: {step}")
        return False

    def raw_value(self) -> int:
        return self._value

    @staticmethod
    def value_of(obj: Any) -> Optional['Vint8']:
        if isinstance(obj, int):
            return Vint8(int(obj))
        return None

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if not isinstance(other, Vint8):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)