from abc import ABC, abstractmethod
from models.responses.prompt_response_dto import PromptResponseDto
from models.responses.string_data_response_dto import StringDataResponseDto


class PromptUseCase(ABC):

    @abstractmethod
    def generate_prompt(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> StringDataResponseDto:
        pass

    @abstractmethod
    def generate_prompt_with_debug(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> PromptResponseDto:
        pass
