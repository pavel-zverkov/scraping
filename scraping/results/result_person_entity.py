from dataclasses import dataclass
import datetime
from typing import NamedTuple
from results.group_info_entity import GroupInfo

from results.group_results_entity import ControlPointInfo
from results.results_constants import NO_RESULT, TIME_FORMAT


@dataclass
class ResultPersonEntity:
    person: str
    result: datetime.time | None
    group_info: GroupInfo
    split_info: list[ControlPointInfo]
