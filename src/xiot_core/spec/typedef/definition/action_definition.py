from typing import Optional, Dict

from xiot_core.spec.typedef.definition.argument_definition import ArgumentDefinition
from xiot_core.spec.typedef.definition.urn.action_type import ActionType


class ActionDefinition:
    def __init__(self, type_: ActionType,
                 description: Optional[Dict[str, str]] = None,
                 in_args: Optional[list[ArgumentDefinition]] = None,
                 out_args: Optional[list[ArgumentDefinition]] = None):
        self._type = type_
        self._description = description if description is not None else {}
        self._in: list[ArgumentDefinition] = []
        self._out: list[ArgumentDefinition] = []
        if in_args:
            self._in.extend(in_args)
        if out_args:
            self._out.extend(out_args)

    @property
    def type(self) -> ActionType:
        return self._type

    @type.setter
    def type(self, type_: ActionType) -> None:
        self._type = type_

    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Dict[str, str]) -> None:
        self._description = description

    @property
    def in_args(self) -> list[ArgumentDefinition]:
        return self._in

    @property
    def out_args(self) -> list[ArgumentDefinition]:
        return self._out