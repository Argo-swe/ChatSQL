from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto


class DictionariesResponseDto(ResponseDto):
    """Data Transfer Object for responses that include a list of dictionaries.

    Attributes:
        data (list[DictionaryDto] | list[None]): A list of DictionaryDto representing the dictionaries (if present).
    """
    data: list[DictionaryDto] | list[None]
