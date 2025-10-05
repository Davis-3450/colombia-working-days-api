from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, PositiveInt, TypeAdapter

class Request(BaseModel):
    days: PositiveInt | None = None
    hours: PositiveInt | None = None
    date: datetime | None = None


class Error(Enum):
    """Error types"""

    INVALID_PARAMETERS = "InvalidParameters"


class ErrorMessage(Enum):
    """Error messages"""

    INVALID_PARAMETERS = "Invalid parameters"


holyday_list_adapter = TypeAdapter(List[date])