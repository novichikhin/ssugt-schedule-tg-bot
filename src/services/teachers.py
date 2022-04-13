import json
from typing import Optional


class TeachersService:
    def __init__(self):
        with open('teachers.json', encoding='utf-8') as f:
            self._teachers = json.load(f)

    def get_teachers(self):
        return self._teachers

    def find_teacher(self, name: str) -> Optional[dict]:
        return next((a for a in self.get_teachers() if a['name'].lower() == name), None)


teachers_service = TeachersService()
