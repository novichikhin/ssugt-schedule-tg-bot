import datetime
import time
from collections import defaultdict

from src.config import config


class UserService:
    def __init__(self):
        self._anti_flood = 0
        self._group = {
            'name': '',
            'max_date': None,
            'last_date': None
        }
        self._messages = []

    def get_messages(self) -> list:
        return self._messages

    def add_message(self, message_id: int) -> None:
        self._messages.append(message_id)

    def clear_messages(self) -> None:
        self._messages.clear()

    def set_group(self, data: dict) -> None:
        self._group = data

    def get_group(self) -> dict:
        return self._group

    def is_flood(self) -> bool:
        return self._anti_flood > time.time()

    def add_flood_delay(self) -> None:
        self._anti_flood = time.time() + int(config.FLOOD_DELAY)


user_service = defaultdict(UserService)
