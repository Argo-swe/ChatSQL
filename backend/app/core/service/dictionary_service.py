from core.port.outcoming.dictionary_repository import DictionaryRepository
from core.port.incoming.dictionary_use_case import DictionaryUseCase
from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.responses.dictionaries_response_dto import DictionariesResponseDto


class DictionaryService(DictionaryUseCase):

    def __init__(self, dictionary_repository: DictionaryRepository) -> None:
        self._dictionary_repository = dictionary_repository

    def get_dictionary_list(self) -> DictionariesResponseDto:
        dictionaries = self._dictionary_repository.get_all_dictionaries()
        return DictionariesResponseDto(data=dictionaries, status=ResponseStatusEnum.OK)

    def get_dictionary_by_id(self, id: int) -> DictionaryResponseDto:
        pass

    def get_dictionary_file(self, id: int) -> str:
        pass

    def get_dictionary_preview(self, id: int) -> DictionaryResponseDto:
        pass

    def create_dictionary(
        self, dictionary: DictionaryDto, file: str
    ) -> DictionaryResponseDto:
        pass

    def update_dictionary_metadata(
        self, id: int, dictionary: DictionaryDto
    ) -> DictionaryResponseDto:
        pass

    def update_dictionary_file(self, id: int, file: str) -> DictionaryResponseDto:
        pass

    def delete_dictionary(self, id: int) -> ResponseDto:
        pass
