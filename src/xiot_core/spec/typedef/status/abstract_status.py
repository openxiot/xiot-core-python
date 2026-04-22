from typing import Optional

from xiot_core.spec.typedef.status.status import Status


# 占位：IotError（原代码未提供完整定义，保留接口）
class IotError(Exception):
    def __init__(self, status: int, description: str):
        self.status = status
        self.description = description

class AbstractStatus:
    def __init__(self,
                 status: int = Status.COMPLETED,
                 description: Optional[str] = None):
        self._status: int = status
        self._description: Optional[str] = description

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, status: int):
        self._status = status

    def set_status_with_desc(self, status: int, description: str) -> "AbstractStatus":
        self._status = status
        self._description = description
        return self

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    def set_error(self, error: IotError) -> "AbstractStatus":  # 前置声明IotError
        self._status = error.status
        self._description = error.description
        return self

    @property
    def is_error(self) -> bool:
        return self._status < 0

    @property
    def is_not_error(self) -> bool:
        return self._status >= 0

    @property
    def is_completed(self) -> bool:
        return self._status == 0

    @property
    def is_not_completed(self) -> bool:
        return self._status == Status.TO_BE_EXECUTE