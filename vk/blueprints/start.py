from dependencies import *
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint, Message

bp = Blueprint()

@bp.on.private_message(text=start_commands)
async def handler_start(message: Message):
    keyboard = Keyboard()
    keyboard.add(Text('Выбрать группу'), color=KeyboardButtonColor.NEGATIVE)

    await message.answer(MESSAGE_ON_START, keyboard=keyboard)