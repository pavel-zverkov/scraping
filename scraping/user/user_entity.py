from dataclasses import dataclass
from datetime import date

from enums.qualify import Qualify


@dataclass
class UserCreate:
    first_name: str
    last_name: str
    birthdate: date
    qualify: Qualify
