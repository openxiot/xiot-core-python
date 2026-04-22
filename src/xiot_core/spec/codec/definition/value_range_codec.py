from typing import TypeVar, Generic

from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.property.value_range import ValueRange

T = TypeVar('T')


class ValueRangeCodec(Generic[T]):
    @staticmethod
    def decode(fmt: DataFormat, array: list[T]) -> ValueRange[T]:
        return ValueRange(fmt, array.copy())

    @staticmethod
    def encode(range_: ValueRange[T]) -> list[T]:
        return range_.to_list().copy()