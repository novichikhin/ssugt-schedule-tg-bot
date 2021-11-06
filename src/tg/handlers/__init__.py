from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from src.consts import start_commands, groups_commands, cancel_commands
from src.tg.handlers.schedule import handler_schedule
from src.tg.handlers.start import handler_start
from src.tg.handlers.states import handler_group, handler_cancel, process_group, process_course, process_institute
from src.tg.states.group import GroupState


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handler_start, chat_type=types.ChatType.PRIVATE, commands=start_commands)
    dp.register_message_handler(handler_group, Text(equals=groups_commands, ignore_case=True),
                                chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(handler_cancel, Text(equals=cancel_commands, ignore_case=True), state='*')
    dp.register_message_handler(handler_schedule, chat_type=types.ChatType.PRIVATE)

    dp.register_message_handler(process_group, chat_type=types.ChatType.PRIVATE, state=GroupState.group)
    dp.register_message_handler(process_course, chat_type=types.ChatType.PRIVATE, state=GroupState.course)
    dp.register_message_handler(process_institute, chat_type=types.ChatType.PRIVATE, state=GroupState.institute)
