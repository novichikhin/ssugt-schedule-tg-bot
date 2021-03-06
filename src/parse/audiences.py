from collections import defaultdict
from bs4 import BeautifulSoup


class AudiencesParser:
    def __init__(self, html: str):
        self._audiences = defaultdict(list)
        self._parse_audiences(html)

    def get_audiences(self):
        return self._audiences

    def _parse_audiences(self, html: str) -> None:
        soup = BeautifulSoup(html, 'html.parser')
        div_block_alf_block_alfabet_names2 = soup.find_all('div', {'class': 'block_alf block_alfabet_names2'})

        if div_block_alf_block_alfabet_names2 is None:
            return

        for div_block_alf_block_alfabet_name2 in div_block_alf_block_alfabet_names2:
            div_letter_alfabet = div_block_alf_block_alfabet_name2.find('div', {'class': 'letter_alfabet'})
            a_numbers = div_block_alf_block_alfabet_name2.find_all('a')
            for a_number in a_numbers:
                self._audiences[div_letter_alfabet.text.strip()].append(int(a_number.text.strip()))
