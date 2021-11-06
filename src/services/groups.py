import json
from typing import Optional, Dict, List


class GroupsService:
    def __init__(self):
        with open('groups.json', encoding='utf-8') as f:
            self.__groups = json.load(f)

    def get_groups(self) -> Optional[Dict[str, Dict[str, List]]]:
        return self.__groups

    def find_group(self, name: str) -> Optional[dict]:
        return next((c for a in self.get_groups().values() for b in a.values() for c in b if c['name'].lower() == name),
                    None)


groups_service = GroupsService()
