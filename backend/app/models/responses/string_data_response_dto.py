from models.responses.response_dto import ResponseDto
from typing import Optional


class StringDataResponseDto(ResponseDto):
    """Data Transfer Object for responses that return string data.

    Attributes:
        data (Optional[str]): An optional string representing the response data. 
    """
    data: Optional[str] = None
