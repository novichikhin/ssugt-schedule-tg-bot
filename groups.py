import asyncio
import json
import httpx

from src.parse.groups import GroupsParser
from src.consts import SCHEDULE_URL, GROUPS_PARAMETERS

groups_parser = GroupsParser()


async def get_group_parse(group_parameters: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL + group_parameters)

        if response.status_code != httpx.codes.OK:
            return

        groups_parser.add_group(response.text)
    except httpx.HTTPError:
        pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        tasks = [loop.create_task(get_group_parse(group_parameters)) for group_parameters in GROUPS_PARAMETERS]
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        loop.close()

        with open('groups.json', 'w', encoding='utf-8') as f:
            json.dump(groups_parser.get_groups(), f, ensure_ascii=False, indent=4, sort_keys=True)
