from datetime import timedelta
from datetime import datetime

from src.models.data import Weekday
from .constants import *

#z suffix is optional, fallback to Colombian timezone
#order -> days, hours, date

#TODO
# [x] fallback to Colombia timezone


class Calculator:
    def __init__(
        self, days: int | None = None, hours: int | None = None, date: datetime | None = None
    ):
        self.days: int = 0 if days is None else days
        self.hours: int = 0 if hours is None else hours

        # date
        self.date: datetime | None = self._set_date(date)

    def _set_date(self, date: datetime | None) -> datetime | None:
        if date is None:
            return self._now()
        return date

    def _now(self) -> datetime:
        return datetime.now(TZ)
