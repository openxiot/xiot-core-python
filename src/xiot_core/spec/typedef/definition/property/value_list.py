from typing import List, Generic, TypeVar

from xiot_core.spec.typedef.definition.property.constraint_value import ConstraintValue
from xiot_core.spec.typedef.definition.property.data.data_value import DataValue
from xiot_core.spec.typedef.definition.property.value_definition import ValueDefinition

T = TypeVar('T')

class ValueList(ConstraintValue[T], Generic[T]):
    def __init__(self, values: List[ValueDefinition[T]]):
        self._values = values

    def validate(self, value: DataValue[T]) -> bool:
        for v in self._values:
            if v.value == value:
                return True
        return False

    @property
    def values(self) -> List[ValueDefinition[T]]:
        return self._values