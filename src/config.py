import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    FLOOD_DELAY = os.environ.get('FLOOD_DELAY')
    CACHE_TIME = os.environ.get('CACHE_TIME')
    TG_API_TOKEN = os.environ.get('TG_API_TOKEN')

config = Config()
