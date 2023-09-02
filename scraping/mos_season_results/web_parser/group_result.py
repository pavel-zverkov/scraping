from typing import NamedTuple

from .group_info import GroupInfo
from .person_result import PersonResult


class GroupResults(NamedTuple):
    group_info: GroupInfo
    results: list[PersonResult]
