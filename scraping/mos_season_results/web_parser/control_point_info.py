from dataclasses import dataclass
from datetime import time


@dataclass
class ControlPointInfo:
    id: int
    split_time: time
    cumulative_time: time
    place: int
