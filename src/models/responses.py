from pydantic import BaseModel
from datetime import datetime
from .data import Error, ErrorMessage


class InvalidResponse(BaseModel):
    """
    Response model for invalid response
    """
    error: Error = Error.INVALID_PARAMETERS
    message: ErrorMessage = ErrorMessage.INVALID_PARAMETERS


# rsponse "date": "2025-08-01T14:00:00Z" (clave obligatoria "date", valor en UTC ISO 8601 con Z, sin campos extra).
class Response(BaseModel):
    """
    Response model for valid response
    """
    date: datetime
