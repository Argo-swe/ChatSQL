from models.responses.response_dto import ResponseDto
from typing import Optional

class StringDataResponseDto(ResponseDto):
    data: Optional[str] = None
