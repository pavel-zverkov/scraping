from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import NamedTuple

from enums.qualify import Qualify


class GroupResultsEntity(NamedTuple):
    control_points_order: list[int]
    results: list[Result]


@dataclass
class Result:
    serial: int
    first_name: str
    second_name: str
    orient_id: int
    birth_year: int
    control_points_info: list[ControlPointInfo]
    place: int | None = None
    club: str | None = None
    qualify: Qualify | None = None
    result: datetime.time | None = None
    lider_lag: timedelta | None = None
    additional_info: str = ''

    @property
    def person(self) -> str:
        return self.second_name + self.first_name


class ControlPointInfo(NamedTuple):
    id: int
    time: datetime.time
    cumulative_time: datetime.time
    place: int
