from enum import Enum
from typing import List
from zoneinfo import ZoneInfo
import httpx
from datetime import date
from pydantic import TypeAdapter
from models.data import holyday_list_adapter

HOLIDAYS_URL = "https://content.capta.co/Recruitment/WorkingDays.json"
TZ = ZoneInfo("America/Bogota")
class Weekday(int, Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class WorkHour(int, Enum):
    WORK_START = 8
    LUNCH_START = 12
    LUNCH_END = 13
    WORK_END = 17

# Note: this is an oversimplification, only happens on cold boot, I doubt we need amything else...
# TODO: fix, this might run on each import.
holyday_list = holyday_list_adapter.validate_python([])
with httpx.Client() as client:
    r = client.get(HOLIDAYS_URL)
    holyday_list = holyday_list_adapter.validate_python(r.json())