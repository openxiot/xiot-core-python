from typing import Dict, Any

from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.urn.service_type import ServiceType
from xiot_core.support.codec.controller.action_controller_codec import ActionControllerCodec
from xiot_core.support.codec.controller.event_controller_codec import EventControllerCodec
from xiot_core.support.codec.controller.property_controller_codec import PropertyControllerCodec
from xiot_core.support.typedef.controller.action_controller import ActionController
from xiot_core.support.typedef.controller.event_controller import EventController
from xiot_core.support.typedef.controller.property_controller import PropertyController
from xiot_core.support.typedef.controller.service_controller import ServiceController


class ServiceControllerCodec:
    @staticmethod
    def _decode(obj: Dict[str, Any]) -> ServiceController:
        iid: int = obj.get(Spec.IID, -1)
        type_str: str = obj.get(Spec.TYPE, "")
        type_: ServiceType = ServiceType.parse(type_str)
        description: Dict[str, str] = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION))

        properties: list[PropertyController[Any]] = PropertyControllerCodec.decode(obj.get(Spec.PROPERTIES, []))
        actions: list[ActionController] = ActionControllerCodec.decode(obj.get(Spec.ACTIONS, []))
        events: list[EventController] = EventControllerCodec.decode_array(obj.get(Spec.EVENTS, []))

        return ServiceController(iid, type_, description, properties, actions, events)

    @staticmethod
    def decode(array: list[Dict[str, Any]]) -> list[ServiceController]:
        services: list[ServiceController] = []
        if array is not None:
            for item in array:
                services.append(ServiceControllerCodec._decode(item))
        return services