from typing import Dict, Generic, TypeVar, Optional, Callable

from xiot_core.spec.typedef.definition.property.access import Access
from xiot_core.spec.typedef.definition.property.data.data_format import DataFormat
from xiot_core.spec.typedef.definition.urn.property_type import PropertyType
from xiot_core.spec.typedef.instance.property import Property
from xiot_core.spec.typedef.operation.property_operation import PropertyOperation
from xiot_core.support.typedef.controller.operator.property_setter_wrapper import PropertySetterWrapper

T = TypeVar('T')

class PropertyController(Generic[T], Property[T]):
    def __init__(self,
                 other: Optional[Property[T]] = None,
                 iid: int = 0,
                 type_: Optional[PropertyType] = None,
                 access: Access = Access(),
                 fmt: DataFormat = DataFormat.INT8,
                 ):
        super().__init__(other = other, iid = iid, type_ = type_, access = access, fmt = fmt)
        self._setter: Optional[PropertySetterWrapper] = None
        self._observers: Dict[str, Callable[[T], None]] = {}

    @classmethod
    def from_iid_type_access_format(cls, iid: int, type_: PropertyType, access: Access, format_: DataFormat):
        instance = cls()
        instance.iid = iid
        instance.type = type_
        instance.description = None
        instance.access = access
        instance.format = format_
        instance.constraint = None
        instance.unit = None
        instance.members = None
        instance.initialize_value()
        return instance

    @classmethod
    def from_property(cls, property_: Property[T]):
        instance = cls()
        instance.iid = property_.iid
        instance.type = property_.type
        instance.description = property_.description
        instance.format = property_.format
        instance.access = property_.access
        instance.constraint = property_.constraint
        instance.unit = property_.unit
        instance.members = property_.members
        instance.initialize_value()
        return instance

    def add_observer(self, observer: Callable[[T], None]) -> None:
        self._observers[str(observer)] = observer

    def remove_observer(self, observer: Callable[[T], None]) -> None:
        self._observers.pop(str(observer), None)

    def handle_property_changed(self, o: PropertyOperation) -> None:
        self.set_value_for_operation(o)
        if o.is_completed:
            for observer in self._observers.values():
                observer(self.get_value())

    @property
    def setter(self) -> Optional[PropertySetterWrapper]:
        return self._setter

    @setter.setter
    def setter(self, setter: PropertySetterWrapper) -> None:
        self._setter = setter

    async def set(self, value: T):
        if not self.writable():
            raise IOError("property cannot write")

        if self._setter is None:
            raise NotImplementedError("property set: cannot implemented")

        if self.format == DataFormat.COMBINATION:
            await self._setter.call(self.iid, self.to_map(value))
        else:
            await self._setter.call(self.iid, value)

    def set_with_callback(self, value: T, success: Callable[[T], None], error: Callable[[Exception], None]) -> None:
        async def _set():
            result = await self.set(value)
            success(result)

    # 以下为原注释掉的方法，保留结构
    # def get(self) -> T:
    #     if self.format() == DataFormat.COMBINATION:
    #         raw_value = self.current_value().raw_value()
    #         if isinstance(raw_value, dict):
    #             return self.valueOf(raw_value)
    #         else:
    #             return None
    #     else:
    #         return self.current_value().raw_value()

    def put_value(self, value: Optional[object]):
        if value is None:
            raise ValueError("value is None")

        if not self.set_value(value):
            raise ValueError("PROPERTY_VALUE_INVALID")

    def value_of(self, value: Dict[int, object]) -> T:
        return None

    def to_map(self, value: Optional[T]) -> Dict[int, object]:
        return {}