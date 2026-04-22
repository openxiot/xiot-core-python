from typing import Generic, TypeVar

from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.property.value_definition import ValueDefinition
from xiot_core.spec.typedef.definition.property.value_list import ValueList

T = TypeVar('T')

class ValueListCodec(Generic[T]):
    @staticmethod
    def decode(fmt: DataFormat, array: list[dict]) -> ValueList[T]:
        values: list[ValueDefinition[T]] = []
        for obj in array:
            if isinstance(obj, dict):
                values.append(ValueListCodec._decode(fmt, obj))
        return ValueList(values)

    @staticmethod
    def _decode(fmt: DataFormat, obj: dict) -> ValueDefinition[T]:
        value = obj.get(Spec.VALUE)
        description = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION))
        return ValueDefinition(None, description, fmt, value)

    @staticmethod
    def encode(list_: ValueList[T]) -> list[dict]:
        return [
            {
                Spec.VALUE: val.get_value(),
                Spec.DESCRIPTION: DescriptionCodec.encode(val.description)
            }
            for val in list_.values
        ]