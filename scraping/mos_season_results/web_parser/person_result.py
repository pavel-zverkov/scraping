from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import NamedTuple

from ...enums.qualify import Qualify
from .control_point_info import ControlPointInfo


@dataclass
class PersonResult:
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


class RawPersonResultInfo(NamedTuple):
    person_info: str
    split_info: str
    cumulative_info: str
