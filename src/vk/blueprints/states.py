from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint, Message

from src.consts import cancel_commands, MESSAGE_CANCELLED, MESSAGE_INSTITUTE_NOT_FOUND, MESSAGE_SELECT_COURSE, \
    MESSAGE_COURSE_NOT_FOUND, MESSAGE_SELECT_GROUP, groups_commands, MESSAGE_SELECT_INSTITUTE
from src.services.groups import groups_service
from src.vk.states.group import GroupState
from src.vk.blueprints.schedule import handler_schedule

bp = Blueprint()


@bp.on.private_message(func=lambda x: x.text.lower() in cancel_commands)
async def handler_cancel(message: Message):
    curr_state_peer = message.state_peer
    if curr_state_peer is None:
        return

    keyboard = Keyboard()
    keyboard.add(Text('Выбрать группу'), color=KeyboardButtonColor.NEGATIVE)

    await bp.state_dispenser.delete(message.peer_id)
    await message.answer(MESSAGE_CANCELLED, keyboard=keyboard.get_json())


@bp.on.private_message(state=GroupState.INSTITUTE_STATE)
async def process_institute(message: Message):
    institute = message.text
    keyboard = Keyboard()

    if institute not in groups_service.get_groups():
        await bp.state_dispenser.delete(message.peer_id)
        keyboard.add(Text('Выбрать группу'), color=KeyboardButtonColor.NEGATIVE)
        return await message.answer(MESSAGE_INSTITUTE_NOT_FOUND, keyboard=keyboard.get_json())

    for index, value in enumerate(sorted(groups_service.get_groups()[institute].keys())):
        keyboard.add(Text(value), color=KeyboardButtonColor.POSITIVE)
        if index % 2 == 0:
            keyboard.row()

    await bp.state_dispenser.set(message.peer_id, GroupState.COURSE_STATE, institute=institute)
    await message.answer(MESSAGE_SELECT_COURSE, keyboard=keyboard.get_json())


@bp.on.private_message(state=GroupState.COURSE_STATE)
async def process_course(message: Message):
    course = message.text
    institute = message.state_peer.payload['institute']
    keyboard = Keyboard()

    if course not in groups_service.get_groups()[institute]:
        await bp.state_dispenser.delete(message.peer_id)
        keyboard.add(Text('Выбрать группу'), color=KeyboardButtonColor.NEGATIVE)
        return await message.answer(MESSAGE_COURSE_NOT_FOUND, keyboard=keyboard.get_json())

    for index, value in enumerate(groups_service.get_groups()[institute][course]):
        keyboard.add(Text(value['name']), color=KeyboardButtonColor.POSITIVE)
        if (index + 1) % 4 == 0:
            keyboard.row()

    await bp.state_dispenser.set(message.peer_id, GroupState.GROUP_STATE)
    await message.answer(MESSAGE_SELECT_GROUP, keyboard=keyboard.get_json())


@bp.on.private_message(state=GroupState.GROUP_STATE)
async def process_course(message: Message):
    await bp.state_dispenser.delete(message.peer_id)
    await handler_schedule(message)


@bp.on.private_message(func=lambda x: x.text.lower() in groups_commands)
async def handler_group(message: Message):
    keyboard = Keyboard()
    for x in groups_service.get_groups().keys():
        keyboard.add(Text(x), color=KeyboardButtonColor.POSITIVE)

    await bp.state_dispenser.set(message.peer_id, GroupState.INSTITUTE_STATE)
    await message.answer(MESSAGE_SELECT_INSTITUTE, keyboard=keyboard.get_json())
