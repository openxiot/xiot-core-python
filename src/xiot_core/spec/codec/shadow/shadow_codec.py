from __future__ import annotations
from typing import Optional, Dict, Any, Collection

from xiot_core.spec.typedef.shadow.shadow import Shadow


class ShadowCodec:
    """影子编解码器（对应Java ShadowCodec）"""

    @staticmethod
    def decode_array(array: Optional[list]) -> list[Shadow]:
        """解码列表为Shadow列表"""
        list_ = []
        if array is not None:
            for item in array:
                if isinstance(item, dict):
                    list_.append(ShadowCodec.decode_single(item))
        return list_

    @staticmethod
    def decode_single(obj: Dict[str, Any]) -> Shadow:
        """解码单个字典为Shadow"""
        siid = obj.get("siid", 0)
        piid = obj.get("piid", 0)
        value = obj.get("value")

        if isinstance(value, dict):
            value_item = value.get("value")
            if value_item is not None:
                value = value_item

        status = obj.get("status", 0)
        description = obj.get("description", "")

        shadow = Shadow.from_siid_piid_value(siid, piid, value)
        shadow.status = status
        shadow.description = description
        return shadow

    @staticmethod
    def encode_collection(shadows: Collection[Shadow]) -> list:
        """编码Shadow集合为列表"""
        list_ = []
        for m in shadows:
            list_.append(ShadowCodec.encode_single(m))
        return list_

    @staticmethod
    def encode_single(m: Shadow) -> Dict[str, Any]:
        """编码单个Shadow为字典"""
        o: Dict[str, Any]  = {
            "siid": m.siid,
            "piid": m.piid,
            "status": m.status
        }

        if m.status >= 0:
            o["value"] = m.value
        else:
            description = m.description
            if description is not None:
                o["description"] = description

        return o