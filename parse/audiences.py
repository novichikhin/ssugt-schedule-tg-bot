from collections import defaultdict
from bs4 import BeautifulSoup

class AudiencesParser:
    def __init__(self, html):
        self.__audiences = defaultdict(list)

        self.__soup = BeautifulSoup(html, 'html.parser')
        self.__parse_html()

    def get_audiences(self):
        return self.__audiences

    def __parse_html(self):
        div_block_alf_block_alfabet_names2 = self.__soup.find_all('div', {'class':'block_alf block_alfabet_names2'})

        if div_block_alf_block_alfabet_names2 is None:
            return None
        
        for div_block_alf_block_alfabet_name2 in div_block_alf_block_alfabet_names2:
            div_letter_alfabet = div_block_alf_block_alfabet_name2.find('div', {'class':'letter_alfabet'})
            a_numbers = div_block_alf_block_alfabet_name2.find_all('a')
            for a_number in a_numbers:
                self.__audiences[div_letter_alfabet.text.strip()].append(int(a_number.text.strip()))