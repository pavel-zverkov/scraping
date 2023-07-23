from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import NamedTuple

from enums.qualify import Qualify

from .group_info_entity import GroupInfo


class GroupResultsEntity(NamedTuple):
    info: GroupInfo
    results: list[Result]


@dataclass
class Result:
    serial: int
    first_name: str
    second_name: str
    control_points_info: list[ControlPointInfo]
    result: datetime.time | None = None
    orient_id: int | None = None
    birth_year: int | None = None
    place: int | None = None
    club: str | None = None
    qualify: Qualify | None = None
    lider_lag: timedelta | None = None
    additional_info: str = ''

    @property
    def person(self) -> str:
        return self.second_name + ' ' + self.first_name


class RawResultInfo(NamedTuple):
    person_info: str
    split_info: str
    cumulative_info: str


class ControlPointInfo(NamedTuple):
    id: int
    time: datetime.time
    cumulative_time: datetime.time
    place: int
