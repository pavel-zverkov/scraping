from distancies.group_info_entity import GroupInfo
from loguru import logger
from enums.gender import Gender

GENDER_INDEX = 0


def parse_group_info(group_info: str) -> GroupInfo:
    logger.debug(f'Group info: {group_info.split()}')
    gender_age, ctrl_points_cnt, _, dist_len, _ = group_info.split()
    return GroupInfo(
        gender=get_gender(gender_age),
        age=get_age(gender_age),
        ctrl_points_cnt=int(ctrl_points_cnt),
        dist_len=get_dist_len(dist_len)
    )


def get_gender(gender_age: str) -> Gender:
    gender = gender_age[GENDER_INDEX]
    return Gender(gender).name


def get_age(gender_age: str) -> int:
    return int(gender_age[GENDER_INDEX + 1:].replace(',', ''))


def get_dist_len(dist_len: str) -> float:
    return float(dist_len.replace(',', '.'))