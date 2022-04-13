from bs4 import BeautifulSoup


class TeachersParser:
    def __init__(self, html: str):
        self._teachers = []
        self._parse_teachers(html)

    def get_teachers(self):
        return self._teachers

    def _parse_teachers(self, html: str) -> None:
        soup = BeautifulSoup(html, 'html.parser')
        div_block_alf_block_alfabet_names2 = soup.find_all('div', {'class': 'block_alf block_alfabet_names2'})

        if not len(div_block_alf_block_alfabet_names2):
            return

        for div_block_alf_block_alfabet_name2 in div_block_alf_block_alfabet_names2:
            a_teachers = div_block_alf_block_alfabet_name2.find_all('a')

            if not len(a_teachers):
                continue

            for a_teacher in a_teachers:
                teacher = {
                    'name': ' '.join(a_teacher.text.strip().split()),
                    'url': a_teacher['href']
                }

                self._teachers.append(teacher)
