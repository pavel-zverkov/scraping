from datetime import datetime
from json import dumps

from competition.competition_entity import Competition
from logger import logger
from mos_season_results.result_person_searcher import ResultPersonSearcher
from mos_season_results.web_parser.parser_entity import ResultsParser
from requests import post
from splits.split_comparer import SplitComparer
from splits.split_entity import Split
from tqdm import tqdm

URL = 'http://o-mephi.net/cup/prot/Mosleto2023_9_spl.htm'
PERSON_1 = 'Ольховский Дмитрий'
PERSON_2 = 'Хамурзов Владимир'

SPLIT_API_URL = 'http://localhost:8000/'


@logger.catch
def main() -> None:
    results_parser = ResultsParser(URL)
    competition_result_list = results_parser.parse()

    for i, competition_result in enumerate(competition_result_list):
        competition_data = {
            'name': f'D{i + 1}',
            'date': competition_result.competition_date.strftime('%Y-%m-%d'),
            'class_list': competition_result.class_list,
            'control_point_list': competition_result.control_points,
            'sport_kind': 'orient',
            'format': 'кросс-классика'
        }

        post(SPLIT_API_URL + 'competition/', json=competition_data)

        for result in competition_result.competition_result:
            for workout in tqdm(result.results):
                splits = {
                    item.id: item.to_dict()
                    for item in workout.control_points_info
                }
                workout_data = {
                    "user_first_name": workout.first_name,
                    "user_last_name": workout.second_name,
                    "user_birthdate": workout.birth_year if workout.birth_year else datetime.now().strftime('%Y-%m-%d'),
                    "date": competition_result.competition_date.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "sport_kind": "orient",
                    "competition_name": f'D{i + 1}',
                    "fit_file": "string",
                    "gpx_file": "string",
                    "tcx_file": "string",
                    "splits": splits
                }

                post(SPLIT_API_URL + 'workout/by_user', json=workout_data)


if __name__ == '__main__':
    main()
