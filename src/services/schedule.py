from datetime import datetime

from src.consts import SCHEDULE_NUMBERS, SCHEDULE_URL
from src.exceptions import ScheduleNotFound, CurrentWeekNotFound
from src.parse.schedule import ScheduleParser
from src.services.audiences import audiences_service


class ScheduleService:
    def get_schedule(self, html: str) -> str:
        schedule_parser = ScheduleParser(html)
        schedule = schedule_parser.get_schedule()

        if not len(schedule['schedule']):
            raise ScheduleNotFound

        index = datetime.today().weekday() == 6
        curr_week_schedule = schedule['schedule'][index]['weekly_schedule']
        # curr_week_schedule = list(filter(lambda x: len(x['schedule_for_day'])>0, curr_week_schedule))

        if curr_week_schedule is None:
            raise CurrentWeekNotFound

        message = f"🎓 {schedule['group']}\n\n"

        for week_schedule in curr_week_schedule:
            message += f"✅ {week_schedule['day']} ({week_schedule['date']})\n\n"

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

            message += '\n\n'

        message += f"❗ Расписание взято с сайта СГУГиТ — {SCHEDULE_URL}"

        return message


schedule_service = ScheduleService()
