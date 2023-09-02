from typing import NamedTuple

from ..event.event_entity import Event
from .api_competition_result import APICompetitionResult


class APIResults(NamedTuple):
    event: Event
    results: list[APICompetitionResult]
