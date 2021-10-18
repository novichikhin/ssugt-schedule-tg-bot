from aiogram.dispatcher.filters.state import State, StatesGroup

class GroupState(StatesGroup):
    institute = State()
    course = State()
    group = State()