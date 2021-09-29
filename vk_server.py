import asyncio
import time
import json
import httpx

from aiovk import API
from aiovk.longpoll import BotsLongPoll
from aiovk.sessions import TokenSession

from utils import get_groups_message, find_group
from consts import groups_commands, start_commands, spam_list, \
    SCHEDULE_URL, SPAM_DELAY, MESSAGE_STOP_FLOOD, MESSAGE_GROUP_NOT_FOUND, \
    MESSAGE_SCHEDULE_NOT_FOUND, MESSAGE_CURRENT_WEEK_NOT_FOUND, MESSAGE_CONNECTION_PROBLEM, MESSAGE_ON_START

from parse.utils import get_schedule_parse
from exceptions import ScheduleNotFound, CurrentWeekNotFound
from vk.config import VkConfig

api = None
CHAT_START_ID = int(2E9)

async def worker(event):
    global test
    if event['type'] != 'message_new': return None

    keyboard = {
        'buttons':[
            [
                {'action':{'type':'text','label':'Группы','payload':''},'color':'negative'},
            ],
            [
                {'action':{'type':'open_link','link':f'{SCHEDULE_URL}','label':'Расписание СГУГиТ','payload':''}}
            ]
        ]
    }
    user_id = event['object']['message']['peer_id']

    if user_id >= CHAT_START_ID: return None

    text = event['object']['message']['text'].lower().strip()

    if text.startswith(tuple(start_commands)):
        await api('messages.send', peer_id=user_id, random_id=0, message=MESSAGE_ON_START, keyboard=json.dumps(keyboard))
        return None
    
    cur_time = time.time()

    if (user_id in spam_list) and (spam_list[user_id] > cur_time):
        await api('messages.send', peer_id=user_id, random_id=0, message=MESSAGE_STOP_FLOOD)
        return None
    
    spam_list[user_id] = cur_time + SPAM_DELAY

    if any(groups_command in text for groups_command in groups_commands):
        await api('messages.send', peer_id=user_id, random_id=0, message=get_groups_message())
        return None

    group_found = find_group(text)
    if group_found is None:
        await api('messages.send', peer_id=user_id, random_id=0, message=MESSAGE_GROUP_NOT_FOUND, keyboard=json.dumps(keyboard))
        return None

    keyboard['buttons'] = [keyboard['buttons'][0] + [{'action':{'type':'text','label':group_found['name'],'payload':''},'color':'positive'}]] + [keyboard['buttons'][1]]

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL+group_found['url'])

        schedule = get_schedule_parse(response.text)
    except ScheduleNotFound:
        await api('messages.send', peer_id=user_id, random_id=0, message=MESSAGE_SCHEDULE_NOT_FOUND, keyboard=json.dumps(keyboard))
    except CurrentWeekNotFound:
        await api('messages.send', peer_id=user_id, random_id=0, message=MESSAGE_CURRENT_WEEK_NOT_FOUND, keyboard=json.dumps(keyboard))
    except:
        await api('messages.send', peer_id=user_id, random_id=0, message=MESSAGE_CONNECTION_PROBLEM, keyboard=json.dumps(keyboard))
    finally:
        await api('messages.send', peer_id=user_id, random_id=0, message=schedule, keyboard=json.dumps(keyboard))

async def main():
    global api
    async with TokenSession(access_token=VkConfig.ACCESS_TOKEN) as session:
        api = API(session)
        lp = BotsLongPoll(session, group_id=VkConfig.GROUP_ID)

        async for event in lp.iter():
            asyncio.get_event_loop().create_task(worker(event))

if __name__ == '__main__':
    asyncio.run(main())