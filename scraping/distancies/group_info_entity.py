from enums.gender import Gender
from typing import NamedTuple


class GroupInfo(NamedTuple):
    gender: Gender
    age: int
    ctrl_points_cnt: int
    dist_len: int