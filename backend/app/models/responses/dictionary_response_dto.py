from typing import Optional, Union

from models.dictionary_dto import DictionaryDto
from models.dictionary_preview_dto import DictionaryPreviewDto
from models.responses.response_dto import ResponseDto


class DictionaryResponseDto(ResponseDto):
    data: Optional[Union[DictionaryDto, DictionaryPreviewDto]] = None
