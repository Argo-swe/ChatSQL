from enum import Enum
from typing import Optional
from fastapi_camelcase import CamelModel


class ResponseStatusEnum(str, Enum):
    """Enumeration representing possible response statuses."""
    OK = "OK"
    ERROR = "ERROR"
    BAD_CREDENTIAL = "BAD_CREDENTIAL"
    BAD_REQUEST = "BAD_REQUEST"
    CONTENT_TOO_LARGE = "CONTENT_TOO_LARGE"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"


class ResponseDto(CamelModel):
    """Base Data Transfer Object for API responses.
    
    Attributes:
        message (Optional[str]): An optional message giving details about the response.
        status (ResponseStatusEnum): The status of the response.
    """
    message: Optional[str] = None
    status: ResponseStatusEnum
