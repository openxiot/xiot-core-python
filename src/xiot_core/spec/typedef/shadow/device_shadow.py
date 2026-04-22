from __future__ import annotations

from typing import Collection

from .shadow import Shadow


class DeviceShadow:
    def __init__(self, did: str, shadows: Collection[Shadow]):
        self._did: str = did
        self._shadows: Collection[Shadow] = shadows

    @property
    def did(self) -> str:
        return self._did

    @did.setter
    def did(self, did: str):
        self._did = did

    @property
    def shadows(self) -> Collection[Shadow]:
        return self._shadows

    @shadows.setter
    def shadows(self, shadows: list[Shadow]):
        self._shadows = shadows