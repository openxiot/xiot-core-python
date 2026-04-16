from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Protocol

T = TypeVar('T')

# 定义 Protocol 描述 DataValue 的核心特征
class DataValueProtocol(Protocol):
    def raw_value(self) -> Any: ...

# E 绑定到实现 DataValueProtocol 的类型（等价于 DataValue[Any]）
E = TypeVar('E', bound=DataValueProtocol)

class DataValue(ABC, Generic[T]):
    """对应 Java 的抽象类 DataValue<T>"""

    def less_equals(self: DataValue[T], max_value: E) -> bool:
        raise RuntimeError("not implemented!")

    def validate(self: DataValue[T], min_val: E, max_val: E) -> bool:
        raise RuntimeError("not implemented!")

    def validate_with_step(self: DataValue[T], min_val: E, max_val: E, step: E) -> bool:
        raise RuntimeError("not implemented!")

    @abstractmethod
    def raw_value(self) -> T:
        pass