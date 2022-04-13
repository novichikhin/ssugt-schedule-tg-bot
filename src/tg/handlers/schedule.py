import datetime
import logging

import httpx
from aiogram import types

from src.consts import MESSAGE_STOP_FLOOD, MESSAGE_SCHEDULE_NOT_FOUND, \
    MESSAGE_CONNECTION_PROBLEM, MESSAGE_SOMETHING_WENT_WRONG, \
    KEYBOARD_BUTTON_CHOOSE_SCHEDULE, MESSAGE_SELECT_OTHER_SCHEDULE
from src.exceptions import ScheduleNotFound
from src.services.calendar import CalendarService
from src.services.schedule import schedule_service
from src.services.user import user_service


async def handler_schedule(message: types.Message):
    text = message.text.lower().strip()
    user_id = message.from_user.id

    if user_service[user_id].is_flood() or user_service[user_id].group['in_proccesing']:
        return await message.reply(MESSAGE_STOP_FLOOD)

    user_service[user_id].add_flood_delay()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=KEYBOARD_BUTTON_CHOOSE_SCHEDULE))

    try:
        user_service[user_id].group['in_proccesing'] = True

        curr_date = datetime.date.today()

        group_name, schedule, min_date, max_date = await schedule_service.get_schedule(text)
        formated_schedule = schedule_service.filter_schedule(text, schedule, curr_date)

        keyboard.insert(types.KeyboardButton(text=group_name))

        detailed_telegram_calendar = CalendarService(locale='ru', min_date=min_date, current_date=datetime.date.today(),
                                                     max_date=max_date)

        calendar, _ = detailed_telegram_calendar.build()

        await message.answer(formated_schedule, reply_markup=calendar)
        await message.answer(MESSAGE_SELECT_OTHER_SCHEDULE, reply_markup=keyboard)
    except ScheduleNotFound:
        await message.answer(MESSAGE_SCHEDULE_NOT_FOUND, reply_markup=keyboard)
    except httpx.HTTPError:
        logging.exception('HTTP Exception')
        await message.answer(MESSAGE_CONNECTION_PROBLEM, reply_markup=keyboard)
    except Exception as e:
        logging.exception('Sending a schedule')
        await message.answer(MESSAGE_SOMETHING_WENT_WRONG, reply_markup=keyboard)
    finally:
        if user_service[user_id].group['in_proccesing']:
            user_service[user_id].group['in_proccesing'] = False


async def handler_keyboard_calendar_schedule(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if user_service[user_id].group['in_proccesing']:
        await callback_query.answer()
        return

    try:
        user_service[user_id].group['in_proccesing'] = True

        key = schedule_service.parse_key(callback_query.message.text)
        _, schedule, min_date, max_date = await schedule_service.get_schedule(key)

        detailed_telegram_calendar = CalendarService(locale='ru', min_date=min_date, max_date=max_date,
                                                     current_date=datetime.date.today())
        selected, keyboard, step = detailed_telegram_calendar.process(
            callback_query.data)

        if not selected and keyboard:
            if callback_query.message.reply_markup.as_json() != keyboard:
                await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        elif selected:
            formated_schedule = schedule_service.filter_schedule(key, schedule, selected)

            if callback_query.message.text != formated_schedule:
                detailed_telegram_calendar.current_date = selected
                keyboard, _ = detailed_telegram_calendar.build()

                await callback_query.message.edit_text(formated_schedule, reply_markup=keyboard)
    except ScheduleNotFound:
        await callback_query.message.reply(MESSAGE_SCHEDULE_NOT_FOUND)
    except httpx.HTTPError:
        logging.exception('HTTP Exception')
        await callback_query.message.reply(MESSAGE_CONNECTION_PROBLEM)
    except Exception as e:
        logging.exception('Sending a schedule')
        await callback_query.message.reply(MESSAGE_SOMETHING_WENT_WRONG)
    finally:
        await callback_query.answer()

        if user_service[user_id].group['in_proccesing']:
            user_service[user_id].group['in_proccesing'] = False
