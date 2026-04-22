from __future__ import annotations
from typing import Generic, TypeVar, Optional

from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.property.data.data_value import DataValue

T = TypeVar('T')

class PropertyValue(Generic[T]):
    def __init__(self):
        self._format: Optional[DataFormat] = None
        self._init_value: Optional[DataValue[T]] = None
        self._current_value: Optional[DataValue[T]] = None
        self._default_value: Optional[DataValue[T]] = None

    @classmethod
    def create(cls, format_: DataFormat[T]) -> PropertyValue[T]:
        value = cls()
        value._format = format_
        value._init_value = format_.create_default_value()
        return value

    # value 读取方法（对应Java的value()）
    @property
    def value(self) -> Optional[DataValue[T]]:
        if self._current_value is not None:
            return self._current_value
        if self._default_value is not None:
            return self._default_value
        return self._init_value

    # default_value 属性
    @property
    def default_value(self) -> Optional[DataValue[T]]:
        return self._default_value

    @default_value.setter
    def default_value(self, v: DataValue[T]) -> None:
        self._default_value = v

    def update(self, value: DataValue[T]) -> None:
        if value is None:
            raise ValueError("DataValue is null")
        if self._format and not self._format.check(value):
            raise ValueError(
                f"DataFormat is: {self._format}, Illegal Value: {value.__class__.__name__}"
            )
        self._current_value = value