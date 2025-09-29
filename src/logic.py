from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from src.constants import Weekday, WorkHour

from .constants import TZ, holyday_list

#z suffix is optional, fallback to Colombian timezone
#order -> days, hours, date

#TODO
# [x] fallback to Colombia timezone

def set_tz(date: datetime, tz: ZoneInfo) -> datetime:
    if date.tzinfo is None:
        return date.replace(tzinfo=tz)
    return date.astimezone(tz)


    """
    Date validator class
    """
    def __init__(self, date: datetime):
        self.date = date

    def is_working_day(self) -> bool:
        weekday = self.date.weekday()
        if weekday in (Weekday.SATURDAY.value, Weekday.SUNDAY.value):
            return False
        return self.date.date() not in holyday_list

    def is_working_hour(self) -> bool:
        t = self.date.time()
        morning_ok = time(WorkHour.WORK_START.value) <= t < time(WorkHour.LUNCH_START.value)
        afternoon_ok = time(WorkHour.LUNCH_END.value) <= t < time(WorkHour.WORK_END.value)
        return morning_ok or afternoon_ok

    def is_holiday(self) -> bool:
        return self.date.date() in holyday_list

class Calculator:
    def __init__(
        self,
        days: int | None = None,
        hours: int | None = None,
        date: datetime | None = None,
    ):
        self.days: int = 0 if days is None else days
        self.hours: int = 0 if hours is None else hours

        # date
        self.date: datetime | None = self._set_date(date)
        self.tz = TZ

    def _set_date(self, date: datetime | None) -> datetime | None:
        if date is None:
            return self._now()
        return date

    def _now(self) -> datetime:
        return datetime.now(TZ)

    #TODO
    def calculate(self) -> datetime:

        # cases:
        # date is None -> not provided | order: days, hours
        
        
        return self.date
        
        final_date: datetime | None = None
        days = self.days
        # matches: List[datetime] = []

        for day in range(days):
            if final_date is not None:
                break

            current_date = self.date + timedelta(days=day)

            if not DateValidator(current_date).is_valid():
                continue
            
            current_date = current_date + timedelta(hours=self.hours)
            
            if not DateValidator(current_date).is_valid():
                continue
            
            #sum hours
            hours = self.hours
            for hour in range(self.hours):
                current_date = current_date + timedelta(hours=1)
                if not DateValidator(current_date).is_valid():
                    continue
                
            final_date = current_date
        return self.date #placeholder
