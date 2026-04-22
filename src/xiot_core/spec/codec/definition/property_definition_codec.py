from typing import TypeVar, Generic, Dict

from xiot_core.spec.codec.definition.access_codec import AccessCodec
from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.codec.definition.value_length_codec import ValueLengthCodec
from xiot_core.spec.codec.definition.value_list_codec import ValueListCodec
from xiot_core.spec.codec.definition.value_range_codec import ValueRangeCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.property.value_length import ValueLength
from xiot_core.spec.typedef.definition.property.value_list import ValueList
from xiot_core.spec.typedef.definition.property.value_range import ValueRange
from xiot_core.spec.typedef.definition.property_definition import PropertyDefinition
from xiot_core.spec.typedef.definition.urn.property_type import PropertyType

T = TypeVar('T')

class PropertyDefinitionCodec(Generic[T]):
    @staticmethod
    def decode(obj: dict) -> PropertyDefinition[T]:
        def_ = PropertyDefinition[T]()
        def_.type = PropertyType.parse(obj.get(Spec.TYPE, ""))

        desc_obj = obj.get(Spec.DESCRIPTION)
        def_.description = DescriptionCodec.decode(desc_obj)

        format_str = obj.get(Spec.FORMAT, "")
        def_.format = DataFormat.from_str(format_str)

        access_array = obj.get(Spec.ACCESS, [])
        def_.access = AccessCodec.decode(access_array)

        unit = obj.get(Spec.UNIT)
        def_.unit = unit

        fmt = def_.format
        if fmt == DataFormat.COMBINATION:
            members_array = obj.get(Spec.MEMBERS, [])
            def_.members = PropertyDefinitionCodec._decode_types(members_array)
        else:
            has_value_list = Spec.VALUE_LIST in obj
            has_value_range = Spec.VALUE_RANGE in obj
            if has_value_list and has_value_range:
                raise ValueError("value-list & value-range both exist!")

            if has_value_list:
                value_list_array = obj.get(Spec.VALUE_LIST, [])
                val_list = ValueListCodec.decode(fmt, value_list_array)
                def_.constraint_value = val_list

            if has_value_range:
                value_range_array = obj.get(Spec.VALUE_RANGE, [])
                val_range = ValueRangeCodec.decode(fmt, value_range_array)
                def_.constraint_value = val_range

            if Spec.VALUE_LENGTH in obj:
                value_length_array = obj.get(Spec.VALUE_LENGTH, [])
                val_length = ValueLengthCodec.decode(value_length_array)
                def_.constraint_value = val_length

        return def_

    @staticmethod
    def encode(def_: PropertyDefinition[T]) -> dict:
        obj: Dict[str, object] = {}
        if def_.type:
            obj[Spec.TYPE] = str(def_.type)

        obj[Spec.DESCRIPTION] = DescriptionCodec.encode(def_.description)

        if def_.format:
            obj[Spec.FORMAT] = def_.format.value

        if def_.access:
            obj[Spec.ACCESS] = def_.access.to_list()

        if def_.unit:
            obj[Spec.UNIT] = def_.unit

        constraint_val = def_.constraint_value
        if constraint_val:
            if isinstance(constraint_val, ValueList):
                obj[Spec.VALUE_LIST] = ValueListCodec.encode(constraint_val)
            elif isinstance(constraint_val, ValueRange):
                obj[Spec.VALUE_RANGE] = ValueRangeCodec.encode(constraint_val)
            elif isinstance(constraint_val, ValueLength):
                obj[Spec.VALUE_LENGTH] = ValueLengthCodec.encode(constraint_val)

        if def_.members:
            obj[Spec.MEMBERS] = PropertyDefinitionCodec._encode_types(def_.members)

        return obj

    @staticmethod
    def _decode_types(array: list[str]) -> list[PropertyType]:
        return [PropertyType.parse(s) for s in array if isinstance(s, str)]

    @staticmethod
    def _encode_types(types: list[PropertyType]) -> list[str]:
        return [str(t) for t in types]