from loguru import logger
from results.group_results_entity import GroupResultsEntity
from results.result_person_entity import ResultPersonEntity


class ResultPersonSearcher:
    def __init__(self, person: str) -> None:
        self.person = person

    def search(self, results: list[GroupResultsEntity]) -> ResultPersonEntity:
        for group_result in results:
            for result in group_result.results:
                if result.person == self.person:
                    return ResultPersonEntity(
                        person=result.person,
                        result=result.result,
                        group_info=group_result.info,
                        split_info=result.control_points_info
                    )
