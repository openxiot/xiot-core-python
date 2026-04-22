from typing import Dict, Any, TypeVar, Generic

from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.urn.urn import Urn
from xiot_core.spec.typedef.definition.urn.urn_type import UrnType
from xiot_core.support.codec.controller.service_controller_codec import ServiceControllerCodec
from xiot_core.support.typedef.controller.device_controller import DeviceController

T = TypeVar('T')

class DeviceControllerCodec(Generic[T]):
    @staticmethod
    def decode(obj: Dict[str, Any]) -> DeviceController[T]:
        type_str = obj.get(Spec.TYPE, "")
        type_ = Urn(types = [UrnType.DEVICE, UrnType.GROUP], string = type_str)
        description = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION, {}))
        services = ServiceControllerCodec.decode(obj.get(Spec.SERVICES, []))
        return DeviceController[T](type_ = type_, description = description, services = services)