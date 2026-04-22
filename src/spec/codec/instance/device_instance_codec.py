from typing import Dict, Any

from src.spec.codec.definition.description_codec import DescriptionCodec
from src.spec.codec.instance.service_codec import ServiceCodec
from src.spec.typedef.constant.spec import Spec
from src.spec.typedef.definition.urn.device_type import DeviceType
from src.spec.typedef.instance.device_instance import DeviceInstance


class DeviceInstanceCodec:
    @staticmethod
    def decode(obj: Dict[str, Any]) -> DeviceInstance:
        type_str = obj.get(Spec.TYPE, "")
        type_ = DeviceType.parse(type_str)
        description = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION, {}))
        services = ServiceCodec.decode_array(obj.get(Spec.SERVICES))
        device =  DeviceInstance(type_)
        device.description = description
        device.services = services
        return device

    @staticmethod
    def encode(device: DeviceInstance) -> Dict[str, Any]:
        o: Dict[str, Any] = {
            Spec.TYPE: str(device.type)
        }

        if len(device.description) > 0:
            o[Spec.DESCRIPTION] = DescriptionCodec.encode(device.description)

        services: list[Dict[str, Any]] = []
        for service in device.services.values():
            services.append(ServiceCodec.encode(service))
        o[Spec.SERVICES] = services

        return o