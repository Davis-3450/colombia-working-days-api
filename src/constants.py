from datetime import date, datetime
from enum import Enum
from zoneinfo import ZoneInfo

import httpx

from src.models.data import holyday_list_adapter

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
    for date in r.json():
        date = datetime.strptime(date, "%Y-%m-%d").astimezone(TZ)
        holyday_list.append(date)
    holyday_list = holyday_list_adapter.validate_python(holyday_list)
