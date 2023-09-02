from dataclasses import dataclass

from enums.gender import Gender


@dataclass
class GroupInfo:
    gender: Gender
    age: int
    additional_code: str
    ctrl_points_cnt: int
    ctrl_points_order: list[int]
    dist_len: int

    @property
    def group_code(self) -> str:
        return self.gender.value + str(self.age) + self.additional_code