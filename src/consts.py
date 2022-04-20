from enum import Enum


class ChooseType(Enum):
    student = 'Студент'
    teacher = 'Преподаватель'


SELECT_COMMANDS = [
    'список групп',
    'группы',
    'выбрать группу',
    'выбрать расписание',
    'расписание'
]

START_COMMANDS = [
    'старт',
    'start',
    'help',
    'помощь'
]

CANCEL_COMMANDS = [
    'отмена',
    'cancel'
]

INSTITUTES_PARAMETERS = [
    '?ii=1&fi=1&c=1&',
    '?ii=2&fi=1&c=1&',
    '?ii=3&fi=1&c=1&',
]

TEACHERS_LIST = '?sec=1'
SCHEDULE_URL = 'http://rasp.sgugit.ru/'

SCHEDULE_NUMBERS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

KEYBOARD_BUTTON_CHOOSE_SCHEDULE = 'Выбрать расписание'

MESSAGE_STOP_FLOOD = '📛 Пожалуйста, прекратите флудить.'
MESSAGE_SCHEDULE_NOT_FOUND = '📛 Расписание не найдено, попробуйте позже.'
MESSAGE_CURRENT_DAY_NOT_FOUND = '📛 Расписание на этот день не найдено.'
MESSAGE_CONNECTION_PROBLEM = '📛 Проблема с соединением сайта, попробуйте позже.'
MESSAGE_SOMETHING_WENT_WRONG = '📛 Что-то пошло не так, попробуйте позже.'

MESSAGE_ON_START = '👋 Здравствуйте. Выберите расписание.'

MESSAGE_SELECT_TYPE = '📃 Выберите тип расписания.'
MESSAGE_SELECT_INSTITUTE = '🏛 Выберите ваш институт.'
MESSAGE_SELECT_COURSE = '🔢 Выберите ваш курс.'
MESSAGE_SELECT_FORM_OF_TRAINING = '🎫 Выберите форму обучения.'
MESSAGE_SELECT_GROUP = '🎓 Выберите вашу группу.'
MESSAGE_SELECT_OTHER_SCHEDULE = '🎓 Вы можете выбрать другое расписание.'

MESSAGE_ENTER_TEACHER = '🎓 Введите полное ФИО преподавателя (как на сайте СГУГиТ).'

MESSAGE_TYPE_NOT_FOUND = '📛 Тип расписания не найден. Попробуйте ещё раз.'
MESSAGE_INSTITUTE_NOT_FOUND = '📛 Институт не найден. Попробуйте ещё раз.'
MESSAGE_COURSE_NOT_FOUND = '📛 Курс не найден. Попробуйте ещё раз.'
MESSAGE_FORM_OF_TRAINING_NOT_FOUND = '📛 Форма обучения не найдена. Попробуйте ещё раз.'

MESSAGE_CANCELLED = '❌ Действие отменено.'
