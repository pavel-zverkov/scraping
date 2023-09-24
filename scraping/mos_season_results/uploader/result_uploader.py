from json import dumps, loads
from requests import Response, post
from tqdm import tqdm

from ...abase.utils.datetime_json_encoder import DateTimeEncoder
from ...logger import logger

from ..constants import SPLIT_API_URL
from ..api_results import APIResults


class ResultUploader:

    def upload(self, results: APIResults) -> None:

        response_event = post(
            SPLIT_API_URL + 'event/',
            data=dumps(results.event.__dict__, cls=DateTimeEncoder)
        )
        self._post_status(response_event)

        for competition_result in results.results:
            logger.info(competition_result.competition.name)
            logger.info(competition_result.competition.date)

            competition_dict = competition_result.competition.__dict__
            competition_dict.update({'event': response_event.json()['id']})

            response_competition = post(
                SPLIT_API_URL + 'competition/',
                data=dumps(
                    competition_dict,
                    cls=DateTimeEncoder
                )
            )
            self._post_status(response_competition)

            for workout in tqdm(competition_result.workout_list):
                response_workout = post(
                    SPLIT_API_URL + 'workout/by_user',
                    data=dumps(workout.__dict__, cls=DateTimeEncoder)
                )
            self._post_status(response_workout)

            logger.success(
                f'Success upload results for {competition_result.competition.name}')

    @staticmethod
    def _post_status(response: Response) -> None:
        if response.status_code != 200:
            logger.error(response.text)
