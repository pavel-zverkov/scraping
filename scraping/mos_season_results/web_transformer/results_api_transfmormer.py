
from collections import defaultdict
from datetime import date, datetime
from json import dumps

from ...competition.competition_entity import Competition
from ...event.event_entity import Event
from ...workout.workout_entity import Workout
from .. import constants as c
from ..api_competition_result import APICompetitionResult
from ..api_results import APIResults
from ..web_parser.competition_results import CompetitionResults
from ...logger import logger
from ..web_parser.group_result import GroupResults
from ..web_parser.person_result import PersonResult


class ResultsAPITransformer:

    def transform_results(self, results: CompetitionResults) -> APIResults:
        event_name, description, competition_date, competition_location = \
            self.__parse_competition_info(results.competition_info)

        event = self.__transform_competition_info_to_event(event_name)
        competition_info_list = \
            self.__create_competition_dict(
                results.results,
                description,
                competition_date,
                competition_location
            )

        api_competition_result_list = [
            APICompetitionResult(competition, competition_workout_list)
            for competition, competition_workout_list in competition_info_list
        ]

        return APIResults(event, api_competition_result_list)

    def __parse_competition_info(self, info: str):
        info_list = [item.strip() for item in info.split('\n')]

        event_name = info_list[c.EVENT_TITLE_INDEX]
        description = info_list[c.DESCRIPTION_INDEX]
        competition_date, competition_location = \
            info_list[c.COMPETITION_DATE_PLACE_INDEX].split(', ')

        competition_date = datetime.strptime(
            competition_date, '%d %B %Y')

        return event_name, description, competition_date, competition_location

    def __create_competition_dict(
        self,
        group_result_list: list[GroupResults],
        description: str,
        competition_date: date,
        competition_location: str
    ) -> list[tuple[Competition, list[Workout]]]:

        raw_competition_dict: dict[str, list[GroupResults]] = defaultdict(list)
        for group_result in group_result_list:
            key = str(group_result.group_info.ctrl_points_order)
            value = group_result

            raw_competition_dict[key].append(value)

        raw_competition_dict = self.__sort_dict(raw_competition_dict)

        competition_info_list = [
            (
                Competition(
                    name=f'D{i + 1}',
                    date=competition_date,
                    description=description,
                    location=competition_location,
                    control_point_list=self.__str_to_list(ctr_point_list),
                    class_list=self.__get_class_list(group_result_list),
                    format=c.COMPETITION_FORMAT
                ),
                [
                    self.__trasform_person_result_to_workout(
                        person_result,
                        competition_date,
                        f'D{i + 1}'
                    )
                    for group_result in group_result_list
                    for person_result in group_result.results
                ]
            )
            for i, (ctr_point_list, group_result_list)
            in enumerate(raw_competition_dict.items())
        ]

        return competition_info_list

    def __transform_competition_info_to_event(
        self,
        event_name: str
    ) -> Event:
        YEAR = datetime.now().year

        if 'лето' in event_name.lower():
            start_date, end_date = \
                datetime(YEAR, 6, 1).date(), datetime(YEAR, 8, 31).date()

        if 'осень' in event_name.lower():
            start_date, end_date = \
                datetime(YEAR, 9, 1).date(), datetime(YEAR, 11, 31).date()

        if 'зима' in event_name.lower():
            start_date, end_date = \
                datetime(YEAR, 12, 1).date(), datetime(YEAR, 3, 1).date()

        start_date, end_date = \
            datetime(YEAR, 3, 1).date(), datetime(YEAR, 5, 31).date()

        return Event(
            name=event_name,
            start_date=start_date,
            end_date=end_date
        )

    def __get_class_list(
        self,
        result_list: list[GroupResults]
    ) -> str:
        return [
            group_result.group_info.group_code
            for group_result in result_list
        ]

    def __trasform_person_result_to_workout(
        self,
        result: PersonResult,
        competition_date: datetime,
        competition_name: str
    ) -> Workout:
        splits = {
            str(ctrl_point_info.id): ctrl_point_info
            for ctrl_point_info in result.control_points_info
        }

        return Workout(
            user_first_name=result.first_name,
            user_last_name=result.second_name,
            user_birthdate=datetime(result.birth_year).date()
            if result.birth_year else datetime(1970, 1, 1).date(),
            date=competition_date,
            splits=splits,
            competition_name=competition_name
        )

    def __str_to_list(self, s: str) -> list[str]:
        return s.replace('[', '').replace(']', '').split(', ')

    def __sort_dict(self, d: dict) -> dict:
        sorted_keys = sorted(d.keys(), key=lambda x: len(x), reverse=True)
        return {key: d[key] for key in sorted_keys}


if __name__ == '__main__':
    from ..web_parser.results_parser import ResultsParser
    from ...abase.utils.datetime_json_encoder import DateTimeEncoder
    from dataclasses import asdict

    MOS_SEASON_URL = 'http://o-mephi.net/cup/prot/Mosleto2023_9_spl.htm'
    parser = ResultsParser(MOS_SEASON_URL)
    transformer = ResultsAPITransformer()

    api_results = transformer.transform_results(parser.parse())
    logger.info(dumps(asdict(api_results.event),
                indent=2, cls=DateTimeEncoder))
    logger.info(dumps(asdict(api_results.results[0].competition),
                      indent=2, cls=DateTimeEncoder))
    logger.info(dumps(api_results.results[0].workout_list[0].__dict__,
                      indent=2, cls=DateTimeEncoder))
