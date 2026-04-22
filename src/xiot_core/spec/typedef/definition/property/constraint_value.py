from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .data.data_value import DataValue

T = TypeVar('T')

class ConstraintValue(ABC, Generic[T]):
    @abstractmethod
    def validate(self, value: DataValue[T]) -> bool:
        pass