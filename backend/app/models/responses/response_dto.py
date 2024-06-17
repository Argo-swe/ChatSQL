from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ResponseStatusEnum(str, Enum):
    OK = 'OK'
    ERROR = 'ERROR'
    BAD_REQUEST = 'BAD_REQUEST'
    NOT_FOUND = 'NOT_FOUND'

class ResponseDto(BaseModel):
    message: Optional[str] = None
    status: ResponseStatusEnum
