from bs4 import BeautifulSoup


class ScheduleParser:
    def __init__(self, html: str):
        self._schedule = {
            'group': '',
            'schedule': []
        }

        self._parse_schedule(html)

    def get_schedule(self):
        return self._schedule

    def _parse_schedule(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        div_general_title_page_no_print = soup.find('div', {'class': 'general_title_page no-print'})

        if div_general_title_page_no_print is None:
            return

        # print(f"{div_general_title_page_no_print.text}\n\n\n")
        self._schedule['group'] = div_general_title_page_no_print.text.strip()
        ul_bxslider = soup.find('ul', {'class': 'bxslider'})
        li_date_weeks = ul_bxslider.find_all('li', {'class': 'date_week'})

        for li_date_week in li_date_weeks:
            weekly_schedule = {
                'date': li_date_week['data-date'],
                'weekly_schedule': []
            }
            div_one_days = li_date_week.find_all('div', {'class': 'one-day'})

            for div_one_day in div_one_days:
                div_ever_d = div_one_day.find('div', {'class': 'everD'})
                div_day = div_one_day.find('div', {'class': 'day'})

                # print(div_ever_d.text, div_day.text)

                if (div_ever_d is None) or (div_day is None):
                    continue

                schedule_for_day = {
                    'day': div_day.text.strip(),
                    'date': div_ever_d.text.strip(),
                    'schedule_for_day': []
                }

                div_for_lesson_every_day = div_one_day.find('div', {'class': 'for_lesson_every_day'})
                div_one_lessons = div_for_lesson_every_day.find_all('div', {'class': 'one_lesson'})

                for div_one_lesson in div_one_lessons:
                    div_starting_less = div_one_lesson.find('div', {'class': 'starting_less'})
                    div_finished_less = div_one_lesson.find('div', {'class': 'finished_less'})

                    div_lot_lesson_clearfix = div_one_lesson.find('div', {'class': 'lot_lesson clearfix'})

                    div_names_of_less = div_lot_lesson_clearfix.find('div', {'class': 'names_of_less'})
                    a_kabinet_of_less = div_lot_lesson_clearfix.find('a', {'class': 'kabinet_of_less'})
                    a_name_of_teacher = div_lot_lesson_clearfix.find('a', {'class': 'name_of_teacher'})
                    div_type_less = div_lot_lesson_clearfix.find('div', {'class': 'type_less'})

                    if (div_names_of_less is None) or (a_kabinet_of_less is None) or (a_name_of_teacher is None) or (
                            div_type_less is None) \
                            or (div_starting_less is None) or (div_finished_less is None):
                        schedule_for_day['schedule_for_day'].append({})
                        continue

                    lesson_schedule = {
                        'start': div_starting_less.text.strip(),
                        'end': div_finished_less.text.strip(),
                        'name': div_names_of_less.text.strip(),
                        'auditorium': a_kabinet_of_less.text.strip(),
                        'name_teacher': a_name_of_teacher.text.strip(),
                        'type': div_type_less.text.strip()
                    }

                    schedule_for_day['schedule_for_day'].append(lesson_schedule)

                    # print(f"{div_ever_d.text} {div_day.text}\n{div_names_of_less.text} {a_kabinet_of_less.text} {a_name_of_teacher.text} ({div_type_less.text})\n{div_starting_less.text} - {div_finished_less.text}\n\n\n")

                weekly_schedule['weekly_schedule'].append(schedule_for_day)

            self._schedule['schedule'].append(weekly_schedule)
