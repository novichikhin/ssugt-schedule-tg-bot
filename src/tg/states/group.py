from aiogram.dispatcher.filters.state import State, StatesGroup


class GroupState(StatesGroup):
    institute = State()
    course = State()
    form_of_training = State()
    group = State()
