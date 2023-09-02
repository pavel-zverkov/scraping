from typing import NamedTuple

from ..competition.competition_entity import Competition
from ..workout.workout_entity import Workout


class APICompetitionResult(NamedTuple):
    competition: Competition
    workout_list: list[Workout]
