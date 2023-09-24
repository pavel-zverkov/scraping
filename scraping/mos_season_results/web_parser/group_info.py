from dataclasses import dataclass

from ...enums.gender import Gender


@dataclass
class GroupInfo:
    gender: Gender | None
    age: int
    additional_code: str
    ctrl_points_cnt: int
    ctrl_points_order: list[int]
    dist_len: int

    @property
    def group_code(self) -> str:
        str_age = str(self.age) if self.age else ''
        str_gender = self.gender.value if self.gender else ''
        return str_gender + str_age + self.additional_code
