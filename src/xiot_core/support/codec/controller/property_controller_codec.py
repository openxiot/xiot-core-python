from typing import Dict, Any, TypeVar, Generic

from xiot_core.spec.codec.instance.property_codec import PropertyCodec
from xiot_core.spec.typedef.instance.property import Property
from xiot_core.support.typedef.controller.property_controller import PropertyController

T = TypeVar('T')

class PropertyControllerCodec(Generic[T]):
    @staticmethod
    def decode(array: list[Dict[str, Any]]) -> list[PropertyController[T]]:
        properties: list[PropertyController[T]] = []
        if array is not None:
            for item in array:
                properties.append(PropertyControllerCodec._decode(item))
        return properties

    @staticmethod
    def _decode(obj: Dict[str, Any]) -> PropertyController[T]:
        other: Property[T] = PropertyCodec.decode_dict(obj)
        return PropertyController[T](other = other)

    @staticmethod
    def encode(property_: PropertyController[Any]) -> Dict[str, Any]:
        return PropertyCodec.encode(property_)