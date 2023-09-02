from datetime import time
from typing import NamedTuple


class ControlPointInfo(NamedTuple):
    id: int
    split_time: time
    cumulative_time: time
    place: int
