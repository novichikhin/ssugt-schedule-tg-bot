import asyncio
import json
import httpx

from parse.groups import GroupsParser
from consts import SCHEDULE_URL, GROUPS_PARAMETERS

groups_parser = GroupsParser()

async def get_response(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)

async def get_group_parse(group_parameters):
    try:
        response = await get_response(SCHEDULE_URL+group_parameters)
        if response.status_code != 200: return None
    except: return None
    groups_parser.add_group(response.text)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        tasks = [loop.create_task(get_group_parse(group_parameters)) for group_parameters in GROUPS_PARAMETERS]
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        loop.close()

        with open('groups.json', 'w', encoding='utf-8') as f:
            json.dump(groups_parser.get_groups(), f, ensure_ascii=False, indent=4)