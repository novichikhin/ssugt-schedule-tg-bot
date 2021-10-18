from collections import defaultdict
from bs4 import BeautifulSoup

class GroupsParser:
    def __init__(self):
        self.__groups = defaultdict(lambda: defaultdict(list))

    def add_group(self, html):
        self.__soup = BeautifulSoup(html, 'html.parser')
        self.__parse_html()

    def get_groups(self):
        return self.__groups

    def __parse_html(self):
        div_general_title_page_no_print = self.__soup.find('div', {'class': 'general_title_page no-print'})

        if div_general_title_page_no_print is None:
            return None

        institute, course, _ = div_general_title_page_no_print.text.strip().replace(',','').split()
        
        form_table_filter = self.__soup.find('form', {'class':'table-filter'})

        if form_table_filter is None:
            return None

        a_item_filters_select = form_table_filter.find_all('a', {'class':'item_filter_select'})

        if a_item_filters_select is None:
            return None

        for a_item_filter_select in a_item_filters_select:
            group = {
                'name': a_item_filter_select.text.strip(),
                'url': a_item_filter_select['href']
            }
            self.__groups[institute][course].append(group)