import asyncio
import json
import httpx

from src.parse.groups import GroupsParser
from src.consts import SCHEDULE_URL, INSTITUTES_PARAMETERS
from src.parse.institute import InstituteParser

institute_parser = InstituteParser()
groups_parser = GroupsParser()


async def get_forms_of_training(institute_parameter: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL + institute_parameter)

        institute_parser.add_forms_of_training(response.text)
    except httpx.HTTPError:
        pass


async def get_courses(form_of_training_parameter: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL + form_of_training_parameter)

        institute_parser.add_courses(response.text)
    except httpx.HTTPError:
        pass


async def get_groups(group_parameters: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL + group_parameters)

        groups_parser.add_group(response.text)
    except httpx.HTTPError:
        pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        tasks = [loop.create_task(get_forms_of_training(institute_parameter)) for institute_parameter in
                 INSTITUTES_PARAMETERS]
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        forms_of_training = [j for i in institute_parser.get_forms_of_training().values() for j in i.values()]

        try:
            tasks = [loop.create_task(get_courses(form_of_training)) for form_of_training in
                     forms_of_training]
            loop.run_until_complete(asyncio.wait(tasks))
        finally:

            groups_parameters = []
            for i in institute_parser.get_courses().values():
                for j in i.values():
                    groups_parameters += j

            try:
                tasks = [loop.create_task(get_groups(group_parameters)) for group_parameters in groups_parameters]
                loop.run_until_complete(asyncio.wait(tasks))
            finally:
                loop.close()

                with open('groups.json', 'w', encoding='utf-8') as f:
                    json.dump(groups_parser.get_groups(), f, ensure_ascii=False, indent=4, sort_keys=True)
