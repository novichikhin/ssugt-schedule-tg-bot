from aiogram import types
from aiogram.dispatcher import FSMContext

from src.consts import MESSAGE_ON_START


async def handler_start(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state:
        await state.finish()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Выбрать группу'))

    await message.answer(MESSAGE_ON_START, reply_markup=keyboard)
