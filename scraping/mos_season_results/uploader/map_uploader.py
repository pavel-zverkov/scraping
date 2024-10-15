from json import dumps
from typing import Any
from requests import post, Response

from ...abase.utils.datetime_json_encoder import DateTimeEncoder
from ...logger import logger
from ..constants import SPLIT_API_URL


class MapUploader:

    def upload(self, map_url: str, competition: dict[str, Any]) -> None:

        map_dict = {
            "artifact_params": {
                "file_name": f"map_{competition.get('name')}.jpeg".lower(),
                "kind": "o_map",
                "tags": f"#{competition.get('location')}",
                "competition": competition.get('id'),
                "uploader": 380
            },
            "artifact_kind_spec": {}
        }

        response_map = post(
            SPLIT_API_URL + 'artifact/',
            params={'artifact_url': map_url},
            data=dumps(map_dict, cls=DateTimeEncoder)
        )
        self._post_status(response_map)

        logger.success(f'Success upload map for {competition.get("name")}')

    @staticmethod
    def _post_status(response: Response) -> None:
        if response.status_code != 200:
            logger.error(response.text)
