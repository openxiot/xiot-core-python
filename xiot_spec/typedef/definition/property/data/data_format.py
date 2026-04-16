from __future__ import annotations

from enum import Enum
from typing import Type, Optional, Any

from xiot_spec.typedef.definition.property.data.data_value import DataValue
from xiot_spec.typedef.definition.property.data.value.vbool import Vbool
from xiot_spec.typedef.definition.property.data.value.vcombination import Vcombination
from xiot_spec.typedef.definition.property.data.value.vfloat import Vfloat
from xiot_spec.typedef.definition.property.data.value.vhex import Vhex
from xiot_spec.typedef.definition.property.data.value.vint16 import Vint16
from xiot_spec.typedef.definition.property.data.value.vint32 import Vint32
from xiot_spec.typedef.definition.property.data.value.vint64 import Vint64
from xiot_spec.typedef.definition.property.data.value.vint8 import Vint8
from xiot_spec.typedef.definition.property.data.value.vstring import Vstring
from xiot_spec.typedef.definition.property.data.value.vuint16 import Vuint16
from xiot_spec.typedef.definition.property.data.value.vuint32 import Vuint32
from xiot_spec.typedef.definition.property.data.value.vuint8 import Vuint8


class DataFormat(Enum):
    """对应 Java 的 DataFormat 枚举类"""
    UNKNOWN = "unknown"
    BOOL = "bool"
    UINT8 = "uint8"
    UINT16 = "uint16"
    UINT32 = "uint32"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    FLOAT = "float"
    STRING = "string"
    HEX = "hex"
    COMBINATION = "combination"

    def __str__(self) -> str:
        """重写 toString 方法"""
        return self.value

    @classmethod
    def from_str(cls, s: str) -> DataFormat:
        """对应 Java 的 from 方法"""
        for fmt in cls:
            if str(fmt) == s:
                return fmt
        raise ValueError(f"DataFormat invalid: {s}")

    def check(self, value: DataValue[Any]) -> bool:
        """检查 DataValue 类型是否匹配"""
        cls = self.get_class()
        if cls is None:
            return False
        return isinstance(value, cls)

    def check_min_max(self, min_val: DataValue[Any], max_val: DataValue[Any], step: Optional[DataValue[Any]]) -> bool:
        """对应 Java 的 check(min, max, step) 方法"""
        return min_val.less_equals(max_val)

    def validate(self, value: DataValue[Any], min_val: DataValue[Any], max_val: DataValue[Any], step: Optional[DataValue[Any]]) -> bool:
        """验证值是否符合 min/max/step 规则"""
        if step is None:
            return value.validate(min_val, max_val)
        return value.validate_with_step(min_val, max_val, step)

    def get_java_row_name(self) -> str:
        """获取 Java 基础类型名"""
        mapping = {
            DataFormat.BOOL: "boolean",
            DataFormat.UINT8: "int",
            DataFormat.UINT16: "int",
            DataFormat.UINT32: "int",
            DataFormat.INT8: "int",
            DataFormat.INT16: "int",
            DataFormat.INT32: "int",
            DataFormat.INT64: "long",
            DataFormat.FLOAT: "float",
            DataFormat.STRING: "string",
            DataFormat.HEX: "string",
            DataFormat.COMBINATION: "object",
        }
        return mapping.get(self, "unknown")

    def get_java_class_name(self) -> str:
        """获取 Java 包装类名"""
        mapping = {
            DataFormat.BOOL: "Boolean",
            DataFormat.UINT8: "Integer",
            DataFormat.UINT16: "Integer",
            DataFormat.INT8: "Integer",
            DataFormat.INT16: "Integer",
            DataFormat.INT32: "Integer",
            DataFormat.UINT32: "Long",
            DataFormat.INT64: "Long",
            DataFormat.FLOAT: "Double",
            DataFormat.STRING: "String",
            DataFormat.HEX: "String",
            DataFormat.COMBINATION: "Object",
        }
        return mapping.get(self, "unknown")

    def get_java_class(self) -> Type[DataValue[Any]]:
        """获取对应的 DataValue 子类"""
        cls = self.get_class()
        if cls is None:
            raise RuntimeError("DataFormat invalid")
        return cls

    def create_object_value(self, string: str) -> Any:
        """从字符串创建对应类型的原始值"""
        try:
            if self == DataFormat.BOOL:
                return self._boolean_value_of(string)
            elif self in (DataFormat.UINT8, DataFormat.UINT16, DataFormat.UINT32,
                          DataFormat.INT8, DataFormat.INT16, DataFormat.INT32, DataFormat.INT64):
                return int(string)
            elif self == DataFormat.FLOAT:
                if string == "0":
                    string = "0.0f"
                return float(string.replace("f", ""))
            elif self == DataFormat.STRING:
                return string
            elif self == DataFormat.HEX:
                return int(string, 16)
            else:
                raise ValueError(f"createObjectValue failed, invalid type: {self}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"createObjectValue failed: {e}") from e

    def create_default_value(self) -> DataValue[Any]:
        """创建默认值的 DataValue 实例"""
        cls = self.get_class()
        if cls is None:
            raise ValueError(f"createObjectValue failed, invalid type: {self}")
        return cls()

    def create_value(self, value: Any) -> Optional[DataValue[Any]]:
        """从原始值创建 DataValue 实例"""
        cls = self.get_class()
        if cls is None:
            raise ValueError(f"createValue failed, invalid type: {self}")
        return cls.value_of(value)

    def get_class(self) -> type[Vbool] | type[Vuint8] | type[Vuint16] | type[Vuint32] | type[Vint8] | type[Vint16] | \
                           type[Vint32] | type[Vint64] | type[Vfloat] | type[Vstring] | None | Any:
        type_mapping = {
            DataFormat.BOOL: Vbool,
            DataFormat.UINT8: Vuint8,
            DataFormat.UINT16: Vuint16,
            DataFormat.UINT32: Vuint32,
            DataFormat.INT8: Vint8,
            DataFormat.INT16: Vint16,
            DataFormat.INT32: Vint32,
            DataFormat.INT64: Vint64,
            DataFormat.FLOAT: Vfloat,
            DataFormat.STRING: Vstring,
            DataFormat.HEX: Vhex,
            DataFormat.COMBINATION: Vcombination,
        }
        return type_mapping.get(self)

    @staticmethod
    def _boolean_value_of(string: str) -> bool:
        if not string:
            return False
        v = string.upper()  # ✅ 修复 165 行
        if v in ("1", "YES", "TRUE"):
            return True
        if v in ("0", "NO", "FALSE"):
            return False
        raise ValueError(f"BooleanValueOf failed: {string}")