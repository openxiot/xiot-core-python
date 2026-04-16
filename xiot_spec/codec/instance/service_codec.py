from typing import Dict, Any, Optional

from xiot_spec.codec.definition.description_codec import DescriptionCodec
from xiot_spec.codec.instance.action_codec import ActionCodec
from xiot_spec.codec.instance.event_codec import EventCodec
from xiot_spec.codec.instance.property_codec import PropertyCodec
from xiot_spec.typedef.constant.spec import Spec
from xiot_spec.typedef.definition.urn.service_type import ServiceType
from xiot_spec.typedef.instance.service import Service


class ServiceCodec:
    @staticmethod
    def decode_dict(obj: Dict[str, Any]) -> Service:
        iid = obj.get(Spec.IID, -1)
        type_ = ServiceType.parse(obj.get(Spec.TYPE, ""))
        description = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION, {}))
        properties = PropertyCodec.decode_array(obj.get(Spec.PROPERTIES))
        actions = ActionCodec.decode_array(obj.get(Spec.ACTIONS))
        events = EventCodec.decode_array(obj.get(Spec.EVENTS))
        service = Service(iid, type_)
        service.description = description
        service.properties = properties
        service.actions = actions
        service.events = events
        return service

    @staticmethod
    def decode_array(array: Optional[list[Any]]) -> list[Service]:
        services = []
        if not array:
            return services

        for i in range(len(array)):
            services.append(ServiceCodec.decode_dict(array[i]))
        return services

    @staticmethod
    def encode(service: Service) -> Dict[str, Any]:
        o: Dict[str, Any] = {
            Spec.IID: service.iid,
            Spec.TYPE: str(service.service_type)
        }

        if len(service.description) > 0:
            o[Spec.DESCRIPTION] = DescriptionCodec.encode(service.description)

        if len(service.properties) > 0:
            properties = []
            for prop in service.properties.values():
                properties.append(PropertyCodec.encode(prop))
            o[Spec.PROPERTIES] = properties

        if len(service.actions) > 0:
            actions = []
            for action in service.actions.values():
                actions.append(ActionCodec.encode(action))
            o[Spec.ACTIONS] = actions

        if len(service.events) > 0:
            events = []
            for event in service.events.values():
                events.append(EventCodec.encode(event))
            o[Spec.EVENTS] = events

        return o