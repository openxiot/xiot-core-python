from typing import Dict


class UrnNamespace:
    """URN 命名空间单例类"""
    _instance = None
    _namespaces: Dict[str, str]

    def __new__(cls):
        if cls._instance is None:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_namespaces()
        return cls._instance

    def _init_namespaces(self) -> None:
        """初始化命名空间映射"""
        self._namespaces = {
            "homekit-spec": "-0000-1000-8000-0026BB765291"
        }

    @staticmethod
    def get_instance() -> "UrnNamespace":
        """获取单例实例"""
        return UrnNamespace()

    def get_suffix_uuid(self, namespace: str) -> str:
        """获取命名空间对应的UUID后缀"""
        return self._namespaces.get(namespace, "")