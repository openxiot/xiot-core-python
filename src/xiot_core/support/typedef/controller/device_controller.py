from typing import Dict, Generic, TypeVar, Optional, Callable, Awaitable

from xiot_core.spec.typedef.definition.urn.urn import Urn
from xiot_core.spec.typedef.instance.device_instance import DeviceInstance
from xiot_core.spec.typedef.operation.action_operation import ActionOperation
from xiot_core.spec.typedef.operation.event_operation import EventOperation
from xiot_core.spec.typedef.operation.property_operation import PropertyOperation
from xiot_core.spec.typedef.status.abstract_status import IotError
from xiot_core.spec.typedef.status.status import Status
from xiot_core.spec.typedef.summary.summary import Summary
from xiot_core.support.typedef.controller.operator.action_invoker_wrapper import ActionInvokerWrapper
from xiot_core.support.typedef.controller.operator.property_setter_wrapper import PropertySetterWrapper
from xiot_core.support.typedef.controller.service_controller import ServiceController

T = TypeVar('T')

class DeviceController(Generic[T], DeviceInstance):
    def __init__(self, type_: Urn, description: Dict[str, str] = None, services: list[ServiceController] = None):
        super().__init__(type_ = type_, description_ = description, services_ = services)
        self._did: str = "?"
        self._additional: Optional[T] = None
        self._summary: Optional[Summary] = None

    def did(self, did: str = None) -> Optional[str]:
        if did is not None:
            self._did = did
        return self._did

    @property
    def summary(self) -> Optional[Summary]:
        return self._summary

    @summary.setter
    def summary(self, summary: Summary = None) -> None:
        self._summary = summary

    @property
    def additional(self) -> Optional[T]:
        return self._additional

    @additional.setter
    def additional(self, additional: T = None) -> None:
        self._additional = additional

    def handle_property_changed(self, ops: list[PropertyOperation]) -> None:
        for o in ops:
            self.handle_single_property_changed(o)

    def handle_single_property_changed(self, o: PropertyOperation) -> None:
        service = self._services.get(o.siid)
        if isinstance(service, ServiceController):
            service.handle_property_changed(o)
        else:
            raise IotError(Status.SERVICE_NOT_FOUND, f"handlePropertyChanged, service not found: {o.siid}")

    def handle_event_occurred(self, e: EventOperation) -> None:
        service = self._services.get(e.siid)
        if isinstance(service, ServiceController):
            service.handle_event_occurred(e)
        else:
            raise ValueError(f"handleEventOccurred, service not found: {e.siid}")

    def set_operator(
            self,
            setter: Callable[[PropertyOperation], Awaitable[PropertyOperation]],
            invoker: Callable[[ActionOperation], Awaitable[ActionOperation]]
    ) -> None:
        for siid, service in self._services.items():
            setter_wrapper = PropertySetterWrapper(did = self._did, siid = siid, operator=setter)
            invoker_wrapper = ActionInvokerWrapper(did = self._did, siid = siid, operator=invoker)

            if isinstance(service, ServiceController):
                for piid, property_ in service.properties().items():
                    property_.setter = setter_wrapper

                for aiid, action in service.actions().items():
                    action.invoker = invoker_wrapper

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, DeviceController):
            return False
        return self._did == other._did

    def __hash__(self) -> int:
        return hash(self._did)