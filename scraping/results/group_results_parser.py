from datetime import datetime
import re

from loguru import logger
from results.group_results_entity import ControlPointInfo, GroupResultsEntity
from results.group_results_entity import Result

TITLE_INDEX = 0
PERSON_INFO_INDEX = 0
SPLIT_INFO_INDEX = 1
FINISH_SPLIT_INDEX = -1
PLACE_INDEX = -1
CONTROL_POINT_INFO_PATTERN = '\d\d:\d\d:\d\d\(\s*\d*\)\(\s*\d*\)'
TIME_FORMAT = '%H:%M:%S'


def parse_all_groups(all_group_results: list) -> list[GroupResultsEntity]:
    return [parse_group_results(group_results) for group_results in all_group_results]


def parse_group_results(group_results: list[str]) -> GroupResultsEntity:
    control_points_order = \
        parse_control_points_order(group_results.u.text)
    logger.info(control_points_order)
    # <class 'bs4.element.NavigableString'>
    # <class 'bs4.element.Tag'>
    results = []
    person_result = []
    # TODO: Начинать итерацию без заголовков
    for result in group_results:
        if result.name != 'u':
            person_result.append(result.text)
        else:
            person_result = ' '.join(person_result)
            main_info = re.split(CONTROL_POINT_INFO_PATTERN, person_result)
            person_info = main_info[PERSON_INFO_INDEX]

            result_info = {
                'person_info': person_info.strip(),
                'split_info': person_result.split(person_info)[SPLIT_INFO_INDEX].strip(),
                'cumulative_info': result.text.strip()
            }
            results.append(result_info)
            person_result = []

    results = results[1:]
    return [parse_result(result) for result in results]


def parse_result(result: dict) -> Result: 
    
    control_points_info = collect_split_info(
        result['split_info'],
        result['cumulative_info']
    )

    person_info = result['person_info'].split()
    logger.debug(person_info)
    serial, second_name, first_name = person_info[:3]
    if person_info[PLACE_INDEX].isnumeric() or person_info[PLACE_INDEX] == 'в/к':
        orient_id, birth_year, result, lider_lag, place = person_info[-5:]
    # TODO: Убрать костыль
    elif re.match('\d\d:\d\d:\d\d', person_info[PLACE_INDEX]): 
        orient_id, birth_year, result, _ = person_info[-4:]
        result = None
        lider_lag = None
        place = None
    else:
        orient_id, birth_year, result = person_info[-3:]
        result = None
        lider_lag = None
        place = None

    result = Result(
        serial=int(serial),
        first_name=first_name,
        second_name=second_name,
        orient_id=int(orient_id),
        birth_year=int(birth_year),
        control_points_info=control_points_info,
        result=datetime.strptime(result, TIME_FORMAT) if result else None,
        lider_lag=lider_lag,
        place=place
    )

    return result


def collect_split_info(
    split_info: str,
    cumulative_info: str
) -> list[ControlPointInfo]:
    split_info = re.findall(CONTROL_POINT_INFO_PATTERN, split_info)
    cumulative_info = re.findall(CONTROL_POINT_INFO_PATTERN, cumulative_info)

    output = []
    for split, cumulative_split in zip(split_info, cumulative_info):
        time, cp_id, place = parse_control_point_time_info(split)
        cumulative_time, _, _ = parse_control_point_time_info(cumulative_split)

        output.append(
            ControlPointInfo(
                id=cp_id,
                time=datetime.strptime(time, TIME_FORMAT),
                cumulative_time=datetime.strptime(cumulative_time, TIME_FORMAT),
                place=place
            )
        )

    return output


def parse_control_point_time_info(control_point_time_info: str) -> list:
    return control_point_time_info.replace('(', ' ').replace(')', ' ').split()


def parse_control_points_order(group_result_title: str) -> list[int]:
    return [
        get_contol_point_number(item) 
        for item in re.findall('\d*\(\s*\d*', group_result_title)
    ]


def get_contol_point_number(raw_number: str) -> int:
    return int(raw_number.replace('(', ' ').split()[1])