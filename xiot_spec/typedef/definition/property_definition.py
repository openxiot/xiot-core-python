from typing import Generic, TypeVar, Optional, Dict, Any

from xiot_spec.typedef.definition.property.access import Access
from xiot_spec.typedef.definition.property.constraint_value import ConstraintValue
from xiot_spec.typedef.definition.property.data.data_format import DataFormat
from xiot_spec.typedef.definition.property.data.data_value import DataValue
from xiot_spec.typedef.definition.urn.property_type import PropertyType

T = TypeVar('T')

class PropertyDefinition(Generic[T]):
    def __init__(self, type_: Optional[PropertyType] = None,
                 description: Optional[Dict[str, str]] = None,
                 access: Optional[Access] = None,
                 format_: DataFormat = DataFormat.UNKNOWN,
                 constraint_value: Optional[ConstraintValue[T]] = None,
                 unit: Optional[str] = None):
        self._type = type_
        self._description = description if description is not None else {}
        self._access = access if access is not None else Access()
        self._format = format_
        self._constraint_value = constraint_value
        self._unit = unit
        self._members: list[PropertyType] = []

    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, description: Dict[str, str]) -> None:
        self._description = description

    @property
    def access(self) -> Access:
        return self._access

    @access.setter
    def access(self, access: Access) -> None:
        self._access = access

    @property
    def readable(self) -> bool:
        return self._access.is_readable()

    @readable.setter
    def readable(self, readable: bool) -> None:
        self._access.set_readable(readable)

    @property
    def writable(self) -> bool:
        return self._access.is_writable()

    @writable.setter
    def writable(self, writable: bool) -> None:
        self._access.set_writable(writable)

    @property
    def notifiable(self) -> bool:
        return self._access.is_notifiable()

    @notifiable.setter
    def notifiable(self, notifiable: bool) -> None:
        self._access.set_notifiable(notifiable)

    @property
    def type(self) -> Optional[PropertyType]:
        return self._type

    @type.setter
    def type(self, type_: PropertyType) -> None:
        self._type = type_

    @property
    def format(self) -> DataFormat:
        return self._format

    @format.setter
    def format(self, format_: DataFormat) -> None:
        self._format = format_

    @property
    def unit(self) -> Optional[str]:
        return self._unit

    @unit.setter
    def unit(self, unit: str) -> None:
        self._unit = unit

    @property
    def members(self) -> list[PropertyType]:
        return self._members

    @members.setter
    def members(self, members: list[PropertyType]) -> None:
        self._members = members

    @property
    def constraint_value(self) -> Optional[ConstraintValue[T]]:
        return self._constraint_value

    @constraint_value.setter
    def constraint_value(self, constraint_value: ConstraintValue[T]) -> None:
        self._constraint_value = constraint_value

    def validate(self, value: Optional[DataValue[T]]) -> bool:
        if value is None:
            print("property value validate failed, value is null")
            return False

        expected_cls = self._format.get_java_class()
        if not isinstance(value, expected_cls):
            print(f"property value validate failed, expect format: {expected_cls.__name__} "
                  f"but value.format: {value.__class__.__name__}")
            return False

        return self._constraint_value is None or self._constraint_value.validate(value)

    def __hash__(self) -> int:
        prime = 31
        result = 1
        result = prime * result + (0 if self._type is None else hash(self._type))
        return result

    def __eq__(self, other: Any) -> bool:
        if self is other:
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        return self._type == other._type