from typing import Dict, Optional, Generic, TypeVar

from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.property.data.data_value import DataValue

T = TypeVar('T')

class ValueDefinition(Generic[T]):
    def __init__(self,
                 value: DataValue[T] = None,
                 description: Dict[str, str] = None,
                 fmt: DataFormat = None,
                 raw_value: object = None):
        self._value: Optional[DataValue[T]] = None
        self._description: Dict[str, str] = description or {}

        if value is not None:
            self._value = value
        elif fmt is not None and raw_value is not None:
            self._value = fmt.create_value(raw_value)
            if self._value is None:
                raise ValueError("value invalid")

    @property
    def value(self) -> Optional[DataValue[T]]:
        return self._value

    @value.setter
    def value(self, value: DataValue[T]) -> None:
        self._value = value

    @property
    def description(self) -> dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Dict[str, str]) -> None:
        self._description = description

    def get_value(self) -> T:
        if self._value is None:
            raise ValueError("value is None")
        return self._value.raw_value()