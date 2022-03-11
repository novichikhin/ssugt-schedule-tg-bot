from typing import Optional

from bs4 import BeautifulSoup


def parse_institute_info(soup: BeautifulSoup) -> Optional[tuple]:
    div_general_title_page_no_print = soup.find('div', {'class': 'general_title_page no-print'})

    if div_general_title_page_no_print is None:
        return

    institute, course, _ = div_general_title_page_no_print.text.strip().replace(',', '').split()
    return (institute, course)

def parse_institute_parameters(soup: BeautifulSoup) -> Optional[tuple]:
    div_for_list_inst_selected_clearfix = soup.find('div', {'class': 'for_list_inst_selected clearfix'})

    if div_for_list_inst_selected_clearfix is None:
        return

    divs_for_list_inst_selected_clearfix = div_for_list_inst_selected_clearfix.find_all('div', {
        'class': 'for_list_inst_selected clearfix'})

    if not len(divs_for_list_inst_selected_clearfix):
        return

    form_of_training, course = divs_for_list_inst_selected_clearfix

    return (form_of_training, course)