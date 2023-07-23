from competition.competition_entity import Competition
from results.group_results_entity import GroupResultsEntity
from splits.split_entity import Split


class ResultPersonSearcher:
    def __init__(self, results: list[GroupResultsEntity]) -> None:
        self.results = results

    def search(self, person: str) -> Split:
        for group_result in self.results:
            for result in group_result.results:
                if result.person == person:
                    return Split(
                        competition=Competition(),
                        person=result.person,
                        result=result.result,
                        group_info=group_result.info,
                        ctrl_points_info=result.control_points_info
                    )
