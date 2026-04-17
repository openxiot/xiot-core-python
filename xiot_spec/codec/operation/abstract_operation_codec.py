from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Any

T = TypeVar('T')
K = TypeVar('K')


class AbstractOperationCodec(ABC, Generic[T, K]):
    """抽象操作编解码器基类（对应Java AbstractOperationCodec）"""

    def decode(self, array: Optional[list]) -> list[T]:
        """解码JsonArray为对象列表"""
        if array is None:
            return []
        return [obj for obj in (self.decode_single(item) for item in array) if obj is not None]

    @abstractmethod
    def decode_single(self, o: Any) -> Optional[T]:
        """解码单个对象（抽象方法）"""
        ...

    @abstractmethod
    def encode_single(self, p: T) -> Optional[K]:
        """编码单个对象（抽象方法）"""
        ...

    def encode(self, list_: Optional[list[T]]) -> list:
        """编码对象列表为JsonArray（Python list）"""
        if list_ is None:
            return []
        return [obj for obj in (self.encode_single(item) for item in list_) if obj is not None]