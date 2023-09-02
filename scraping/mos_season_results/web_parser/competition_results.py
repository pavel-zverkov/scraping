
from typing import NamedTuple

from .group_result import GroupResults


class CompetitionResults(NamedTuple):
    competition_info: str
    results: list[GroupResults]
