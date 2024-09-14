from typing import Optional, Union

from models.dictionary_dto import DictionaryDto
from models.dictionary_preview_dto import DictionaryPreviewDto
from models.responses.response_dto import ResponseDto


class DictionaryResponseDto(ResponseDto):
    """Data Transfer Object for responses related to a single dictionary.

    Attributes:
        data (Optional[Union[DictionaryDto, DictionaryPreviewDto]]): Information or preview of a dictionary (if present).
    """

    data: Optional[Union[DictionaryDto, DictionaryPreviewDto]] = None
