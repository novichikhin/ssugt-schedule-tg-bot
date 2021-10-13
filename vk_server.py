import time
import httpx

from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message

from config import Config
from utils import get_groups_message, find_group, get_schedule_parse
from consts import groups_commands, start_commands, spam_list, \
    SCHEDULE_URL, MESSAGE_STOP_FLOOD, MESSAGE_GROUP_NOT_FOUND, \
    MESSAGE_SCHEDULE_NOT_FOUND, MESSAGE_CURRENT_WEEK_NOT_FOUND, MESSAGE_CONNECTION_PROBLEM, MESSAGE_ON_START
from exceptions import ScheduleNotFound, CurrentWeekNotFound

from vk.config import VkConfig

bot = Bot(VkConfig.ACCESS_TOKEN)

@bot.on.private_message(text=start_commands)
async def handler_start(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text('Группы'), color=KeyboardButtonColor.NEGATIVE)

    await message.answer(MESSAGE_ON_START, keyboard=keyboard)

@bot.on.private_message()
async def handler_any(message: Message):
    text = message.text.lower().strip()
    user_id = message.peer_id
    cur_time = time.time()

    if (user_id in spam_list) and (spam_list[user_id] > cur_time):
        await message.answer(MESSAGE_STOP_FLOOD)
        return None

    spam_list[user_id] = cur_time + Config.SPAM_DELAY

    if any(groups_command in text for groups_command in groups_commands):
        await message.answer(get_groups_message())
        return None

    keyboard = Keyboard()
    keyboard.add(Text('Группы'), color=KeyboardButtonColor.NEGATIVE)

    group_found = find_group(text)
    if group_found is None:
        await message.answer(MESSAGE_GROUP_NOT_FOUND, reply_markup=keyboard)
        return None

    keyboard.add(Text(group_found['name']), color=KeyboardButtonColor.POSITIVE)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(SCHEDULE_URL+group_found['url'])

        schedule = get_schedule_parse(response.text)
        await message.answer(schedule, keyboard=keyboard)
    except ScheduleNotFound:
        await message.answer(MESSAGE_SCHEDULE_NOT_FOUND, keyboard=keyboard)
    except CurrentWeekNotFound:
        await message.answer(MESSAGE_CURRENT_WEEK_NOT_FOUND, keyboard=keyboard)
    except:
        await message.answer(MESSAGE_CONNECTION_PROBLEM, keyboard=keyboard)

if __name__ == '__main__':
    bot.run_forever()