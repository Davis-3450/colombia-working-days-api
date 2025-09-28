from zoneinfo import ZoneInfo

import httpx

HOLIDAYS = "https://content.capta.co/Recruitment/WorkingDays.json"
TZ = ZoneInfo("America/Bogota")
WORK_HOUR_START = 8
WORK_HOUR_END = 17
LUNCH_HOUR_START = 12
LUNCH_HOUR_END = 13

# Note: this is an oversimplification, only happens on cold boot, I doubt we need amything else...
HOLIDAYS_LIST: list = []
with httpx.Client() as client:
    r = client.get(HOLIDAYS)
    HOLIDAYS_LIST = r.json()
