import time
from collections import defaultdict

from src.config import config


class UserService:
    def __init__(self):
        self._anti_flood = 0
        self.group = {
            'messages': defaultdict(dict),
            'in_proccesing': False
        }

    def is_flood(self) -> bool:
        return self._anti_flood > time.time()

    def add_flood_delay(self) -> None:
        self._anti_flood = time.time() + int(config.FLOOD_DELAY)


user_service = defaultdict(UserService)
