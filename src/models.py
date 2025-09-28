from datetime import datetime, timedelta

from pydantic import BaseModel, Field, RootModel
from typing import List
from enum import Enum

# datetime
# class request(BaseModel):
#     days: int | None = None
#     hours: timedelta | None = None
#     datetime: datetime | None = None


class Error(Enum):
    """
    Error types
    """
    INVALID_PARAMETERS = "InvalidParameters"

class InvalidResponse(BaseModel):
    error: Error = Error.INVALID_PARAMETERS
    message: str = "Error"  # default


# rsponse "date": "2025-08-01T14:00:00Z" (clave obligatoria "date", valor en UTC ISO 8601 con Z, sin campos extra).
class Response(BaseModel):
    date: datetime