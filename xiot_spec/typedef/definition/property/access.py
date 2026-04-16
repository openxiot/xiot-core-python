from typing import List

class Access:
    WRITABLE = 0x01
    READABLE = 0x02
    NOTIFIABLE = 0x04

    def __init__(self, writable: bool = None, readable: bool = None, notifiable: bool = None):
        self.value = 0
        if writable is not None and readable is not None and notifiable is not None:
            self.set_writable(writable)
            self.set_readable(readable)
            self.set_notifiable(notifiable)

    def is_writable(self) -> bool:
        return (self.value & Access.WRITABLE) == Access.WRITABLE

    def is_readable(self) -> bool:
        return (self.value & Access.READABLE) == Access.READABLE

    def is_notifiable(self) -> bool:
        return (self.value & Access.NOTIFIABLE) == Access.NOTIFIABLE

    def set_writable(self, settable: bool) -> int:
        if settable:
            self.value |= Access.WRITABLE
        else:
            self.value &= ~Access.WRITABLE
        return self.value

    def set_readable(self, gettable: bool) -> int:
        if gettable:
            self.value |= Access.READABLE
        else:
            self.value &= ~Access.READABLE
        return self.value

    def set_notifiable(self, notifiable: bool) -> int:
        if notifiable:
            self.value |= Access.NOTIFIABLE
        else:
            self.value &= ~Access.NOTIFIABLE
        return self.value

    @staticmethod
    def value_of_list(list_: List[str]) -> "Access":
        access = Access()
        for v in list_:
            if v == "read":
                access.set_readable(True)
            elif v == "write":
                access.set_writable(True)
            elif v == "notify":
                access.set_notifiable(True)
        return access

    def to_list(self) -> List[str]:
        array = []
        if self.is_readable():
            array.append("read")
        if self.is_writable():
            array.append("write")
        if self.is_notifiable():
            array.append("notify")
        return array

    @staticmethod
    def value_of_int(value: int) -> "Access":
        access = Access()
        access.value = value
        return access

    def get_value(self) -> int:
        return self.value