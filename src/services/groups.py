import json
from typing import Optional


class GroupsService:
    def __init__(self):
        with open('groups.json', encoding='utf-8') as f:
            self._groups = json.load(f)

    def get_groups(self):
        return self._groups

    def find_group(self, name: str) -> Optional[dict]:
        return next((d for a in self.get_groups().values() for b in a.values() for c in b.values() for d in c if
                     d['name'].lower() == name),
                    None)


groups_service = GroupsService()
