from __future__ import annotations
from typing import Optional

import copy
import datetime

from xiot_core.spec.typedef.definition.urn.urn import Urn
from xiot_core.spec.typedef.definition.urn.urn_type import UrnType

class Summary:
    _FORMAT = datetime.datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S").strftime

    def __init__(self,
                 type_val: Optional[Urn | str] = None,
                 online: bool = False,
                 protocol: Optional[str] = None,
                 parent_id: Optional[str] = None,
                 root_id: Optional[str] = None,
                 members: Optional[list[str]] = None):
        self._type: Optional[Urn] = None
        self._online: bool = online
        self._cloud_id: Optional[str] = None
        self._protocol: Optional[str] = protocol
        self._parent_id: Optional[str] = parent_id
        self._root_id: Optional[str] = root_id
        self._members: list[str] = []
        self._last_online: datetime.datetime = datetime.datetime.now()
        self._last_offline: datetime.datetime = datetime.datetime.now()

        # 初始化type
        if isinstance(type_val, str):
            self._type = Urn(types = [UrnType.GROUP, UrnType.DEVICE], string = type_val)
        elif isinstance(type_val, Urn):
            self._type = type_val

        # 初始化members
        if members:
            self._members.extend(members)

    # 拷贝构造
    @classmethod
    def from_other(cls, other: Summary) -> Summary:
        instance = cls()
        instance._type = other._type
        instance._online = other._online
        instance._cloud_id = other._cloud_id
        instance._protocol = other._protocol
        instance._parent_id = other._parent_id
        instance._root_id = other._root_id
        instance._members = copy.deepcopy(other._members)
        instance._last_online = other._last_online
        instance._last_offline = other._last_offline
        return instance

    @property
    def type(self) -> Optional[Urn]:
        return self._type

    @type.setter
    def type(self, type_val: Urn | str):
        if isinstance(type_val, str):
            self._type = Urn(types = [UrnType.GROUP, UrnType.DEVICE], string = type_val)
        else:
            self._type = type_val

    @property
    def online(self) -> bool:
        return self._online

    @online.setter
    def online(self, online: bool):
        self._online = online

    @property
    def parent_id(self) -> Optional[str]:
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id: str):
        self._parent_id = parent_id

    @property
    def root_id(self) -> Optional[str]:
        return self._root_id

    @root_id.setter
    def root_id(self, root_id: str):
        self._root_id = root_id

    @property
    def members(self) -> list[str]:
        return self._members

    @members.setter
    def members(self, members: list[str]):
        self._members.clear()
        if members:
            self._members.extend(members)

    @property
    def protocol(self) -> Optional[str]:
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        self._protocol = protocol

    @property
    def cloud_id(self) -> Optional[str]:
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id: str):
        self._cloud_id = cloud_id

    @property
    def last_online(self) -> datetime.datetime:
        return self._last_online

    @property
    def last_online_time(self) -> int:
        return int(self._last_online.timestamp() * 1000) if self._last_online else 0

    @property
    def last_online_string(self) -> Optional[str]:
        if self._last_online:
            return self._last_online.strftime("%Y-%m-%d %H:%M:%S")
        return None

    def set_last_online(self, last_online: datetime.datetime | int | str) -> Summary:
        if isinstance(last_online, datetime.datetime):
            self._last_online = last_online
        elif isinstance(last_online, int):
            self._last_online = datetime.datetime.fromtimestamp(last_online / 1000)
        elif isinstance(last_online, str):
            try:
                # 替换T字符，兼容SQL timestamp格式
                dt_str = last_online.replace("T", " ")
                self._last_online = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                print(f"lastOnline parser failed: {e}")
                self._last_online = None  # type: ignore
        return self

    @property
    def last_offline(self) -> datetime.datetime:
        return self._last_offline

    @property
    def last_offline_time(self) -> int:
        return int(self._last_offline.timestamp() * 1000) if self._last_offline else 0

    @property
    def last_offline_string(self) -> Optional[str]:
        if self._last_offline:
            return self._last_offline.strftime("%Y-%m-%d %H:%M:%S")
        return None

    def set_last_offline(self, last_offline: datetime.datetime | int | str) -> Summary:
        if isinstance(last_offline, datetime.datetime):
            self._last_offline = last_offline
        elif isinstance(last_offline, int):
            self._last_offline = datetime.datetime.fromtimestamp(last_offline / 1000)
        elif isinstance(last_offline, str):
            try:
                dt_str = last_offline.replace("T", " ")
                self._last_offline = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                print(f"lastOffline parser failed: {e}")
                self._last_offline = None  # type: ignore
        return self

    def change(self, other: Summary) -> bool:
        if self is other:
            return False

        type_changed = self._change_type(other._type)
        online_changed = self._change_online(other._online)
        root_id_changed = self._change_root_id(other._root_id)
        parent_id_changed = self._change_parent_id(other._parent_id)
        cloud_id_changed = self._change_cloud_id(other._cloud_id)
        protocol_changed = self._change_protocol(other._protocol)
        members_changed = self._change_members(other._members)
        last_online_changed = self._change_last_online(other.last_online_time)
        last_offline_changed = self._change_last_offline(other.last_offline_time)

        return (type_changed or online_changed or root_id_changed or parent_id_changed or
                cloud_id_changed or protocol_changed or members_changed or
                last_online_changed or last_offline_changed)

    def _change_type(self, type_val: Optional[Urn]) -> bool:
        if self._type == type_val:
            return False
        self._type = type_val
        return True

    def _change_online(self, online: bool) -> bool:
        if self._online == online:
            return False
        self._online = online
        return True

    def _change_root_id(self, root_id: Optional[str]) -> bool:
        if self._root_id == root_id:
            return False
        self._root_id = root_id
        return True

    def _change_parent_id(self, parent_id: Optional[str]) -> bool:
        if self._parent_id == parent_id:
            return False
        self._parent_id = parent_id
        return True

    def _change_cloud_id(self, cloud_id: Optional[str]) -> bool:
        if self._cloud_id == cloud_id:
            return False
        self._cloud_id = cloud_id
        return True

    def _change_protocol(self, protocol: Optional[str]) -> bool:
        if self._protocol == protocol:
            return False
        self._protocol = protocol
        return True

    def _change_members(self, members: list[str]) -> bool:
        changed = False
        if len(members) != len(self._members):
            self.members = members
            changed = True
        else:
            for i in range(len(self._members)):
                if self._members[i] != members[i]:
                    self._members[i] = members[i]
                    changed = True
        return changed

    def _change_last_online(self, last_online: datetime.datetime | int) -> bool:
        if isinstance(last_online, datetime.datetime):
            ts = int(last_online.timestamp() * 1000)
        else:
            ts = last_online

        if ts == 0:
            return False
        if self.last_offline_time == ts:
            return False

        self._last_online = datetime.datetime.fromtimestamp(ts / 1000)
        return True

    def _change_last_offline(self, last_offline: datetime.datetime | int) -> bool:
        if isinstance(last_offline, datetime.datetime):
            ts = int(last_offline.timestamp() * 1000)
        else:
            ts = last_offline

        if ts == 0:
            return False
        if self.last_offline_time == ts:
            return False

        self._last_offline = datetime.datetime.fromtimestamp(ts / 1000)
        return True

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, Summary):
            return False
        return (self._online == other._online and
                self._type == other._type and
                self._cloud_id == other._cloud_id and
                self._protocol == other._protocol and
                self._parent_id == other._parent_id and
                self._root_id == other._root_id and
                self._members == other._members and
                self._last_online == other._last_online and
                self._last_offline == other._last_offline)

    def __hash__(self) -> int:
        return hash((self._type, self._online, self._cloud_id, self._protocol,
                     self._parent_id, self._root_id, tuple(self._members),
                     self._last_online, self._last_offline))