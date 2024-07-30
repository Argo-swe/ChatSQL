from enum import Enum
from typing import Optional
from fastapi_camelcase import CamelModel


class ResponseStatusEnum(str, Enum):
    OK = "OK"
    ERROR = "ERROR"
    BAD_CREDENTIAL = "BAD_CREDENTIAL"
    BAD_REQUEST = "BAD_REQUEST"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"


class ResponseDto(CamelModel):
    message: Optional[str] = None
    status: ResponseStatusEnum
