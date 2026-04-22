from typing import Optional
from decimal import Decimal

from xiot_core.spec.typedef.definition.property.data.data_value import DataValue


class Vfloat(DataValue[float]):
    def __init__(self, value: float = 0.0):
        if isinstance(value, (float, int)):
            self._value = float(value)
        elif isinstance(value, Decimal):
            self._value = float(value)
        else:
            self._value = 0.0

    def less_equals(self, max_value: DataValue) -> bool:
        if not isinstance(max_value, Vfloat):
            return False
        return self.raw_value() <= max_value.raw_value()

    def validate(self, min_value: DataValue, max_value: DataValue) -> bool:
        if not (isinstance(min_value, Vfloat) and isinstance(max_value, Vfloat)):
            return False
        min_v = min_value.raw_value()
        max_v = max_value.raw_value()
        current = self.raw_value()
        if current < min_v or current > max_v:
            print(f"Vfloat.validate failed: {self._value} min: {min_value} max: {max_value}")
            return False
        return True

    def validate_with_step(self, min_value: DataValue, max_value: DataValue, step: DataValue) -> bool:
        if not (isinstance(min_value, Vfloat) and isinstance(max_value, Vfloat) and isinstance(step, Vfloat)):
            return False
        min_v = min_value.raw_value()
        max_v = max_value.raw_value()
        step_v = step.raw_value()

        current = self.raw_value()
        if current < min_v or current > max_v:
            print(f"Vfloat.validate failed: {self._value} min: {min_v} max: {max_v}")
            return False

        def to_long(num: float) -> int:
            num_float = num * 10000000
            result = int(num_float)
            return (result + 1) // 10 * 10

        min_long = to_long(min_v)
        step_long = to_long(step_v)
        value_long = to_long(current)

        return (value_long - min_long) % step_long == 0

    def raw_value(self) -> float:
        return self._value

    @staticmethod
    def value_of(obj: object) -> Optional['Vfloat']:
        if isinstance(obj, (float, int)):
            return Vfloat(obj)
        if isinstance(obj, Decimal):
            return Vfloat(float(obj))
        return None

    def __str__(self) -> str:
        return str(self._value)