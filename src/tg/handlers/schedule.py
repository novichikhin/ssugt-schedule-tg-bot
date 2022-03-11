import logging

import httpx
from aiogram import types

from src.consts import MESSAGE_STOP_FLOOD, MESSAGE_GROUP_NOT_FOUND, SCHEDULE_URL, MESSAGE_SCHEDULE_NOT_FOUND, \
    MESSAGE_CURRENT_WEEK_NOT_FOUND, MESSAGE_CONNECTION_PROBLEM, MESSAGE_SOMETHING_WENT_WRONG, \
    KEYBOARD_BUTTON_CHOOSE_GROUP
from src.exceptions import ScheduleNotFound, CurrentWeekNotFound

from src.services.groups import groups_service
from src.services.schedule import schedule_service
from src.services.user import user_service


async def handler_schedule(message: types.Message):
    text = message.text.lower().strip()
    user_id = message.from_user.id

    if user_service[user_id].is_flood():
        return await message.reply(MESSAGE_STOP_FLOOD)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=KEYBOARD_BUTTON_CHOOSE_GROUP))

    group_found = groups_service.find_group(text)
    if group_found is None:
        return await message.reply(MESSAGE_GROUP_NOT_FOUND, reply_markup=keyboard)

    keyboard.insert(types.KeyboardButton(text=group_found['name']))

    schedule = schedule_service.get_cache(group_found['name'])

    try:
        if schedule is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(SCHEDULE_URL+group_found['url'])

            schedule = schedule_service.get_schedule(response.text)
            schedule_service.set_cache(group_found['name'], schedule)

        await message.answer(schedule, reply_markup=keyboard)
        user_service[user_id].add_flood_delay()
    except ScheduleNotFound:
        await message.answer(MESSAGE_SCHEDULE_NOT_FOUND, reply_markup=keyboard)
    except CurrentWeekNotFound:
        await message.answer(MESSAGE_CURRENT_WEEK_NOT_FOUND, reply_markup=keyboard)
    except httpx.HTTPError as e:
        logging.exception(f'HTTP Exception {e}')
        await message.answer(MESSAGE_CONNECTION_PROBLEM, reply_markup=keyboard)
    except Exception:
        logging.exception('Sending a schedule')
        await message.answer(MESSAGE_SOMETHING_WENT_WRONG, reply_markup=keyboard)
