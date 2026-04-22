from xiot_core.spec.typedef.definition.urn.property_type import PropertyType


class ArgumentDefinition:
    def __init__(self, type_: PropertyType, min_repeat: int = 1, max_repeat: int = 1):
        self._type = type_
        self._min_repeat = min_repeat
        self._max_repeat = max_repeat

    @property
    def type(self) -> PropertyType:
        return self._type

    @type.setter
    def type(self, type_: PropertyType) -> None:
        self._type = type_

    @property
    def min_repeat(self) -> int:
        return self._min_repeat

    @min_repeat.setter
    def min_repeat(self, min_: int) -> None:
        self._min_repeat = min_

    @property
    def max_repeat(self) -> int:
        return self._max_repeat

    @max_repeat.setter
    def max_repeat(self, max_: int) -> None:
        self._max_repeat = max_