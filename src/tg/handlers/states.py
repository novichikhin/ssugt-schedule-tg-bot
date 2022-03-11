from aiogram import types
from aiogram.dispatcher import FSMContext

from src.consts import MESSAGE_CANCELLED, MESSAGE_INSTITUTE_NOT_FOUND, MESSAGE_SELECT_COURSE, MESSAGE_COURSE_NOT_FOUND, \
    MESSAGE_SELECT_GROUP, MESSAGE_SELECT_INSTITUTE, MESSAGE_FORM_OF_TRAINING_NOT_FOUND, MESSAGE_SELECT_FORM_OF_TRAINING, \
    KEYBOARD_BUTTON_CHOOSE_GROUP
from src.services.groups import groups_service
from src.tg.states.group import GroupState
from src.tg.handlers.schedule import handler_schedule


async def handler_cancel(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is None:
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text=KEYBOARD_BUTTON_CHOOSE_GROUP))

    await state.finish()
    await message.answer(MESSAGE_CANCELLED, reply_markup=keyboard)


async def process_institute(message: types.Message, state: FSMContext):
    institute = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if institute not in groups_service.get_groups():
        await state.finish()
        keyboard.add(types.KeyboardButton(text=KEYBOARD_BUTTON_CHOOSE_GROUP))
        return await message.reply(MESSAGE_INSTITUTE_NOT_FOUND, reply_markup=keyboard)

    async with state.proxy() as data:
        data['institute'] = message.text

    keyboard.add(*(types.KeyboardButton(x) for x in sorted(groups_service.get_groups()[institute].keys())))

    await GroupState.course.set()
    await message.reply(MESSAGE_SELECT_COURSE, reply_markup=keyboard)


async def process_course(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    course = message.text

    async with state.proxy() as data:
        institute = data['institute']
        if course not in groups_service.get_groups()[institute]:
            await state.finish()
            keyboard.add(types.KeyboardButton(text=KEYBOARD_BUTTON_CHOOSE_GROUP))
            return await message.reply(MESSAGE_COURSE_NOT_FOUND, reply_markup=keyboard)

        data['course'] = course

    keyboard.add(*(types.KeyboardButton(x) for x in groups_service.get_groups()[institute][course].keys()))

    await GroupState.form_of_training.set()
    await message.reply(MESSAGE_SELECT_FORM_OF_TRAINING, reply_markup=keyboard)


async def process_form_of_training(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    form_of_training = message.text

    async with state.proxy() as data:
        institute = data['institute']
        course = data['course']

        if form_of_training not in groups_service.get_groups()[institute][course]:
            await state.finish()
            keyboard.add(types.KeyboardButton(text=KEYBOARD_BUTTON_CHOOSE_GROUP))
            return await message.reply(MESSAGE_FORM_OF_TRAINING_NOT_FOUND, reply_markup=keyboard)

    keyboard.add(*(types.KeyboardButton(x['name']) for x in groups_service.get_groups()[institute][course][form_of_training]))

    await GroupState.group.set()
    await message.reply(MESSAGE_SELECT_GROUP, reply_markup=keyboard)


async def process_group(message: types.Message, state: FSMContext):
    await state.finish()
    await handler_schedule(message)


async def handler_group(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*(types.KeyboardButton(x) for x in groups_service.get_groups().keys()))

    await GroupState.institute.set()
    await message.answer(MESSAGE_SELECT_INSTITUTE, reply_markup=keyboard)
