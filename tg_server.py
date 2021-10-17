from dependencies import *
from aiogram import Bot, Dispatcher, executor, types
from tg.config import TgConfig

logging.basicConfig(filename='tg_server.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

bot = Bot(token=TgConfig.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(chat_type=types.ChatType.PRIVATE, commands=start_commands)
async def handler_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Группы'))

    await message.answer(MESSAGE_ON_START, reply_markup=keyboard)

@dp.message_handler(chat_type=types.ChatType.PRIVATE)
async def handler_any(message: types.Message):
    text = message.text.lower().strip()
    user_id = message.from_user.id
    cur_time = time.time()

    if (user_id in spam_list) and (spam_list[user_id] > cur_time):
        return await message.reply(MESSAGE_STOP_FLOOD)

    spam_list[user_id] = cur_time + Config.SPAM_DELAY

    if any(groups_command in text for groups_command in groups_commands):
        return await message.answer(get_groups_message())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Группы'))

    group_found = find_group(text)
    if group_found is None:
        return await message.reply(MESSAGE_GROUP_NOT_FOUND, reply_markup=keyboard)

    keyboard.add(types.KeyboardButton(text=group_found['name']))

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL+group_found['url'])

        schedule = get_schedule_parse(response.text)
        await message.answer(schedule, reply_markup=keyboard)
    except ScheduleNotFound:
        await message.answer(MESSAGE_SCHEDULE_NOT_FOUND, reply_markup=keyboard)
    except CurrentWeekNotFound:
        await message.answer(MESSAGE_CURRENT_WEEK_NOT_FOUND, reply_markup=keyboard)
    except httpx.HTTPError:
        await message.answer(MESSAGE_CONNECTION_PROBLEM, reply_markup=keyboard)
    except:
        logging.exception('Sending a schedule')
        await message.answer(MESSAGE_SOMETHING_WENT_WRONG, reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)