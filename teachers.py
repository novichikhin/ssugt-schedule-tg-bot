import json

import httpx
from httpx import Response

from src.consts import SCHEDULE_URL, TEACHERS_LIST
from src.parse.teachers import TeachersParser


def get_teachers_list() -> None:
    try:
        with httpx.Client() as client:
            response: Response = client.get(SCHEDULE_URL + TEACHERS_LIST)

        teachers_parser = TeachersParser(response.text)

        with open('teachers.json', 'w', encoding='utf-8') as f:
            json.dump(teachers_parser.get_teachers(), f, ensure_ascii=False, indent=4, sort_keys=True)
    except httpx.HTTPError as e:
        print(str(e))


if __name__ == '__main__':
    get_teachers_list()
