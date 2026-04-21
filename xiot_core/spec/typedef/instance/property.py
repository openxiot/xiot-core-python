from typing import Generic, TypeVar, Dict, Optional

from .property_value import PropertyValue
from ..definition.property.access import Access
from ..definition.property.constraint_value import ConstraintValue
from ..definition.property.data.data_format import DataFormat
from ..definition.property.data.data_value import DataValue
from ..definition.urn.property_type import PropertyType
from ..operation.property_operation import PropertyOperation
from ..status.abstract_status import IotError
from ..status.status import Status

T = TypeVar('T')

class Property(Generic[T]):
    def __init__(
        self,
        iid: int = 0,
        type_: Optional[PropertyType] = None,
        description: Optional[Dict[str, str]] = None,
        access: Access = Access(),
        fmt: DataFormat = DataFormat.INT8,
        constraint: Optional[ConstraintValue[T]] = None,
        unit: Optional[str] = None,
        other: Optional["Property"] = None,
    ):
        self._iid = iid
        self._type = type_
        self._description = description or {}
        self._access = access
        self._format = fmt
        self._constraint = constraint
        self._unit = unit
        self._members: list[int] = []
        self._value = PropertyValue.create(fmt)
        if other is not None:
            self._iid = other._iid
            self._type = other._type
            self._description = other._description
            self._access = other._access
            self._format = other._format
            self._constraint = other._constraint
            self._unit = other._unit
            self._members = other._members
            self._value = other._value

    # ------------------------------
    # Getter / Setter
    # ------------------------------
    @property
    def iid(self) -> int:
        return self._iid

    @iid.setter
    def iid(self, value: int) -> None:
        self._iid = value

    @property
    def type(self) -> Optional[PropertyType]:
        return self._type

    @type.setter
    def type(self, value: PropertyType) -> None:
        self._type = value

    @property
    def description(self) -> Dict[str, str]:
        return self._description

    @description.setter
    def description(self, value: Dict[str, str]) -> None:
        self._description = value

    @property
    def access(self) -> Optional[Access]:
        return self._access

    @access.setter
    def access(self, value: Access) -> None:
        self._access = value

    def readable(self) -> bool:
        return self._access.is_readable()

    def writable(self) -> bool:
        return self._access.is_writable()

    def notifiable(self) -> bool:
        return self._access.is_notifiable()

    @property
    def format(self) -> DataFormat:
        return self._format

    @format.setter
    def format(self, value: DataFormat) -> None:
        self._format = value

    @property
    def unit(self) -> Optional[str]:
        return self._unit

    @unit.setter
    def unit(self, value: str) -> None:
        self._unit = value

    @property
    def members(self) -> list[int]:
        return self._members

    @members.setter
    def members(self, value: list[int]) -> None:
        self._members = value

    @property
    def current_value(self) -> Optional[DataValue[T]]:
        return self._value.value

    @property
    def constraint(self) -> Optional[ConstraintValue[T]]:
        return self._constraint

    @constraint.setter
    def constraint(self, value: Optional[ConstraintValue[T]]) -> None:
        self._constraint = value

    # ------------------------------
    # 核心业务方法
    # ------------------------------
    def initialize_value(self) -> None:
        """对应Java的initializeValue方法"""
        self._value = PropertyValue.create(self._format)

    def validate(self, value: Optional[DataValue[T]]) -> bool:
        """验证值是否合法"""
        if value is None:
            print("property value validate failed, value is null")
            return False

        expected_type = self._format.get_python_class()
        if not isinstance(value, expected_type):
            print(
                f"property value validate failed, respect format: {expected_type.__name__}, "
                f"but value.format: {type(value).__name__}"
            )
            return False

        if self._constraint is None:
            return True
        return self._constraint.validate(value)

    @property
    def default_value(self) -> Optional[DataValue[T]]:
        """获取默认值"""
        return self._value.default_value

    @default_value.setter
    def default_value(self, value: object) -> None:
        """设置默认值"""
        if value is not None:
            data_value = self._format.create_value(value)
            if self.validate(data_value):
                self._value.default_value = data_value
            else:
                print(f"property default value validate failed, value: {value}")

    def try_set_value(self, value: object) -> bool:
        """尝试设置值（不抛异常）"""
        data_value = self._format.create_value(value)
        return self.set_data_value(data_value, write=False)

    def set_value(self, value: object) -> bool:
        """设置值"""
        data_value = self._format.create_value(value)
        return self.set_data_value(data_value, write=True)

    def set_value_for_operation(self, operation: PropertyOperation) -> None:
        """为操作设置值"""
        try:
            data_value = self._format.create_value(operation.value())
            self.set_data_value_with_exception(data_value, write=True)
            operation.status = Status.COMPLETED
        except IotError as e:
            operation.status = e.status
            operation.description = e.description

    def set_data_value(self, new_value: Optional[DataValue[T]], write: bool) -> bool:
        """设置数据值（无异常）"""
        if new_value is None:
            print(f"setDataValue failed, newValue is null, type: {self._type}, iid: {self._iid}")
            return False

        if not self.validate(new_value):
            return False

        if write:
            self._value.update(new_value)

        return True

    def set_data_value_with_exception(self, new_value: Optional[DataValue[T]], write: bool) -> None:
        """设置数据值（抛异常）"""
        if new_value is None:
            raise IotError(Status.PROPERTY_VALUE_ERROR, "property value is null")

        if not self.validate(new_value):
            raise IotError(Status.PROPERTY_VALUE_INVALID, f"property value invalid: {new_value.raw_value}")

        if write:
            self._value.update(new_value)

    def __lt__(self, other: 'Property[T]') -> bool:
        """实现比较逻辑（替代compareTo）"""
        if not isinstance(other, Property):
            return NotImplemented
        return self._iid < other._iid

    def get_value(self) -> Optional[T]:
        """获取原始值"""
        if self._format == DataFormat.COMBINATION:
            current_val = self.current_value
            if current_val and isinstance(current_val.raw_value, dict):
                return self.value_of(current_val.raw_value)
            return None
        current_val = self.current_value
        return current_val.raw_value if current_val else None

    def put(self, value: T) -> None:
        """强制设置值（忽略可写性）"""
        if self._format == DataFormat.COMBINATION:
            if not self.set_value(self.to_map(value)):
                raise ValueError("PROPERTY_VALUE_INVALID")
        else:
            if not self.set_value(value):
                raise ValueError("PROPERTY_VALUE_INVALID")

    def put_value(self, value: object) -> None:
        """强制设置值（通用版）"""
        if not self.set_value(value):
            raise ValueError("PROPERTY_VALUE_INVALID")

    def value_of(self, value: Dict[int, object]) -> Optional[T]:
        """构造组合属性值（子类实现）"""
        return None

    def to_map(self, value: T) -> Dict[int, object]:
        """转换为Map（子类实现）"""
        return {}