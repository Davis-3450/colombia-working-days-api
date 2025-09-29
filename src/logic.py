from datetime import timedelta
from datetime import datetime

from src.models.data import Weekday
from .constants import *

class Calculator:
    def __init__(
        self, days: int | None = None, hours: int | None = None, date: datetime | None = None
    ):
        self.days: int = 0 if days is None else days
        self.hours: int = 0 if hours is None else hours

        # date
        self.date: datetime | None = self._set_date(date)
