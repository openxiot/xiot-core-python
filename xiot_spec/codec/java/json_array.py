# 模拟 Vert.x JsonArray（Python 中用 list 替代，封装类型检查）
import json
from typing import Optional, Any, Iterator, Self


class JsonArray:
    """
    模拟 Vert.x JsonArray 核心行为
    支持: 空值处理、流式操作、列表转换、JSON序列化/反序列化
    """
    def __init__(self, lst: Optional[list[Any]] = None):
        self._list: list[Any] = lst if lst is not None else []

    def stream(self) -> Iterator[Any]:
        """模拟Java stream() 方法，返回迭代器"""
        return iter(self._list)

    def to_list(self) -> list[Any]:
        """转换为原生Python列表"""
        return list(self._list)

    def add(self, value: Any) -> Self:
        """模拟add方法，链式调用"""
        self._list.append(value)
        return self

    def is_empty(self) -> bool:
        """判断是否为空"""
        return len(self._list) == 0

    def size(self) -> int:
        """获取元素数量"""
        return len(self._list)

    def get(self, index: int) -> Any:
        """按索引获取元素"""
        return self._list[index]

    def to_json(self) -> str:
        """序列化为JSON字符串"""
        return json.dumps(self._list)

    @classmethod
    def from_list(cls, lst: Optional[list[Any]]) -> Optional[Self]:
        if lst is None:
            return None
        return cls(lst)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """从JSON字符串反序列化"""
        return cls(json.loads(json_str))

    def __iter__(self) -> Iterator[Any]:
        return iter(self._list)

    def __repr__(self) -> str:
        return f"JsonArray({self._list})"