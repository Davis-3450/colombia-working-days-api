from datetime import datetime, timedelta, date

from pydantic import BaseModel, Field, RootModel, TypeAdapter
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

class ErrorMessage(Enum):
    """
    Error messages
    """
    INVALID_PARAMETERS = "Invalid parameters"


holyday_list_adapter = TypeAdapter(List[date])