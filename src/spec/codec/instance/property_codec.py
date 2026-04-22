from typing import Generic, TypeVar, Dict, Any, Optional

from src.spec.codec.definition.access_codec import AccessCodec
from src.spec.codec.definition.description_codec import DescriptionCodec
from src.spec.codec.definition.value_length_codec import ValueLengthCodec
from src.spec.codec.definition.value_list_codec import ValueListCodec
from src.spec.codec.definition.value_range_codec import ValueRangeCodec
from src.spec.typedef.constant.spec import Spec
from src.spec.typedef.definition.property.data.data_format import DataFormat
from src.spec.typedef.definition.property.value_length import ValueLength
from src.spec.typedef.definition.property.value_list import ValueList
from src.spec.typedef.definition.property.value_range import ValueRange
from src.spec.typedef.definition.urn.property_type import PropertyType
from src.spec.typedef.instance.property import Property

T = TypeVar('T')

class PropertyCodec(Generic[T]):
    @staticmethod
    def decode_array(array: Optional[list[Any]]) -> list[Property[T]]:
        properties = []
        if not array:
            return properties

        for i in range(len(array)):
            prop = PropertyCodec.decode_dict(array[i])
            properties.append(prop)
        return properties

    @staticmethod
    def decode_dict(obj: Dict[str, Any]) -> Property[T]:
        p = Property[T]()

        p.iid = obj.get(Spec.IID, 0)
        p.type = PropertyType.parse(obj.get(Spec.TYPE, ""))
        p.description = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION, {}))
        p.format = DataFormat.from_str(obj.get(Spec.FORMAT, ""))
        p.access = AccessCodec.decode(obj.get(Spec.ACCESS, []))
        p.unit = obj.get(Spec.UNIT, None)

        if p.format == DataFormat.COMBINATION:
            p.members = PropertyCodec._decode_iids(obj.get(Spec.MEMBERS))
        else:
            has_value_list = Spec.VALUE_LIST in obj
            has_value_range = Spec.VALUE_RANGE in obj
            if has_value_list and has_value_range:
                raise ValueError("value-list & value-range both exist!")

            if has_value_list:
                p.constraint = ValueListCodec.decode(p.format, obj.get(Spec.VALUE_LIST, []))

            if has_value_range:
                p.constraint = ValueRangeCodec.decode(p.format, obj.get(Spec.VALUE_RANGE, []))

            if Spec.VALUE_LENGTH in obj:
                p.constraint = ValueLengthCodec.decode(obj.get(Spec.VALUE_LENGTH, []))

        p.initialize_value()
        p.default_value = obj.get(Spec.DEFAULT_VALUE)

        return p

    @staticmethod
    def encode(p: Property[T]) -> Dict[str, Any]:
        o: Dict[str, Any] = {
            Spec.IID: p.iid,
            Spec.TYPE: str(p.type),
            Spec.FORMAT: str(p.format),
        }

        access = p.access
        if access is not None:
            o[Spec.ACCESS] = access.to_list()

        if p.description and len(p.description) > 0:
            o[Spec.DESCRIPTION] = DescriptionCodec.encode(p.description)

        constraint_val = p.constraint
        if constraint_val:
            if isinstance(constraint_val, ValueList):
                o[Spec.VALUE_LIST] = ValueListCodec.encode(constraint_val)
            elif isinstance(constraint_val, ValueRange):
                o[Spec.VALUE_RANGE] = ValueRangeCodec.encode(constraint_val)
            elif isinstance(constraint_val, ValueLength):
                o[Spec.VALUE_LENGTH] = ValueLengthCodec.encode(constraint_val)

        if p.unit is not None:
            o[Spec.UNIT] = p.unit

        if p.members and len(p.members) > 0:
            o[Spec.MEMBERS] = PropertyCodec._encode_iids(p.members)

        v = p.default_value
        if v is not None:
            o[Spec.DEFAULT_VALUE] = v.raw_value()

        return o

    @staticmethod
    def _decode_iids(array: Optional[list[Any]]) -> list[int]:
        types = []
        if not array:
            return types
        for o in array:
            if isinstance(o, int):
                types.append(o)
        return types

    @staticmethod
    def _encode_iids(types: list[int]) -> list[int]:
        return types