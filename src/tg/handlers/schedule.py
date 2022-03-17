import datetime
import logging

import httpx
from aiogram import types
from aiogram.dispatcher.webhook import DeleteMessage

from src.consts import MESSAGE_STOP_FLOOD, MESSAGE_GROUP_NOT_FOUND, MESSAGE_SCHEDULE_NOT_FOUND, \
    MESSAGE_CONNECTION_PROBLEM, MESSAGE_SOMETHING_WENT_WRONG, \
    KEYBOARD_BUTTON_CHOOSE_GROUP, MESSAGE_SELECT_OTHER_GROUP
from src.exceptions import ScheduleNotFound, GroupNotFound
from src.services.calendar import CalendarService
from src.services.schedule import schedule_service
from src.services.user import user_service


async def handler_schedule(message: types.Message):
    text = message.text.lower().strip()
    user_id = message.from_user.id

    if user_service[user_id].is_flood():
        return await message.reply(MESSAGE_STOP_FLOOD)

    user_service[user_id].add_flood_delay()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=KEYBOARD_BUTTON_CHOOSE_GROUP))

    try:
        for message_id in user_service[user_id].get_messages():
            await DeleteMessage(chat_id=message.chat.id, message_id=message_id).execute_response(message.bot)

        user_service[user_id].clear_messages()

        curr_date = datetime.date.today()

        group_name, schedule, max_date = await schedule_service.get_schedule(text, curr_date)
        keyboard.insert(types.KeyboardButton(text=group_name))

        detailed_telegram_calendar = CalendarService(locale='ru', min_date=datetime.date.today(), max_date=max_date)

        calendar, _ = detailed_telegram_calendar.build()

        user_service[user_id].add_message((await message.answer(schedule, reply_markup=calendar)).message_id)
        await message.answer(MESSAGE_SELECT_OTHER_GROUP, reply_markup=keyboard)

        user_service[user_id].set_group({'name': group_name, 'max_date': max_date, 'last_date': curr_date})
    except GroupNotFound:
        await message.reply(MESSAGE_GROUP_NOT_FOUND, reply_markup=keyboard)
    except ScheduleNotFound:
        await message.answer(MESSAGE_SCHEDULE_NOT_FOUND, reply_markup=keyboard)
    except httpx.HTTPError:
        logging.exception('HTTP Exception')
        await message.answer(MESSAGE_CONNECTION_PROBLEM, reply_markup=keyboard)
    except Exception:
        logging.exception('Sending a schedule')
        await message.answer(MESSAGE_SOMETHING_WENT_WRONG, reply_markup=keyboard)


async def handler_keyboard_calendar_schedule(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    group = user_service[user_id].get_group()

    detailed_telegram_calendar = CalendarService(locale='ru', min_date=datetime.date.today(), max_date=group['max_date'])
    selected, keyboard, step = detailed_telegram_calendar.process(
        callback_query.data)

    try:
        if not selected and keyboard:
            await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        elif selected:
            if 'last_date' not in group or group['last_date'] != selected:
                detailed_telegram_calendar.current_date = selected
                keyboard, _ = detailed_telegram_calendar.build()

                _, schedule, _ = await schedule_service.get_schedule(group['name'].lower(), selected)
                await callback_query.message.edit_text(schedule, reply_markup=keyboard)
    except GroupNotFound:
        await callback_query.message.answer(MESSAGE_GROUP_NOT_FOUND)
    except ScheduleNotFound:
        await callback_query.message.answer(MESSAGE_SCHEDULE_NOT_FOUND)
    except httpx.HTTPError:
        logging.exception('HTTP Exception')
        await callback_query.message.answer(MESSAGE_CONNECTION_PROBLEM)
    except Exception:
        logging.exception('Sending a schedule')
        await callback_query.message.answer(MESSAGE_SOMETHING_WENT_WRONG)
    finally:
        await callback_query.answer()

        if selected is not None:
            group['last_date'] = selected
            user_service[user_id].set_group(group)
