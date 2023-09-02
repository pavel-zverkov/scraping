import datetime
from dataclasses import dataclass
from string import Template

from ..competition.competition_entity import Competition
from ..mos_season_results.constants import TIME_FORMAT
from ..mos_season_results.parser.control_point_info import ControlPointInfo
from ..mos_season_results.parser.group_info import GroupInfo

split_template = Template(
    '$ctrl_point_id'
)


@dataclass
class Split:
    competition: Competition
    person: str
    group_info: GroupInfo
    ctrl_points_info: list[ControlPointInfo]
    result: datetime.time | None

    # TODO: Переделать на шаблоны
    def display(self) -> None:
        print(self.person)
        print(f'Группа - {self.group_info.group_code}', end='\n\n')
        for ctrl_point_info in self.ctrl_points_info:
            print(f'{ctrl_point_info.id:>4} {ctrl_point_info.split_time.strftime(TIME_FORMAT):>10} {ctrl_point_info.cumulative_time.strftime(TIME_FORMAT):>10}')
        print()
        print(f'Финиш - {self.result - ctrl_point_info.cumulative_time}')
        print(
            f'Результат - {self.result.strftime(TIME_FORMAT) if self.result else self.result}')
