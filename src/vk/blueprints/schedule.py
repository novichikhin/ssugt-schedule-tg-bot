import logging

import httpx
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint, Message

from src.consts import MESSAGE_STOP_FLOOD, MESSAGE_GROUP_NOT_FOUND, SCHEDULE_URL, MESSAGE_SCHEDULE_NOT_FOUND, \
    MESSAGE_CURRENT_WEEK_NOT_FOUND, MESSAGE_CONNECTION_PROBLEM, MESSAGE_SOMETHING_WENT_WRONG
from src.exceptions import ScheduleNotFound, CurrentWeekNotFound

from src.services.groups import groups_service
from src.services.schedule import schedule_service
from src.services.user import user_service

bp = Blueprint()


@bp.on.private_message()
async def handler_schedule(message: Message):
    text = message.text.lower().strip()
    user_id = message.peer_id

    if user_service[user_id].is_flood():
        return await message.answer(MESSAGE_STOP_FLOOD)

    keyboard = Keyboard()
    keyboard.add(Text('Выбрать группу'), color=KeyboardButtonColor.NEGATIVE)

    group_found = groups_service.find_group(text)
    if group_found is None:
        return await message.answer(MESSAGE_GROUP_NOT_FOUND, keyboard=keyboard.get_json())

    keyboard.add(Text(group_found['name']), color=KeyboardButtonColor.POSITIVE)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL + group_found['url'])

        schedule = schedule_service.get_schedule(response.text)
        await message.answer(schedule, keyboard=keyboard.get_json())

        user_service[user_id].add_flood_delay()
    except ScheduleNotFound:
        await message.answer(MESSAGE_SCHEDULE_NOT_FOUND, keyboard=keyboard.get_json())
    except CurrentWeekNotFound:
        await message.answer(MESSAGE_CURRENT_WEEK_NOT_FOUND, keyboard=keyboard.get_json())
    except httpx.HTTPError:
        await message.answer(MESSAGE_CONNECTION_PROBLEM, keyboard=keyboard.get_json())
    except Exception:
        logging.exception('Sending a schedule')
        await message.answer(MESSAGE_SOMETHING_WENT_WRONG, keyboard=keyboard.get_json())
