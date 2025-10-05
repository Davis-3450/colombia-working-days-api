from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.constants import holyday_list
from src.logic import Calculator
from src.models.data import Error, Request
from src.models.responses import Response

UTC = ZoneInfo("UTC")

app = FastAPI()


def _format_utc(moment: datetime) -> str:
    normalized = moment.astimezone(UTC)
    trimmed = normalized.replace(microsecond=0)
    text = trimmed.isoformat()
    return text[:-6] + "Z" if text.endswith("+00:00") else text


def _invalid_parameters() -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": Error.INVALID_PARAMETERS.value})


@app.get("/calculate", response_model=Response)
def calculate(
    days: int | None = Query(default=None),
    hours: int | None = Query(default=None),
    date: str | None = Query(default=None),
) -> Response | JSONResponse:
    try:
        payload = Request(days=days, hours=hours, date=date)
    except ValidationError:
        return _invalid_parameters()

    if payload.days is None and payload.hours is None:
        return _invalid_parameters()

    calculator = Calculator(days=payload.days, hours=payload.hours, date=payload.date)
    result = calculator.calculate()
    return Response(date=_format_utc(result))


@app.get("/holidays")
def get_holidays() -> list[date]:
    return holyday_list
