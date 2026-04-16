from typing import Any, Dict, Union

from xiot_spec.typedef.constant.spec import Spec


class DescriptionCodec:
    @staticmethod
    def decode(obj: Any) -> Dict[str, str]:
        description: Dict[str, str] = {}
        if isinstance(obj, str):
            description[Spec.DESCRIPTION_EN_US] = obj
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    description[key] = value
        return description

    @staticmethod
    def encode(description: Dict[str, str]) -> Union[str, dict]:
        if len(description) == 1 and Spec.DESCRIPTION_EN_US in description:
            return description[Spec.DESCRIPTION_EN_US]
        return description.copy()