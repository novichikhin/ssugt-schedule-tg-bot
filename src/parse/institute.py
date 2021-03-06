from collections import defaultdict

from bs4 import BeautifulSoup

from src.parse.utils import parse_institute_info, parse_institute_parameters


class InstituteParser:
    def __init__(self):
        self._forms_of_training_params = defaultdict(lambda: defaultdict(str))
        self._courses_params = defaultdict(lambda: defaultdict(list))

    def add_forms_of_training(self, html: str) -> None:
        self._parse_forms_of_training(html)

    def get_forms_of_training(self):
        return self._forms_of_training_params

    def add_courses(self, html: str) -> None:
        self._parse_courses(html)

    def get_courses(self):
        return self._courses_params

    def _parse_forms_of_training(self, html: str) -> None:
        soup = BeautifulSoup(html, 'html.parser')

        institute_info = parse_institute_info(soup)

        if institute_info is None:
            return

        institute, _ = institute_info

        institute_parameters = parse_institute_parameters(soup)

        if institute_parameters is None:
            return

        form_of_training, _ = institute_parameters

        a_forms_of_training = form_of_training.find_all('a')

        if not len(a_forms_of_training):
            return

        for a_form_of_training in a_forms_of_training:
            self._forms_of_training_params[institute][a_form_of_training.text.strip()] = a_form_of_training['href']

    def _parse_courses(self, html: str) -> None:
        soup = BeautifulSoup(html, 'html.parser')

        institute_info = parse_institute_info(soup)

        if institute_info is None:
            return

        institute, _ = institute_info

        institute_parameters = parse_institute_parameters(soup)

        if institute_parameters is None:
            return

        _, course = institute_parameters

        a_courses = course.find_all('a')

        if not len(a_courses):
            return

        for a_course in a_courses:
            self._courses_params[institute][a_course.text.strip()].append(
                a_course['href'])
