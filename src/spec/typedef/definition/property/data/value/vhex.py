from typing import Optional

from src.spec.typedef.definition.property.data.data_value import DataValue


class Vhex(DataValue[str]):
    def __init__(self, value: str = ""):
        self._value = value if isinstance(value, str) else ""

    def get_integer_value(self) -> int:
        """将十六进制字符串转为整数"""
        try:
            return int(self._value, 16)
        except (ValueError, TypeError):
            return 0

    def less_equals(self, max_value: DataValue) -> bool:
        if not isinstance(max_value, Vhex):
            return False
        return self.get_integer_value() <= max_value.get_integer_value()

    def validate(self, min_value: DataValue, max_value: DataValue) -> bool:
        if not (isinstance(min_value, Vhex) and isinstance(max_value, Vhex)):
            return False
        min_v = min_value.get_integer_value()
        max_v = max_value.get_integer_value()
        current = self.get_integer_value()
        if current < min_v or current > max_v:
            print(f"Vhex.validate failed: {self._value} min: {min_value} max: {max_value}")
            return False
        return True

    def validate_with_step(self, min_value: DataValue, max_value: DataValue, step: DataValue) -> bool:
        if not (isinstance(min_value, Vhex) and isinstance(max_value, Vhex) and isinstance(step, Vhex)):
            return False
        min_v = min_value.get_integer_value()
        max_v = max_value.get_integer_value()
        step_v = step.get_integer_value()

        v = min_v
        while v <= max_v:
            if v == self.get_integer_value():
                return True
            v += step_v

        print(f"Vhex.validate failed: {self._value} min: {min_value} max: {max_value} step: {step}")
        return False

    def raw_value(self) -> str:
        return self._value

    @staticmethod
    def value_of(obj: object) -> Optional['Vhex']:
        if isinstance(obj, str):
            return Vhex(obj)
        return None

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Vhex):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)