from typing import Optional
from pydantic import BaseModel

from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto

class DictionaryResponseDto(ResponseDto):
    data: DictionaryDto | None
