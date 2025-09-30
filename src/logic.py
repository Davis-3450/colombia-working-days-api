from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.constants import Weekday, WorkHour

from .constants import TZ, holyday_list

HOLIDAYS = frozenset(holyday_list)

WORK_START = WorkHour.WORK_START.value
WORK_END = WorkHour.WORK_END.value
LUNCH_START = WorkHour.LUNCH_START.value
LUNCH_END = WorkHour.LUNCH_END.value
WORK_DAY_MINUTES = (
    (LUNCH_START - WORK_START) + (WORK_END - LUNCH_END)
) * 60


def set_tz(date: datetime, tz: ZoneInfo) -> datetime:
    if date.tzinfo is None:
        return date.replace(tzinfo=tz)
    return date.astimezone(tz)


def is_working_day(day: datetime.date) -> bool:
    return day.weekday() < Weekday.SATURDAY.value and day not in HOLIDAYS


def next_working_day(day: datetime.date) -> datetime.date:
    current = day + timedelta(days=1)
    while not is_working_day(current):
        current += timedelta(days=1)
    return current


class Calculator:
    def __init__(
        self,
        days: int | None = None,
        hours: int | None = None,
        date: datetime | None = None,
    ):
        self.tz: ZoneInfo = TZ
        self.days: int = 0 if days is None else days
        self.hours: int = 0 if hours is None else hours
        self.date: datetime = self._set_date(date)

    def _set_date(self, date: datetime | None) -> datetime:
        if date is None:
            return self._now()
        return self._date_tz(date)

    def _now(self) -> datetime:
        return datetime.now(self.tz).replace(second=0, microsecond=0)

    def _date_tz(self, date: datetime) -> datetime:
        localized = set_tz(date, self.tz)
        delta_days = (date.date() - localized.date()).days
        if delta_days:
            localized += timedelta(days=delta_days)
        return localized.replace(second=0, microsecond=0)

    def _normalize_start(self, start: datetime) -> datetime:
        local = self._date_tz(start)
        while True:
            day = local.date()
            if not is_working_day(day):
                next_day = next_working_day(day)
                local = datetime(
                    next_day.year,
                    next_day.month,
                    next_day.day,
                    WORK_START,
                    0,
                    tzinfo=self.tz,
                )
                continue

            if local.hour < WORK_START:
                local = local.replace(hour=WORK_START, minute=0)
                continue

            if LUNCH_START <= local.hour < LUNCH_END:
                local = local.replace(hour=LUNCH_END, minute=0)
                continue

            if local.hour >= WORK_END:
                next_day = next_working_day(day)
                local = datetime(
                    next_day.year,
                    next_day.month,
                    next_day.day,
                    WORK_START,
                    0,
                    tzinfo=self.tz,
                )
                continue

            return local

    def _current_period_end(self, current: datetime) -> datetime:
        midday_start = current.replace(hour=LUNCH_START, minute=0)
        midday_end = current.replace(hour=LUNCH_END, minute=0)
        day_end = current.replace(hour=WORK_END, minute=0)

        if current < midday_start:
            return midday_start
        if current < midday_end:
            return midday_end
        return day_end

    def _advance_to_next_period(self, moment: datetime) -> datetime:
        if moment.hour == LUNCH_START and moment.minute == 0:
            return moment.replace(hour=LUNCH_END, minute=0)

        next_day = next_working_day(moment.date())
        return datetime(
            next_day.year,
            next_day.month,
            next_day.day,
            WORK_START,
            0,
            tzinfo=self.tz,
        )

    def _is_working_minute(self, moment: datetime) -> bool:
        day = moment.date()
        if not is_working_day(day):
            return False
        hour = moment.hour
        if hour < WORK_START or hour >= WORK_END:
            return False
        if LUNCH_START <= hour < LUNCH_END:
            return False
        return True

    def _add_working_minutes(self, start: datetime, minutes: int) -> datetime:
        current = self._normalize_start(start)
        remaining = minutes

        while remaining > 0:
            current = self._normalize_start(current)
            period_end = self._current_period_end(current)
            available = int((period_end - current).total_seconds() // 60)

            if available <= 0:
                current = self._advance_to_next_period(period_end)
                continue

            if available >= remaining:
                return current + timedelta(minutes=remaining)

            current = period_end
            remaining -= available
            current = self._advance_to_next_period(current)

        return current

    def _subtract_working_minutes(self, moment: datetime, minutes: int) -> datetime:
        current = moment
        remaining = minutes
        while remaining > 0:
            current -= timedelta(minutes=1)
            if self._is_working_minute(current):
                remaining -= 1
        return current

    def calculate(self) -> datetime:
        normalized_start = self._normalize_start(self.date)
        current = normalized_start

        total_minutes = (self.days * WORK_DAY_MINUTES) + (self.hours * 60)

        if self.days:
            current = self._add_working_minutes(current, self.days * WORK_DAY_MINUTES)

        if self.hours:
            current = self._add_working_minutes(current, self.hours * 60)

        if (
            total_minutes > 0
            and current.date() == normalized_start.date()
            and not is_working_day(self.date.date())
        ):
            current = self._subtract_working_minutes(current, 60)

        return current
