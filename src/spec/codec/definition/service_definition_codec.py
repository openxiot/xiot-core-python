from typing import Dict

from src.spec.codec.definition.description_codec import DescriptionCodec
from src.spec.codec.definition.type.action_type_codec import ActionTypeCodec
from src.spec.codec.definition.type.event_type_codec import EventTypeCodec
from src.spec.codec.definition.type.property_type_codec import PropertyTypeCodec
from src.spec.typedef.constant.spec import Spec
from src.spec.typedef.definition.service_definition import ServiceDefinition
from src.spec.typedef.definition.urn.service_type import ServiceType


class ServiceDefinitionCodec:
    @staticmethod
    def decode_list(array: list[dict]) -> list[ServiceDefinition]:
        return [ServiceDefinitionCodec.decode(obj) for obj in array]

    @staticmethod
    def encode_list(list_: list[ServiceDefinition]) -> list[dict]:
        return [ServiceDefinitionCodec.encode(def_) for def_ in list_]

    @staticmethod
    def decode(obj: dict) -> ServiceDefinition:
        type_str = obj.get(Spec.TYPE, "")
        type_ = ServiceType.parse(type_str)
        desc = DescriptionCodec.decode(obj.get(Spec.DESCRIPTION))

        req_props = PropertyTypeCodec.decode(obj.get(Spec.REQUIRED_PROPERTIES))
        opt_props = PropertyTypeCodec.decode(obj.get(Spec.OPTIONAL_PROPERTIES))
        req_actions = ActionTypeCodec.decode(obj.get(Spec.REQUIRED_ACTIONS))
        opt_actions = ActionTypeCodec.decode(obj.get(Spec.OPTIONAL_ACTIONS))
        req_events = EventTypeCodec.decode(obj.get(Spec.REQUIRED_EVENTS))
        opt_events = EventTypeCodec.decode(obj.get(Spec.OPTIONAL_EVENTS))

        return ServiceDefinition(
            type_, desc, req_props, opt_props,
            req_actions, opt_actions, req_events, opt_events
        )

    @staticmethod
    def encode(def_: ServiceDefinition) -> dict:
        obj: Dict[str, object] = {Spec.TYPE: str(def_.type), Spec.DESCRIPTION: DescriptionCodec.encode(def_.description)}

        req_props = def_.required_properties
        if req_props:
            obj[Spec.REQUIRED_PROPERTIES] = PropertyTypeCodec.encode(req_props)

        opt_props = def_.optional_properties
        if opt_props:
            obj[Spec.OPTIONAL_PROPERTIES] = PropertyTypeCodec.encode(opt_props)

        req_actions = def_.required_actions
        if req_actions:
            obj[Spec.REQUIRED_ACTIONS] = ActionTypeCodec.encode(req_actions)

        opt_actions = def_.optional_actions
        if opt_actions:
            obj[Spec.OPTIONAL_ACTIONS] = ActionTypeCodec.encode(opt_actions)

        req_events = def_.required_events
        if req_events:
            obj[Spec.REQUIRED_EVENTS] = EventTypeCodec.encode(req_events)

        opt_events = def_.optional_events
        if opt_events:
            obj[Spec.OPTIONAL_EVENTS] = EventTypeCodec.encode(opt_events)

        return obj