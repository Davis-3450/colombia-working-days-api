from typing import List
from zoneinfo import ZoneInfo
import httpx
from datetime import date
from pydantic import TypeAdapter

HOLIDAYS_URL = "https://content.capta.co/Recruitment/WorkingDays.json"
TZ = ZoneInfo("America/Bogota")
WORK_HOUR_START = 8
WORK_HOUR_END = 17
LUNCH_HOUR_START = 12
LUNCH_HOUR_END = 13

holyday_list_adapter: TypeAdapter[List[date]] = TypeAdapter(List[date])

# Note: this is an oversimplification, only happens on cold boot, I doubt we need amything else...
# TODO: fix, this might run on each import.
holyday_list = holyday_list_adapter.validate_python([])
with httpx.Client() as client:
    r = client.get(HOLIDAYS_URL)
    holyday_list = holyday_list_adapter.validate_python(r.json())