from dataclasses import dataclass
from datetime import date


@dataclass
class Competition:
    name: str
    date: date
    class_list: list[str]
    control_point_list: list[str]
    format: str
    sport_kind: str = 'orient'
    description: str | None = None
    location: str | None = None
