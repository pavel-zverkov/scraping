
from datetime import datetime
from ...competition.competition_entity import Competition
from ...event.event_entity import Event
from ...workout.workout_entity import Workout
from ..web_parser.competition_results import CompetitionResults
from ..web_parser.group_info import GroupInfo
from ..web_parser.person_result import PersonResult
from ..api_results import APIResults
from ..api_competition_result import APICompetitionResult
from .. import constants as c


class ResultsAPITransformer:

    def transform_results(self, results: CompetitionResults) -> APIResults:
        event_name, description, competition_date, competition_location = \
            self.__parse_competition_info(results.competition_info)

        event = self.__transform_competition_info_to_event(event_name)

        api_competition_result_list = []
        for group_result in results.results:

            workout_list = [
                self.__trasform_person_result_to_workout(person_result)
                for person_result in group_result.results
            ]

            api_competition_result_list.append(
                APICompetitionResult(competition, workout_list)
            )

        return APIResults(event, api_competition_result_list)

    def __parse_competition_info(self, info: str):
        info_list = [item.strip() for item in info.split('\n')]

        event_name = info_list[c.EVENT_TITLE_INDEX]
        description = info_list[c.DESCRIPTION_INDEX]
        competition_date, competition_location = \
            info_list[c.COMPETITION_DATE_PLACE_INDEX].split(', ')

        competition_date = datetime.strptime(competition_date, '%d %B %Y')

        return event_name, description, competition_date, competition_location

    def __transform_competition_info_to_event(
        self,
        event_name: str
    ) -> Event:
        YEAR = datetime.now().year

        if 'лето' in event_name.lower():
            start_date, end_date = \
                datetime(YEAR, 6, 1).date(), datetime(YEAR, 8, 31)

        if 'осень' in event_name.lower():
            start_date, end_date = \
                datetime(YEAR, 9, 1).date(), datetime(YEAR, 11, 31)

        if 'зима' in event_name.lower():
            start_date, end_date = \
                datetime(YEAR, 12, 1).date(), datetime(YEAR, 3, 1)

        start_date, end_date = \
            datetime(YEAR, 3, 1).date(), datetime(YEAR, 5, 31)

        return Event(
            name=event_name,
            start_date=start_date,
            end_date=end_date
        )

    def __transform_group_info_to_competition(
        self,
        info: GroupInfo
    ) -> Competition:
        pass

    def __trasform_person_result_to_workout(
        self,
        result: PersonResult
    ) -> Workout:
        pass

        competition_dict: dict[str, list[GroupResultsEntity]] = {}
        for result in results:
            key = str(result.info.ctrl_points_order)
            value = result
            if key not in competition_dict.keys():
                competition_dict[key] = [value]
            else:
                competition_dict[key].append(value)

        sorted_keys = sorted(competition_dict.keys(),
                             key=lambda x: len(x), reverse=True)
        competition_dict = dict(
            zip(sorted_keys, [competition_dict[key] for key in sorted_keys]))

        # logger.info(competition_dict)
        output = []
        for key, value in competition_dict.items():
            output.append(
                ResultEntity(
                    event_name=event_name,
                    competition_name=competition_name,
                    competition_date=competition_date.date(),
                    control_points=str_to_int_list(key),
                    class_list=[
                        (item.info.gender.value +
                         str(item.info.age) + item.info.additional_code)
                        for item in value
                    ],
                    competition_result=value
                )
            )

        return output


def str_to_int_list(s: str) -> list[str]:
    return s.replace('[', '').replace(']', '').split(', ')
