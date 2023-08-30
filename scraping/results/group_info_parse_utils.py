from typing import TYPE_CHECKING

from enums.gender import Gender

from .group_info_entity import GroupInfo

if TYPE_CHECKING:
    from bs4.element import Tag


GENDER_INDEX = 0


def parse_group_info(
    group_info: 'Tag',
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


def __get_gender(gender_age: str) -> Gender:
    gender = gender_age[GENDER_INDEX]
    return Gender(gender)


def __get_age(gender_age: str) -> int:
    if gender_age in ['НовичкиМ,', 'НовичкиЖ,', 'ЭкспертыМ,']:
        return 9
    _s = gender_age[GENDER_INDEX + 1:].replace(',', '')
    _s = ''.join([i for i in _s if i.isnumeric()])
    return int(_s)


def __get_additional_code(gender_age: str) -> str:
    _s = gender_age[GENDER_INDEX + 1:].replace(',', '')
    _s = ''.join([i for i in _s if not i.isnumeric()])
    return _s


def __get_dist_len(dist_len: str) -> float:
    return float(dist_len.replace(',', '.'))
