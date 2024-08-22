from abc import ABC, abstractmethod
from models.responses.prompt_response_dto import PromptResponseDto
from models.responses.string_data_response_dto import StringDataResponseDto


class PromptUseCase(ABC):

    @abstractmethod
    def generate_prompt(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> StringDataResponseDto:
        """Generate a prompt based on the given dictionary, query, DBMS, and language.

        Args:
            dictionary_id (int): The unique identifier of the dictionary to be used.
            query (str): The query for which the prompt is to be generated.
            dbms (str): The database management system (DBMS) relevant to the prompt.
            language (str): The language for the prompt.

        Returns:
            StringDataResponseDto: The generated prompt as a string.
        """
        pass

    @abstractmethod
    def generate_prompt_with_debug(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> PromptResponseDto:
        """Generate a prompt along with debug information based on the given dictionary, query, DBMS, and language.

        Args:
            dictionary_id (int): The unique identifier of the dictionary to be used.
            query (str): The query for which the prompt is to be generated.
            dbms (str): The database management system (DBMS) relevant to the prompt.
            language (str): The language for the prompt.

        Returns:
            PromptResponseDto: The generated prompt along with debug information.
        """
        pass
