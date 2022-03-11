from collections import defaultdict

from bs4 import BeautifulSoup

from src.parse.utils import parse_institute_info, parse_institute_parameters


class GroupsParser:
    def __init__(self):
        self.__soup = None
        self.__groups = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def add_group(self, html):
        self.__parse_group(html)

    def get_groups(self):
        return self.__groups

    def __parse_group(self, html: str) -> None:
        soup = BeautifulSoup(html, 'html.parser')

        institute_info = parse_institute_info(soup)

        if institute_info is None:
            return

        institute, course = institute_info

        institute_parameters = parse_institute_parameters(soup)

        if institute_parameters is None:
            return

        form_of_training, _ = institute_parameters

        a_form_of_training_active = form_of_training.find('a', {'class': 'active'})

        if a_form_of_training_active is None:
            return

        form_table_filter = soup.find('form', {'class': 'table-filter'})

        if form_table_filter is None:
            return

        a_item_filters_select = form_table_filter.find_all('a', {'class': 'item_filter_select'})

        if a_item_filters_select is None:
            return

        form_of_training_text = a_form_of_training_active.text.strip()

        for a_item_filter_select in a_item_filters_select:
            group = {
                'name': a_item_filter_select.text.strip(),
                'url': a_item_filter_select['href']
            }
            self.__groups[institute][course][form_of_training_text].append(group)
