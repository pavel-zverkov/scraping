from json import dumps, loads
from requests import post
from tqdm import tqdm

from ...abase.utils.datetime_json_encoder import DateTimeEncoder
from ...logger import logger

from ..constants import SPLIT_API_URL
from ..api_results import APIResults


class ResultUploader:

    def upload(self, results: APIResults) -> None:

        post(
            SPLIT_API_URL + 'event/',
            data=dumps(results.event.__dict__, cls=DateTimeEncoder)
        )

        for competition_result in results.results:
            logger.info(competition_result.competition.name)
            post(
                SPLIT_API_URL + 'competition/',
                data=dumps(competition_result.competition.__dict__,
                           cls=DateTimeEncoder)
            )

            for workout in tqdm(competition_result.workout_list):
                post(
                    SPLIT_API_URL + 'workout/by_user',
                    data=dumps(workout.__dict__, cls=DateTimeEncoder)
                )
            logger.success(
                f'Success upload results for {competition_result.competition.name}')
