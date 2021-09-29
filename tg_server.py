import time
import httpx
from aiogram import Bot, Dispatcher, executor, types

from tg.config import TgConfig
from parse.utils import get_schedule_parse
from exceptions import ScheduleNotFound, CurrentWeekNotFound

from utils import get_groups_message, find_group
from consts import groups_commands, start_commands, spam_list, \
    SCHEDULE_URL, SPAM_DELAY, MESSAGE_STOP_FLOOD, MESSAGE_GROUP_NOT_FOUND, \
    MESSAGE_SCHEDULE_NOT_FOUND, MESSAGE_CURRENT_WEEK_NOT_FOUND, MESSAGE_CONNECTION_PROBLEM, MESSAGE_ON_START

bot = Bot(token=TgConfig.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=start_commands)
async def handler_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Группы'))

    await message.answer(MESSAGE_ON_START, reply_markup=keyboard)

@dp.message_handler()
async def handler_any(message: types.Message):
    text = message.text.lower().strip()
    user_id = message.from_user.id
    cur_time = time.time()

    if (user_id in spam_list) and (spam_list[user_id] > cur_time):
        await message.reply(MESSAGE_STOP_FLOOD)
        return None

    spam_list[user_id] = cur_time + SPAM_DELAY

    if any(groups_command in text for groups_command in groups_commands):
        await message.answer(get_groups_message())
        return None

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Группы'))

    group_found = find_group(text)
    if group_found is None:
        await message.reply(MESSAGE_GROUP_NOT_FOUND, reply_markup=keyboard)
        return None

    keyboard.add(types.KeyboardButton(text=group_found['name']))

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL+group_found['url'])

        schedule = get_schedule_parse(response.text)
    except ScheduleNotFound:
        await message.answer(MESSAGE_SCHEDULE_NOT_FOUND, reply_markup=keyboard)
    except CurrentWeekNotFound:
        await message.answer(MESSAGE_CURRENT_WEEK_NOT_FOUND, reply_markup=keyboard)
    except:
        await message.answer(MESSAGE_CONNECTION_PROBLEM, reply_markup=keyboard)
    finally:
        await message.answer(schedule, reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)