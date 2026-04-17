from __future__ import annotations
from typing import Optional, Dict


class ArgumentOperation:
    def __init__(self,
                 piid: int,
                 values: Optional[list[Any]] = None,
                 value: Optional[Any] = None):
        self._piid: int = piid
        self._values: list[Any] = []

        if value is not None:
            self._values.append(value)
        if values is not None:
            self._values.extend(values)

    @property
    def piid(self) -> int:
        return self._piid

    @property
    def values(self) -> list[Any]:
        return self._values

    def __str__(self) -> str:
        b = [f"#{self._piid} = "]

        for i, value in enumerate(self._values):
            if isinstance(value, str):
                b.append(f'"{value}"')
            else:
                b.append(str(value))

            if i + 1 < len(self._values):
                b.append(", ")

        return "".join(b)

    @staticmethod
    def to_string(arguments: Dict[int, ArgumentOperation],
                  pretty: bool = False,
                  tab: bool = False) -> str:
        b = []
        if pretty:
            b.append("\n    ")
            if tab:
                b.append("    ")

        i = 1
        for entry in arguments.values():
            b.append(str(entry))

            if i < len(arguments):
                b.append(",")
                if pretty:
                    b.append("\n    ")
                    if tab:
                        b.append("    ")
                else:
                    b.append(" ")
            i += 1

        return "".join(b)