import time
import httpx
import logging

from config import Config
from exceptions import ScheduleNotFound, CurrentWeekNotFound
from utils import get_groups_message, find_group, get_schedule_parse
from consts import *