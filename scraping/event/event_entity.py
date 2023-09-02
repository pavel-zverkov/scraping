from dataclasses import dataclass
from datetime import date


@dataclass
class Event:

    name: str
    start_date: date
    end_date: date
    sport_kind: str = 'orient'
