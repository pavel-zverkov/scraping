import datetime

from ..constants import TIME_FORMAT
from .split_entity import Split
from .split_errors import DifferentDistanceError

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'
SL = '      '


class SplitComparer:
    def display_compare(self, left_split: Split, right_split: Split) -> None:
        ctrl_point_order = self.check_distancies(
            left_split.group_info.ctrl_points_order,
            right_split.group_info.ctrl_points_order
        )

        print(f'{left_split.person:>20}{SL}{right_split.person:<20}', end='\n\n')
        for i in range(len(ctrl_point_order)):
            t_1 = left_split.ctrl_points_info[i].time
            t_2 = right_split.ctrl_points_info[i].time
            t_1_s, t_2_s = self.__stringify_times(t_1, t_2)
            arrow = self.__get_arrow(t_1, t_2)
            sign = '+' if t_1 > t_2 else '-'

            print(
                f'{i + 1:>2}({left_split.ctrl_points_info[i].id:>3}){t_1_s:>13}{arrow:^6}{t_2_s:<15}{sign}{t_1 - t_2 if t_1 > t_2 else t_2 - t_1}')

    def check_distancies(
        self,
        left_ctrl_point_order: list[int],
        right_ctrl_point_order: list[int]
    ) -> list[int]:

        if left_ctrl_point_order == right_ctrl_point_order:
            return left_ctrl_point_order

        else:
            raise DifferentDistanceError('Distancies are not match!')

    def __stringify_times(
        self,
        t_1: datetime.time,
        t_2: datetime.time
    ) -> tuple[str]:
        return t_1.strftime(TIME_FORMAT), t_2.strftime(TIME_FORMAT)

    def __get_arrow(
        self,
        t_1: datetime.time,
        t_2: datetime.time
    ) -> str:
        return ' >' if t_2 < t_1 else '< '

    # def __compare_times(self, t_1: datetime.time, t_2: datetime.time) -> tuple[str]:
    #     return (t_1.strftime(TIME_FORMAT), self.__bold_wrapper(t_2.strftime(TIME_FORMAT))) \
    #         if t_2 < t_1 \
    #         else \
    #         (self.__bold_wrapper(t_1.strftime(TIME_FORMAT)
    #                              ), t_2.strftime(TIME_FORMAT))

    # def __bold_wrapper(self, text: str):
    #     return '**' + text + '**'
