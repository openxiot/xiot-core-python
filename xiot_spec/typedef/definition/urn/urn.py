from typing import Optional, Any

from .urn_namespace import UrnNamespace
from .urn_style import UrnStyle
from .urn_type import UrnType


class Urn:
    """URN 核心类"""
    URN: str = "urn"

    def __init__(
        self,
        ns: Optional[str] = None,
        type_: Optional[UrnType] = None,
        name: Optional[str] = None,
        value: Optional[int | str] = None,
        types: Optional[list[UrnType]] = None,
        string: Optional[str] = None,
        exception: bool = False,
        t: Optional[UrnType] = None
    ):
        # 初始化属性
        self.ns: str = ""
        self.type: UrnType = UrnType.UNDEFINED
        self.name: str = ""
        self.value: int = 0
        self.v1modified: str = ""
        self.v2modified: str = ""
        self.v2template: str = ""
        self.organization: str = ""
        self.model: str = ""
        self.version: int = 0
        self.style: UrnStyle = UrnStyle.SPEC
        self.valid: bool = True

        # 重载构造逻辑（模拟Java多构造器）
        if ns is not None and type_ is not None and name is not None and value is not None:
            if isinstance(value, str):
                self.ns = ns
                self.type = type_
                self.name = name
                self.value = int(value, 16)
            elif isinstance(value, int):
                self.ns = ns
                self.type = type_
                self.name = name
                self.value = value
        elif types is not None and string is not None:
            self._init_from_types_string(types, string, exception)
        elif t is not None and string is not None:
            self._init_from_types_string([t], string, exception)
        else:
            # 空构造器
            pass

    def _init_from_types_string(self, types: list[UrnType], string: str, exception: bool) -> None:
        """从类型列表和字符串初始化（核心解析逻辑）"""
        try:
            a = string.split(":")
            if len(a) < 5:
                self._fail(f"invalid type: {string}", exception)
                return

            if not self._init(a[0], a[1], a[2], a[3], a[4]):
                self._fail(f"invalid type: {string}", exception)
                return

            if self.type not in types:
                self._fail(f"type not matched: {string}", exception)
                return

            # 解析不同样式的URN
            if len(a) == 5:
                self.style = UrnStyle.SPEC
            elif len(a) == 6:
                self.style = UrnStyle.V1
                self.v1modified = a[5].lower()
            elif len(a) == 7:
                self.style = UrnStyle.V2
                self.v2modified = a[5].lower()
                self.version = int(a[6], 10)
            elif len(a) == 8:
                if a[7].startswith("0000"):
                    self.style = UrnStyle.V2_TEMPLATE
                    self.v2modified = a[5].lower()
                    self.version = int(a[6], 10)
                    self.v2template = a[7].lower()
                else:
                    self.style = UrnStyle.XIOT
                    self.organization = a[5].lower()
                    self.model = a[6].lower()
                    self.version = int(a[7], 10)

                    if len(self.organization) == 0:
                        self._fail("invalid urn, field: organization is empty", exception)
                        return
                    if len(self.model) == 0:
                        self._fail("invalid urn, field: model is empty", exception)
                        return
        except Exception as e:
            if exception:
                raise ValueError(f"parse urn({string}) failed: {e}") from e
            self.valid = False

    def _init(self, magic: str, ns: str, type_str: str, name: str, value_str: str) -> bool:
        """初始化核心字段"""
        if magic != self.URN:
            return False
        if not ns:
            return False
        if not type_str:
            return False
        if not name:
            return False
        if not value_str:
            return False

        self.ns = ns
        self.type = UrnType.from_string(type_str)
        self.name = name.lower()
        try:
            self.value = int(value_str, 16)
        except ValueError:
            return False
        return self.type != UrnType.UNDEFINED

    def _fail(self, msg: str, exception: bool) -> None:
        """失败处理逻辑"""
        if exception:
            raise ValueError(msg)
        self.valid = False

    # 基础属性方法
    def is_valid(self) -> bool:
        return self.valid

    def is_invalid(self) -> bool:
        return not self.valid

    def get_modified(self) -> Optional[str]:
        """获取modified字段（兼容不同样式）"""
        if self.style == UrnStyle.V1:
            return self.v1modified
        elif self.style in [UrnStyle.V2, UrnStyle.V2_TEMPLATE]:
            return self.v2modified
        return None

    def set_modified(self, modified: str) -> None:
        """设置modified字段（兼容不同样式）"""
        if self.style == UrnStyle.V1:
            self.v1modified = modified
        elif self.style in [UrnStyle.V2, UrnStyle.V2_TEMPLATE]:
            self.v2modified = modified

    def version_increase(self) -> None:
        """版本号自增"""
        self.version += 1

    def version_decrease(self) -> None:
        """版本号自减"""
        self.version -= 1

    # UUID相关方法
    def get_uuid(self, capital: bool = False) -> str:
        """获取UUID字符串"""
        fmt = "%X" if capital else "%x"
        return fmt % self.value

    def get_short_uuid(self) -> str:
        """获取短UUID"""
        if self.ns.startswith("miot-spec"):
            return "%08X" % self.value
        return "%08x" % self.value

    def get_full_uuid(self) -> str:
        """获取完整UUID"""
        suffix = UrnNamespace.get_instance().get_suffix_uuid(self.ns)
        return f"%08x{suffix}" % self.value

    # 克隆方法
    def clone(self) -> "Urn":
        """深度克隆当前Urn实例"""
        new_urn = Urn()
        new_urn.ns = self.ns
        new_urn.type = self.type
        new_urn.name = self.name
        new_urn.value = self.value
        new_urn.v1modified = self.v1modified
        new_urn.v2modified = self.v2modified
        new_urn.v2template = self.v2template
        new_urn.organization = self.organization
        new_urn.model = self.model
        new_urn.version = self.version
        new_urn.style = self.style
        new_urn.valid = self.valid
        return new_urn

    # 字符串序列化方法
    def to_string_without_version(self) -> str:
        """序列化（不含版本号）"""
        if self.style == UrnStyle.V2:
            return f"{self.URN}:{self.ns}:{self.type.value}:{self.name}:{self.get_short_uuid()}:{self.v2modified}"
        elif self.style == UrnStyle.XIOT:
            return f"{self.URN}:{self.ns}:{self.type.value}:{self.name}:{self.get_short_uuid()}:{self.organization}:{self.model}"
        return str(self)

    def __str__(self) -> str:
        """完整序列化"""
        if self.style == UrnStyle.SPEC:
            return f"{self.URN}:{self.ns}:{self.type.value}:{self.name}:{self.get_short_uuid()}"
        elif self.style == UrnStyle.V1:
            return f"{self.URN}:{self.ns}:{self.type.value}:{self.name}:{self.get_short_uuid()}:{self.v1modified}"
        elif self.style == UrnStyle.V2:
            return f"{self.URN}:{self.ns}:{self.type.value}:{self.name}:{self.get_short_uuid()}:{self.v2modified}:{self.version}"
        elif self.style == UrnStyle.V2_TEMPLATE:
            return f"{self.URN}:{self.ns}:{self.type.value}:{self.name}:{self.get_short_uuid()}:{self.v2modified}:{self.version}:{self.v2template}"
        elif self.style == UrnStyle.XIOT:
            return f"{self.URN}:{self.ns}:{self.type.value}:{self.name}:{self.get_short_uuid()}:{self.organization}:{self.model}:{self.version}"
        return ""

    # 相等性判断
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Urn):
            return False
        return (self.value == other.value
                and self.version == other.version
                and self.ns == other.ns
                and self.type == other.type
                and self.name == other.name
                and self.v1modified == other.v1modified
                and self.v2modified == other.v2modified
                and self.v2template == other.v2template
                and self.organization == other.organization
                and self.model == other.model
                and self.style == other.style)

    def __hash__(self) -> int:
        """哈希值计算"""
        return hash((
            self.ns, self.type, self.name, self.value,
            self.v1modified, self.v2modified, self.v2template,
            self.organization, self.model, self.version, self.style
        ))