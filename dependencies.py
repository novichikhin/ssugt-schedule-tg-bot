import time
import httpx
import logging

from config import Config
from exceptions import ScheduleNotFound, CurrentWeekNotFound
from utils import *
from consts import *