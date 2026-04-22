from typing import Dict, Optional

from xiot_core.spec.typedef.definition.urn.action_type import ActionType
from xiot_core.spec.typedef.instance.action import Action
from xiot_core.spec.typedef.instance.argument import Argument
from xiot_core.support.typedef.controller.operator.action_invoker_wrapper import ActionInvokerWrapper


class ActionController(Action):
    def __init__(self,
                 iid: int,
                 type_: ActionType,
                 description: Dict[str, str] = None,
                 in_: list[Argument] = None,
                 out: list[Argument] = None):
        super().__init__(iid, type_)
        if description is None:
            description = {}
        if in_ is None:
            in_ = []
        if out is None:
            out = []

        self._description = description
        self.arguments_in = in_
        self.arguments_out = out
        self._invoker: Optional[ActionInvokerWrapper] = None

    @property
    def invoker(self) -> Optional[ActionInvokerWrapper]:
        return self._invoker

    @invoker.setter
    def invoker(self, invoker: ActionInvokerWrapper = None):
        self._invoker = invoker