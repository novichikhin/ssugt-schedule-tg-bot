from dependencies import *
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message
from vk.config import VkConfig

logging.basicConfig(filename='vk_server.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

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
        return await message.answer(MESSAGE_STOP_FLOOD)

    spam_list[user_id] = cur_time + Config.SPAM_DELAY

    if any(groups_command in text for groups_command in groups_commands):
        return await message.answer(get_groups_message())

    keyboard = Keyboard()
    keyboard.add(Text('Группы'), color=KeyboardButtonColor.NEGATIVE)

    group_found = find_group(text)
    if group_found is None:
        return await message.answer(MESSAGE_GROUP_NOT_FOUND, reply_markup=keyboard)

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
    except httpx.HTTPError:
        await message.answer(MESSAGE_CONNECTION_PROBLEM, keyboard=keyboard)
    except:
        logging.exception('Sending a schedule')
        await message.answer(MESSAGE_SOMETHING_WENT_WRONG, keyboard=keyboard)

if __name__ == '__main__':
    bot.run_forever()