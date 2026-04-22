from typing import List, Optional, TypeVar, Generic

from xiot_core.spec.typedef.definition.property.constraint_value import ConstraintValue
from xiot_core.spec.typedef.definition.property.data.data_value import DataValue
from xiot_core.spec.typedef.definition.property.data.value.vstring import Vstring

T = TypeVar('T')

class ValueLength(ConstraintValue[T], Generic[T]):
    def __init__(self, min_length: int, max_length: int):
        if min_length is None or min_length < 0:
            raise ValueError(f"minLength invalid: {min_length}")
        if max_length is None or max_length <= 0:
            raise ValueError(f"maxLength invalid: {max_length}")
        if min_length > max_length:
            raise ValueError(f"check(min, max) failed, min: {min_length} max: {max_length}")

        self.min_length = min_length
        self.max_length = max_length
        self.fixed_length: Optional[int] = min_length if min_length == max_length else None

    def validate(self, value: DataValue[T]) -> bool:
        if not isinstance(value, Vstring):
            return False

        value_length = len(value.raw_value())
        if self.fixed_length is not None:
            return value_length == self.fixed_length
        return self.min_length <= value_length <= self.max_length

    def max_length(self) -> int:
        return self.max_length

    def min_length(self) -> int:
        return self.min_length

    def fixed_length(self) -> Optional[int]:
        return self.fixed_length

    def to_list(self) -> List[int]:
        return [self.min_length, self.max_length]