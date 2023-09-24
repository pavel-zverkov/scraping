import re
from datetime import datetime

from bs4.element import NavigableString, Tag

from ...enums.gender import Gender
from ...logger import logger
from .. import constants as c
from .control_point_info import ControlPointInfo
from .group_info import GroupInfo
from .person_result import PersonResult, RawPersonResultInfo

GENDER_INDEX = 0


def parse_group_results(
    group_results: list[NavigableString | Tag]
) -> tuple[list[int], list[PersonResult]]:

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

            # logger.debug(main_info)

            result_info = RawPersonResultInfo(
                person_info=person_info.strip(),
                split_info=person_result.split(
                    person_info)[c.SPLIT_INFO_INDEX].strip(),
                cumulative_info=result.text.strip()
            )

            results.append(result_info)
            person_result = []

    results = results[1:]

    return control_points_order, [__parse_result(result) for result in results]


def parse_group_info(
    group_info: Tag,
    group_control_points_order: list[int]
) -> GroupInfo:

    gender_age, ctrl_points_cnt, _, dist_len, _ = group_info.text.split()
    return GroupInfo(
        gender=__get_gender(gender_age),
        age=__get_age(gender_age),
        additional_code=__get_additional_code(gender_age),
        ctrl_points_cnt=int(ctrl_points_cnt),
        ctrl_points_order=group_control_points_order,
        dist_len=__get_dist_len(dist_len)
    )


def __parse_result(result_info: RawPersonResultInfo) -> PersonResult:

    control_points_info = __collect_split_info(
        result_info.split_info,
        result_info.cumulative_info
    )

    person_info = result_info.person_info
    person_info_list = person_info.split()

    serial, second_name, first_name = person_info_list[:3]
    birth_year = __get_birth_year(person_info)

    if person_info_list[c.PLACE_INDEX].isnumeric() \
            or person_info_list[c.PLACE_INDEX] == c.OUT_OF_COMPETITION:

        result = datetime.strptime(
            re.findall(c.TIME_PATTERN, person_info)[0],
            c.TIME_FORMAT
        )
        lider_lag = re.findall(c.LAG_PATTERN, person_info)
        lider_lag = lider_lag[0] if lider_lag else None

        place = person_info_list[c.PLACE_INDEX]

    else:
        result = None
        lider_lag = None
        place = None

    if result:
        control_points_info = __add_result_to_split(
            control_points_info,
            result,
            place
        )
    return PersonResult(
        serial=int(serial),
        first_name=first_name,
        second_name=second_name,
        control_points_info=control_points_info,
        result=result if result else None,
        lider_lag=lider_lag if lider_lag else None,
        place=place if place else None,
        birth_year=datetime(birth_year, 1, 1) if birth_year else None
    )


def __collect_split_info(
    split_info: str,
    cumulative_info: str
) -> list[ControlPointInfo]:

    logger.debug(split_info)
    split_info = re.findall(c.CONTROL_POINT_INFO_PATTERN, split_info)
    cumulative_info = re.findall(c.CONTROL_POINT_INFO_PATTERN, cumulative_info)
    logger.info(split_info)

    output = []
    for split, cumulative_split in zip(split_info, cumulative_info):
        time, cp_id, place = __parse_control_point_time_info(split)
        cumulative_time, _, _ = __parse_control_point_time_info(
            cumulative_split)

        output.append(
            ControlPointInfo(
                id=cp_id,
                split_time=datetime.strptime(
                    __format_time(time), c.TIME_FORMAT).time(),
                cumulative_time=datetime.strptime(
                    __format_time(cumulative_time), c.TIME_FORMAT).time(),
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


def __get_gender(gender_age: str) -> Gender:
    gender = re.search('(?:М|Ж)', gender_age)
    gender = gender.group() if gender else None
    return Gender(gender) if gender else None


def __get_age(gender_age: str) -> int:
    gender = __get_gender(gender_age)
    gender = gender.value if gender else ''
    _s = gender_age.replace(gender, '').replace(',', '')
    _s = ''.join([i for i in _s if i.isnumeric()])
    return int(_s) if _s else 0


def __get_additional_code(gender_age: str) -> str:
    gender = __get_gender(gender_age)
    gender = gender.value if gender else ''
    _s = gender_age.replace(gender, '').replace(',', '')
    _s = ''.join([i for i in _s if not i.isnumeric()])
    return _s


def __get_dist_len(dist_len: str) -> float:
    return float(dist_len.replace(',', '.'))


def __add_result_to_split(
    split: list[ControlPointInfo],
    result: datetime,
    place: int
) -> list[ControlPointInfo]:

    split.append(
        ControlPointInfo(
            id='-1',
            # split_time=result - last_point_info.cumulative_time,
            split_time=datetime(1970, 1, 1, 0, 0).time(),
            cumulative_time=result,
            place=place
        )
    )
    return split


def __get_birth_year(
    person_info: str
) -> int:

    numbers_list = re.findall('(?:19|20)\d{2}', person_info)
    if not numbers_list:
        return 1970
    return int(numbers_list[c.BIRTH_YEAR_INDEX])


def __format_time(time: str) -> str:
    if re.match(c.TIME_PATTERN, time):
        return time

    minutes, seconds = map(int, time.split(':'))
    if minutes > 59:
        hours = minutes // 60
        minutes %= 60

        str_hour = '0' + str(hours) if hours < 10 else str(hours)
        return str_hour + ':' + str(minutes) + ':' + str(seconds)
    return '00:' + str(minutes) + ':' + str(seconds)
