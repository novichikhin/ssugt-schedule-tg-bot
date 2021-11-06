from aiogram import types

from src.consts import MESSAGE_ON_START


async def handler_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Выбрать группу'))

    await message.answer(MESSAGE_ON_START, reply_markup=keyboard)