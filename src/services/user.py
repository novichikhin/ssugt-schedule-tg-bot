import time
from collections import defaultdict

from src.config import config


class UserService:
    def __init__(self):
        self.anti_flood = 0

    def is_flood(self) -> bool:
        return self.anti_flood > time.time()

    def add_flood_delay(self) -> None:
        self.anti_flood = time.time() + int(config.FLOOD_DELAY)


user_service = defaultdict(UserService)
