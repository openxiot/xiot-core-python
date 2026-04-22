from __future__ import annotations

from typing import Dict, Any

from xiot_core.spec.typedef.status.abstract_status import AbstractStatus


class StatusCodec:
    """状态编解码器（对应Java StatusCodec）"""

    @staticmethod
    def decode_single(obj: Dict[str, Any]) -> AbstractStatus:
        """解码字典为AbstractStatus"""
        status = obj.get("status", 0)
        description = obj.get("description", "description")
        return AbstractStatus(status, description)

    @staticmethod
    def encode_single(status: AbstractStatus) -> Dict[str, Any]:
        """编码AbstractStatus为字典"""
        o = {
            "status": status.status,
            "description": status.description
        }
        return o