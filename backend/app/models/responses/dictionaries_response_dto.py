from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto


class DictionariesResponseDto(ResponseDto):
    data: list[DictionaryDto] | list[None]
