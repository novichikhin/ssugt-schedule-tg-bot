import calendar
import datetime
import time
from typing import Optional

import httpx

from src.config import config
from src.consts import SCHEDULE_NUMBERS, SCHEDULE_URL, MESSAGE_CURRENT_DAY_NOT_FOUND, ChooseType
from src.exceptions import ScheduleNotFound
from src.parse.schedule import ScheduleParser
from src.services.audiences import audiences_service
from src.services.groups import groups_service
from src.services.teachers import teachers_service


class ScheduleService:
    def __init__(self):
        self._cache = {}

    def _set_cache(self, key: str, schedule: dict) -> None:
        self._cache[key] = {
            'expired': time.time() + float(config.CACHE_TIME),
            'schedule': schedule
        }

    def _get_cache(self, key: str) -> Optional[dict]:
        if not self._is_cached(key):
            return

        return self._cache[key]['schedule']

    def _is_cached(self, key: str) -> bool:
        if key not in self._cache:
            return False

        return self._cache[key]['expired'] > time.time()

    def find_schedule(self, key: str) -> tuple[Optional[dict], Optional[ChooseType]]:
        schedule = groups_service.find_group(key)

        if schedule is None:
            schedule = teachers_service.find_teacher(key)
            return (schedule, ChooseType.teacher)
        else:
            return (schedule, ChooseType.student)

    async def get_schedule(self, key: str) -> tuple[str, dict, datetime.date, datetime.date]:
        found_schedule, type = self.find_schedule(key)
        if found_schedule is None:
            raise ScheduleNotFound

        schedule = self._get_cache(found_schedule['name'])

        if schedule is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(SCHEDULE_URL + found_schedule['url'], timeout=None)

            schedule_parser = ScheduleParser(response.text)
            schedule = schedule_parser.get_schedule()

            if not len(schedule['schedule']):
                raise ScheduleNotFound

            self._set_cache(found_schedule['name'], schedule)

        _, max_date = self._parse_date(schedule['schedule'][-1])
        min_date, _ = self._parse_date(schedule['schedule'][0])

        return (found_schedule['name'], schedule, min_date, max_date)

    def filter_schedule(self, key: str, schedule: dict, date: datetime.date) -> Optional[str]:

        found_schedule, type = self.find_schedule(key)
        if found_schedule is None:
            return

        formated_schedule = f"{'🎓' if type == ChooseType.student else '👨‍🎓'} {found_schedule['name']}\n\n"
        formated_schedule += self._format_schedule(type, date, self._find_schedule(schedule, date))
        return formated_schedule

    def _find_schedule(self, schedule: dict, date: datetime.date) -> Optional[dict]:
        for curr_schedule in schedule['schedule']:
            min_date, max_date = self._parse_date(curr_schedule)

            if not (min_date <= date and date <= max_date):
                continue

            for week_schedule in curr_schedule['weekly_schedule']:
                if week_schedule['date'] == date.strftime('%d.%m'):
                    return week_schedule

    def _parse_date(self, schedule: dict) -> tuple[datetime.date, datetime.date]:
        min_date, max_date = schedule['date'].split(' - ')
        return datetime.datetime.strptime(min_date, '%d.%m.%y').date(), datetime.datetime.strptime(max_date,
                                                                                                   '%d.%m.%y').date()

    def parse_key(self, schedule: str) -> str:
        return schedule.split('\n')[0].replace('👨‍🎓', '').replace('🎓', '').strip().lower()  # :(

    def _format_schedule(self, type: ChooseType, date: datetime.date, week_schedule: dict) -> str:
        message = f"🔸 {calendar.day_name[date.weekday()]} ({date.strftime('%d.%m.%y')})\n\n"

        if week_schedule is None:
            return message + MESSAGE_CURRENT_DAY_NOT_FOUND

        for index, schedule_day in enumerate(week_schedule['schedule_for_day']):
            if not schedule_day:
                message += f"{SCHEDULE_NUMBERS[index]} —\n"
                continue

            try:
                auditorium = next(
                    (key for key, value in audiences_service.get_audiences().items() if
                     int(schedule_day['auditorium']) in value),
                    '')

                if auditorium:
                    auditorium = ' - ' + auditorium
            except ValueError:
                auditorium = ''

            message += f"{SCHEDULE_NUMBERS[index]} {schedule_day['name']} ({schedule_day['start']} - {schedule_day['end']})\n "
            message += f"{'🎓' if type == ChooseType.teacher else '👨‍🎓'} {schedule_day['name_teacher']} (ауд. {schedule_day['auditorium']}{auditorium}; {schedule_day['type']})\n"

        return message.rstrip('\n')


schedule_service = ScheduleService()
