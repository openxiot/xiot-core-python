class Argument:
    def __init__(self, piid: int, min_repeat: int = 1, max_repeat: int = 1):
        self._piid = piid
        self._min_repeat = min_repeat
        self._max_repeat = max_repeat

    @classmethod
    def from_other(cls, other: "Argument") -> "Argument":
        return cls(other.piid, other.min_repeat, other.max_repeat)

    @property
    def piid(self) -> int:
        return self._piid

    @piid.setter
    def piid(self, value: int) -> None:
        self._piid = value

    @property
    def min_repeat(self) -> int:
        return self._min_repeat

    @min_repeat.setter
    def min_repeat(self, value: int) -> None:
        self._min_repeat = value

    @property
    def max_repeat(self) -> int:
        return self._max_repeat

    @max_repeat.setter
    def max_repeat(self, value: int) -> None:
        self._max_repeat = value