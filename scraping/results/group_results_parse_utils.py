import re
from datetime import datetime

from bs4.element import NavigableString, Tag
from logger import logger

from . import results_constants as c
from .group_results_entity import ControlPointInfo, RawResultInfo, Result


def parse_group_results(
    group_results: list[NavigableString | Tag]
) -> tuple[list[int], list[Result]]:

    control_points_order = \
        __parse_control_points_order(group_results.u.text)

    results = []
    person_result = []
    # TODO: Начинать итерацию без заголовков
    for result in group_results:
        if result.name != 'u':
            person_result.append(result.text)

        else:
            person_result = ' '.join(person_result)
            main_info = re.split(c.CONTROL_POINT_INFO_PATTERN, person_result)
            person_info = main_info[c.PERSON_INFO_INDEX]

            result_info = RawResultInfo(
                person_info=person_info.strip(),
                split_info=person_result.split(
                    person_info)[c.SPLIT_INFO_INDEX].strip(),
                cumulative_info=result.text.strip()
            )
            results.append(result_info)
            person_result = []

    results = results[1:]
    return control_points_order, [__parse_result(result) for result in results]


def __parse_result(result_info: RawResultInfo) -> Result:

    control_points_info = __collect_split_info(
        result_info.split_info,
        result_info.cumulative_info
    )

    person_info = result_info.person_info
    person_info_list = person_info.split()

    serial, second_name, first_name = person_info_list[:3]

    if person_info_list[c.PLACE_INDEX].isnumeric() \
            or person_info_list[c.PLACE_INDEX] == c.OUT_OF_COMPETITION:

        result = re.findall(c.TIME_PATTERN, person_info)[0]
        lider_lag = re.findall(c .LAG_PATTERN, person_info)[0]
        place = person_info_list[c.PLACE_INDEX]

    else:
        result = None
        lider_lag = None
        place = None

    return Result(
        serial=int(serial),
        first_name=first_name,
        second_name=second_name,
        control_points_info=control_points_info,
        result=datetime.strptime(result, c.TIME_FORMAT) if result else None,
        lider_lag=lider_lag if lider_lag else None,
        place=place if place else None
    )


def __collect_split_info(
    split_info: str,
    cumulative_info: str
) -> list[ControlPointInfo]:

    split_info = re.findall(c.CONTROL_POINT_INFO_PATTERN, split_info)
    cumulative_info = re.findall(c.CONTROL_POINT_INFO_PATTERN, cumulative_info)

    output = []
    for split, cumulative_split in zip(split_info, cumulative_info):
        time, cp_id, place = __parse_control_point_time_info(split)
        cumulative_time, _, _ = __parse_control_point_time_info(
            cumulative_split)

        output.append(
            ControlPointInfo(
                id=cp_id,
                time=datetime.strptime(time, c.TIME_FORMAT),
                cumulative_time=datetime.strptime(
                    cumulative_time, c.TIME_FORMAT),
                place=place
            )
        )

    return output


def __parse_control_point_time_info(control_point_time_info: str) -> list:
    return control_point_time_info.replace('(', ' ').replace(')', ' ').split()


def __parse_control_points_order(group_result_title: str) -> list[int]:
    return [
        __get_contol_point_number(item)
        for item in re.findall('\d*\(\s*\d*', group_result_title)
    ]


def __get_contol_point_number(raw_number: str) -> int:
    return int(raw_number.replace('(', ' ').split()[1])
