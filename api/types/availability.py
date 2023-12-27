from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass, asdict

AvailableDataTimeTuple = namedtuple("AvailableDataTimeTuple", ["user_id", "available_date", "start_time", "end_time"])

@dataclass
class AvailableDateTime:
    available_date: str
    start_time: str
    end_time: str

    @classmethod
    def from_raw_req_list(cls, req_list: list[dict]) -> list[AvailableDateTime]:
        return [AvailableDateTime(**d) for d in req_list]

    def to_tuple(self, user_id: str):
        raw = {"user_id":user_id} | asdict(self)
        return tuple(AvailableDataTimeTuple(**raw))



@dataclass
class OverlapInterval:
    available_date: str
    start_overlap: str
    end_overlap: str
    start_time1: str
    end_time1: str
    start_time2: str
    end_time2: str


@dataclass
class Overlaps:
    user1: str
    user2: str
    overlaps: list[OverlapInterval]
