from collections import defaultdict
from typing import DefaultDict, List

import httpx

from src.consts import SCHEDULE_URL
from src.parse.audiences import AudiencesParser


class AudiencesService:
    def __init__(self):
        try:
            with httpx.Client() as client:
                response = client.get(SCHEDULE_URL + '?sec=3')

            audiences_parser = AudiencesParser(response.text)
            self._audiences = audiences_parser.get_audiences()
        except httpx.HTTPError:
            self._audiences = defaultdict(list)

    def get_audiences(self) -> DefaultDict[str, List]:
        return self._audiences


audiences_service = AudiencesService()
