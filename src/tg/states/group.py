from aiogram.dispatcher.filters.state import State, StatesGroup


class GroupState(StatesGroup):
    type = State()
    institute = State()
    course = State()
    form_of_training = State()
    group = State()
