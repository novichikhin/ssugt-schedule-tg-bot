import asyncio
import json
from enum import Enum, auto

import httpx
from httpx import Response

from src.consts import SCHEDULE_URL, INSTITUTES_PARAMETERS
from src.parse.groups import GroupsParser
from src.parse.institute import InstituteParser

institute_parser = InstituteParser()
groups_parser = GroupsParser()
groups_parsed_params = set()


class InstituteData(Enum):
    forms_of_training = auto()
    courses = auto()
    groups = auto()


async def get_institute_data(param: str, institute_data_type: InstituteData) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(SCHEDULE_URL + param)

        match institute_data_type:
            case InstituteData.forms_of_training:
                institute_parser.add_forms_of_training(response.text)
            case InstituteData.courses:
                institute_parser.add_courses(response.text)

        if param not in groups_parsed_params:
            groups_parser.add_group(response.text)
            groups_parsed_params.add(param)

    except httpx.HTTPError as e:
        print(str(e))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        tasks = [loop.create_task(get_institute_data(institute_parameter, InstituteData.forms_of_training)) for
                 institute_parameter in
                 INSTITUTES_PARAMETERS]
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        forms_of_training = [j for i in institute_parser.get_forms_of_training().values() for j in i.values()]

        try:
            tasks = [loop.create_task(get_institute_data(form_of_training, InstituteData.courses)) for form_of_training
                     in
                     forms_of_training]
            loop.run_until_complete(asyncio.wait(tasks))
        finally:

            groups_parameters = []
            for i in institute_parser.get_courses().values():
                for j in i.values():
                    groups_parameters += j

            groups_parameters = [i for i in groups_parameters if i not in groups_parsed_params]

            try:
                tasks = [loop.create_task(get_institute_data(group_parameters, InstituteData.groups)) for
                         group_parameters in groups_parameters]
                loop.run_until_complete(asyncio.wait(tasks))
            finally:
                loop.close()

                with open('groups.json', 'w', encoding='utf-8') as f:
                    json.dump(groups_parser.get_groups(), f, ensure_ascii=False, indent=4, sort_keys=True)
