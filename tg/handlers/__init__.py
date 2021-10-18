from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from dependencies import *
from tg.handlers.start import *
from tg.handlers.schedule import *
from tg.handlers.states import *
from tg.states.group import GroupState

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(handler_start, chat_type=types.ChatType.PRIVATE, commands=start_commands)
    dp.register_message_handler(handler_group, Text(equals=groups_commands, ignore_case=True), chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(handler_cancel, Text(equals=cancel_commands, ignore_case=True), state='*')
    dp.register_message_handler(handler_schedule, chat_type=types.ChatType.PRIVATE)

    dp.register_message_handler(process_group, chat_type=types.ChatType.PRIVATE, state=GroupState.group)
    dp.register_message_handler(process_course, chat_type=types.ChatType.PRIVATE, state=GroupState.course)
    dp.register_message_handler(process_institute, chat_type=types.ChatType.PRIVATE, state=GroupState.institute)