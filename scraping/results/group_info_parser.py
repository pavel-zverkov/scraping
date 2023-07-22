from distancies.group_info_entity import GroupInfo
from loguru import logger
from enums.gender import Gender

GENDER_INDEX = 0


def parse_group_info(group_info: str) -> GroupInfo:
    gender_age, ctrl_points_cnt, _, dist_len, _ = group_info.split()
    return GroupInfo(
        gender=get_gender(gender_age),
        age=get_age(gender_age),
        additional_code=get_additional_code(gender_age),
        ctrl_points_cnt=int(ctrl_points_cnt),
        dist_len=get_dist_len(dist_len)
    )


def get_gender(gender_age: str) -> Gender:
    gender = gender_age[GENDER_INDEX]
    return Gender(gender)


def get_age(gender_age: str) -> int:
    s = gender_age[GENDER_INDEX + 1:].replace(',', '')
    s = ''.join([i for i in s if i.isnumeric()])
    return int(s)


def get_additional_code(gender_age: str) -> str:
    s = gender_age[GENDER_INDEX + 1:].replace(',', '')
    s = ''.join([i for i in s if not i.isnumeric()])
    return s


def get_dist_len(dist_len: str) -> float:
    return float(dist_len.replace(',', '.'))