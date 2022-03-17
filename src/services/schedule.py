import datetime
import time
from typing import Optional

import httpx

from src.config import config
from src.consts import SCHEDULE_NUMBERS, SCHEDULE_URL, MESSAGE_CURRENT_DAY_NOT_FOUND
from src.exceptions import ScheduleNotFound, GroupNotFound
from src.parse.schedule import ScheduleParser
from src.services.audiences import audiences_service
from src.services.groups import groups_service


class ScheduleService:
    def __init__(self):
        self._cache = {}

    def _set_cache(self, group_name: str, schedule: dict) -> None:
        self._cache[group_name] = {
            'expired': time.time() + float(config.CACHE_TIME),
            'schedule': schedule
        }

    def _get_cache(self, group_name: str) -> Optional[dict]:
        if not self._is_cached(group_name):
            return

        return self._cache[group_name]['schedule']

    def _is_cached(self, group_name: str) -> bool:
        if group_name not in self._cache:
            return False

        return self._cache[group_name]['expired'] > time.time()

    async def get_schedule(self, group_name: str, date: datetime.date = datetime.date.today()) -> tuple[
        str, str, datetime.date]:
        group = groups_service.find_group(group_name)
        if group is None:
            raise GroupNotFound

        schedule = self._get_cache(group['name'])

        if schedule is None:
            async with httpx.AsyncClient() as client:
                response = await client.get(SCHEDULE_URL + group['url'], timeout=None)

            schedule_parser = ScheduleParser(response.text)
            schedule = schedule_parser.get_schedule()

            if not len(schedule['schedule']):
                raise ScheduleNotFound

            self._set_cache(group['name'], schedule)

        _, max_date = self._parse_date(schedule['schedule'][-1])
        formated_schedule = f"🎓 {schedule['group']}\n\n"

        formated_schedule += self._format_schedule(self._find_schedule(schedule, date))

        return (group['name'], formated_schedule, max_date)

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

    def _format_schedule(self, week_schedule: dict) -> str:
        if week_schedule is None:
            return MESSAGE_CURRENT_DAY_NOT_FOUND

        message = f"🔸 {week_schedule['day']} ({week_schedule['date']})\n\n"

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
            message += f"👨‍🎓 {schedule_day['name_teacher']} ({schedule_day['auditorium']}{auditorium}; {schedule_day['type']})\n"

        return message


schedule_service = ScheduleService()
