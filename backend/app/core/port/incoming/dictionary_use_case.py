from abc import ABC, abstractmethod
from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.responses.dictionaries_response_dto import DictionariesResponseDto


class DictionaryUseCase(ABC):

    @abstractmethod
    def get_dictionary_list(self) -> DictionariesResponseDto:
        pass

    @abstractmethod
    def get_dictionary_by_id(self, id: int) -> DictionaryResponseDto:
        pass

    @abstractmethod
    def get_dictionary_file(self, id: int) -> str:
        pass

    @abstractmethod
    def get_dictionary_preview(self, id: int) -> DictionaryResponseDto:
        pass

    @abstractmethod
    def create_dictionary(
        self, dictionary: DictionaryDto, file: str
    ) -> DictionaryResponseDto:
        pass

    @abstractmethod
    def update_dictionary_metadata(
        self, id: int, dictionary: DictionaryDto
    ) -> DictionaryResponseDto:
        pass

    @abstractmethod
    def update_dictionary_file(self, id: int, file: str) -> DictionaryResponseDto:
        pass

    @abstractmethod
    def delete_dictionary(self, id: int) -> ResponseDto:
        pass
