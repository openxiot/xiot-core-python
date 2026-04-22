from typing import Generic, TypeVar

from xiot_core.spec.typedef.definition.property.value_length import ValueLength

T = TypeVar('T')


class ValueLengthCodec(Generic[T]):
    @staticmethod
    def decode(array: list[int]) -> ValueLength[T]:
        if len(array) < 2:
            raise ValueError("ValueLength array must have at least 2 elements")
        return ValueLength(array[0], array[1])

    @staticmethod
    def encode(length: ValueLength[T]) -> list[int]:
        return length.to_list().copy()