from dataclasses import dataclass
from datetime import datetime


@dataclass
class Workout:
    user_first_name: str
    user_last_name: str
    user_birthdate: datetime
    date: datetime
    splits: dict
    sport_kind: str = 'orient'
    competition_name: str | None = None
