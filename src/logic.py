from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from src.constants import Weekday, WorkHour

from .constants import TZ, holyday_list

# z suffix is optional, fallback to Colombian timezone
# order -> days, hours, date
# minutes, seconds, microseconds are EXCLUDED
# rounding is to the past

# TODO
# [x] fallback to Colombia timezone
# [ ] working day: bot weekday and (not) in holidays
# [ ] if the end date doesn't hit a day, "round" it to either to the previous or to the next working hour (and day) -> aka working date

HOLIDAYS = frozenset(holyday_list)


def set_tz(date: datetime, tz: ZoneInfo) -> datetime:
    if date.tzinfo is None:
        return date.replace(tzinfo=tz)
    return date.astimezone(tz)


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
        return self._date_tz(date)

    def _now(self) -> datetime:
        return datetime.now(self.tz)

    def _date_tz(self, date: datetime):
        return set_tz(date, self.tz)

    # TODO: refactor, this is a mess
    def _round_to_working_datetime(self, start: datetime):
        """Round to working datetime. (down)"""
        local = self._date_tz(start)

        date, hour = local.date(), local.hour

        if date.weekday() >= Weekday.FRIDAY.value or date in self.HOLIDAYS:
            date = date - timedelta(days=1)
            while date.weekday() >= Weekday.FRIDAY.value or date in self.HOLIDAYS:
                date -= timedelta(days=1)
            return datetime(
                date.year,
                date.month,
                date.day,
                WorkHour.WORK_END.value,
                0,
                tzinfo=self.tz,
            )

        if hour < WorkHour.WORK_START.value:
            date = date - timedelta(days=1)
            while date.weekday() >= Weekday.FRIDAY.value or date in self.HOLIDAYS:
                date -= timedelta(days=1)
            return datetime(
                date.year,
                date.month,
                date.day,
                WorkHour.WORK_END.value,
                0,
                tzinfo=self.tz,
            )

        if hour < WorkHour.WORK_START.value:
            return local.replace(hour=WorkHour.WORK_START.value)

        if hour == WorkHour.LUNCH_START.value:
            return local.replace(hour=WorkHour.LUNCH_START.value)

        if hour >= WorkHour.WORK_START.value:
            return local.replace(hour=WorkHour.WORK_START.value)

        return local

    def calculate(self) -> str:
        base = self._round_to_working_datetime(self.date)
        result = base
        return (
            result.astimezone(timezone.utc)
            .replace(microsecond=0)
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )
