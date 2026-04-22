from typing import Dict, Any, Optional

from xiot_core.spec.codec.definition.description_codec import DescriptionCodec
from xiot_core.spec.codec.instance.action_codec import ActionCodec
from xiot_core.spec.codec.instance.event_codec import EventCodec
from xiot_core.spec.codec.instance.property_codec import PropertyCodec
from xiot_core.spec.typedef.constant.spec import Spec
from xiot_core.spec.typedef.definition.urn.service_type import ServiceType
from xiot_core.spec.typedef.instance.service import Service


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
            Spec.TYPE: str(service.type)
        }

        if len(service.description) > 0:
            o[Spec.DESCRIPTION] = DescriptionCodec.encode(service.description)

        if len(service.properties) > 0:
            properties = []
            for p in service.properties.values():
                properties.append(PropertyCodec.encode(p))
            o[Spec.PROPERTIES] = properties

        if len(service.actions) > 0:
            actions = []
            for a in service.actions.values():
                actions.append(ActionCodec.encode(a))
            o[Spec.ACTIONS] = actions

        if len(service.events) > 0:
            events = []
            for e in service.events.values():
                events.append(EventCodec.encode(e))
            o[Spec.EVENTS] = events

        return o