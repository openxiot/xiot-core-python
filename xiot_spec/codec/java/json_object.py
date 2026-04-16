import json
from typing import Optional, Dict, Any, Iterator, Tuple, Self

from xiot_spec.codec.java.json_array import JsonArray


class JsonObject:
    """
    模拟 Vert.x JsonObject 核心行为
    支持: 键值操作、JSON序列化/反序列化、空值处理、类型安全取值
    """
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self._map: Dict[str, Any] = data if data is not None else {}

    def put(self, key: str, value: Any):
        """模拟put方法，链式调用"""
        self._map[key] = value
        return self

    def get(self, key: str) -> Any:
        """获取指定键的值"""
        return self._map.get(key)

    def get_string(self, key: str) -> Optional[str]:
        """类型安全获取字符串"""
        value = self.get(key)
        return value if isinstance(value, str) else None

    def opt_string(self, key: str, default: str) -> str:
        """类型安全获取字符串"""
        value = self.get(key)
        if value is None:
            return default
        if isinstance(value, str):
            return value
        return default

    def get_integer(self, key: str) -> Optional[int]:
        """类型安全获取整数"""
        value = self.get(key)
        return value if isinstance(value, int) else None

    def get_boolean(self, key: str) -> Optional[bool]:
        """类型安全获取布尔值"""
        value = self.get(key)
        return value if isinstance(value, bool) else None

    def get_json_array(self, key: str) -> Optional[JsonArray]:
        """获取JsonArray类型值"""
        value = self.get(key)
        if isinstance(value, list):
            return JsonArray(value)
        elif isinstance(value, JsonArray):
            return value
        return None

    def get_json_object(self, key: str) -> Optional["JsonObject"]:
        """获取JsonObject类型值"""
        value = self.get(key)
        if isinstance(value, dict):
            return JsonObject(value)
        elif isinstance(value, JsonObject):
            return value
        return None

    def remove(self, key: str) -> Any:
        """移除指定键"""
        return self._map.pop(key, None)

    def contains_key(self, key: str) -> bool:
        """判断是否包含指定键"""
        return key in self._map

    def is_empty(self) -> bool:
        """判断是否为空"""
        return len(self._map) == 0

    def size(self) -> int:
        """获取键值对数量"""
        return len(self._map)

    def to_map(self) -> Dict[str, Any]:
        """转换为原生Python字典"""
        return dict(self._map)

    def to_json(self) -> str:
        """序列化为JSON字符串"""
        return json.dumps(self._map, ensure_ascii=False)

    @classmethod
    def from_map(cls, map_: Optional[Dict[str, Any]]) -> Optional[Self]:
        if map_ is None:
            return None
        return cls(map_)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """从JSON字符串反序列化"""
        return cls(json.loads(json_str))

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self._map.items())

    def __repr__(self) -> str:
        return f"JsonObject({self._map})"