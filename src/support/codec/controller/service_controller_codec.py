from typing import Dict, Any

from src.spec.codec.definition.description_codec import DescriptionCodec
from src.spec.typedef.constant.spec import Spec
from src.spec.typedef.definition.urn.service_type import ServiceType
from src.support.codec.controller.action_controller_codec import ActionControllerCodec
from src.support.codec.controller.event_controller_codec import EventControllerCodec
from src.support.codec.controller.property_controller_codec import PropertyControllerCodec
from src.support.typedef.controller.action_controller import ActionController
from src.support.typedef.controller.event_controller import EventController
from src.support.typedef.controller.property_controller import PropertyController
from src.support.typedef.controller.service_controller import ServiceController


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