from __future__ import annotations
from typing import List, Optional, Dict, Any, Collection
from shadow_codec import ShadowCodec


class DeviceShadowCodec:
    """设备影子编解码器（对应Java DeviceShadowCodec）"""

    @staticmethod
    def decode_array(array: Optional[list]) -> List[DeviceShadow]:
        """解码列表为DeviceShadow列表"""
        list_ = []
        if array is not None:
            for item in array:
                if isinstance(item, dict):
                    list_.append(DeviceShadowCodec.decode_single(item))
        return list_

    @staticmethod
    def decode_single(obj: Dict[str, Any]) -> DeviceShadow:
        """解码单个字典为DeviceShadow"""
        did = obj.get("did")
        array = obj.get("shadows", [])
        return DeviceShadow(did, ShadowCodec.decode_array(array))

    @staticmethod
    def encode_collection(devices: Collection[DeviceShadow]) -> list:
        """编码DeviceShadow集合为列表"""
        list_ = []
        for m in devices:
            list_.append(DeviceShadowCodec.encode_single(m))
        return list_

    @staticmethod
    def encode_single(device: DeviceShadow) -> Dict[str, Any]:
        """编码单个DeviceShadow为字典"""
        return {
            "did": device.did(),
            "shadows": ShadowCodec.encode_collection(device.shadows())
        }