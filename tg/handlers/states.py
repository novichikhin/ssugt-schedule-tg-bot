from dependencies import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from tg.states.group import GroupState
from tg.handlers.schedule import handler_schedule

async def handler_cancel(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is None: return None
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Выбрать группу'))

    await state.finish()
    await message.answer(MESSAGE_CANCELLED, reply_markup=keyboard)

async def process_institute(message: types.Message, state: FSMContext):
    institute = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if institute not in groups:
        await state.finish()
        keyboard.add(types.KeyboardButton(text='Выбрать группу'))
        return await message.reply(MESSAGE_INSTITUTE_NOT_FOUND, reply_markup=keyboard)

    async with state.proxy() as data:
        data['institute'] = message.text

    keyboard.add(*(types.KeyboardButton(x) for x in sorted(groups[institute].keys())))
    
    await GroupState.course.set()
    await message.reply(MESSAGE_SELECT_COURSE, reply_markup=keyboard)

async def process_course(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    course = message.text

    async with state.proxy() as data:
        institute = data['institute']
        if course not in groups[institute]:
            await state.finish()
            keyboard.add(types.KeyboardButton(text='Выбрать группу'))
            return await message.reply(MESSAGE_COURSE_NOT_FOUND, reply_markup=keyboard)

    keyboard.add(*(types.KeyboardButton(x['name']) for x in groups[institute][course]))
    
    await GroupState.group.set()
    await message.reply(MESSAGE_SELECT_GROUP, reply_markup=keyboard)

async def process_group(message: types.Message, state: FSMContext):
    await state.finish()
    await handler_schedule(message)

async def handler_group(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*(types.KeyboardButton(x) for x in groups.keys()))

    await GroupState.institute.set()
    await message.answer(MESSAGE_SELECT_INSTITUTE, reply_markup=keyboard)