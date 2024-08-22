from typing import Optional, Tuple
from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort
from core.service.dictionary_service import DictionaryService
from models.prompt_dto import PromptDto
from models.responses.prompt_response_dto import PromptResponseDto
from models.responses.string_data_response_dto import StringDataResponseDto
from core.port.incoming.prompt_use_case import PromptUseCase
from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from tools.exceptions import PromptError


class PromptManagerService(PromptUseCase):

    def __init__(
        self, dictionary_service: DictionaryService, prompt_manager: PromptManagerPort
    ) -> None:
        """Initialize the PromptManagerService with dictionary and prompt managers.

        Args:
            dictionary_service (DictionaryService): Service for managing dictionaries.
            prompt_manager (PromptManagerPort): Manager for generating prompts.
        """
        self._dictionary_service = dictionary_service
        self._prompt_manager = prompt_manager

    def generate_prompt(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> StringDataResponseDto:
        """Generate a prompt based on the provided query and dictionary ID.

        Args:
            dictionary_id (int): The ID of the dictionary to use.
            query (str): The query to include in the prompt.
            dbms (str): The database management system to consider.
            language (str): The language for the prompt.

        Returns:
            StringDataResponseDto: A response DTO containing the generated prompt or an error message.
                - If the dictionary is not found or the query is empty, returns an error message.
                - Otherwise, returns the generated prompt.
        """
        found_dic_response = self._dictionary_service.get_dictionary_by_id(
            dictionary_id
        )

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        if query is None or query == "":
            return ResponseDto(
                message=PromptError.missing_query(),
                status=ResponseStatusEnum.BAD_REQUEST,
            )

        prompt, _ = self.__generate_prompt(dictionary_id, query, language, dbms, False)

        return StringDataResponseDto(data=prompt, status=ResponseStatusEnum.OK)

    def generate_prompt_with_debug(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> PromptResponseDto:
        """Generate a prompt with debug information.

        Args:
            dictionary_id (int): The ID of the dictionary to use.
            query (str): The query to include in the prompt.
            dbms (str): The database management system to consider.
            language (str): The language for the prompt.

        Returns:
            PromptResponseDto: A response DTO containing the generated prompt and debug information or an error message.
                - If the dictionary is not found or the query is empty, returns an error message.
                - Otherwise, returns the generated prompt along with debug information.
        """
        found_dic_response = self._dictionary_service.get_dictionary_by_id(
            dictionary_id
        )

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        if query is None or query == "":
            return ResponseDto(
                message=PromptError.missing_query(),
                status=ResponseStatusEnum.BAD_REQUEST,
            )

        prompt, log_content = self.__generate_prompt(
            dictionary_id, query, language, dbms, True
        )
        prompt_dto = PromptDto(prompt=prompt, debug=log_content)

        return PromptResponseDto(data=prompt_dto, status=ResponseStatusEnum.OK)

    def __generate_prompt(
        self, dictionary_id: int, query: str, dbms: str, language: str, log: bool
    ) -> Tuple[str, Optional[str]]:
        """Internal method to generate a prompt using the prompt manager.

        Args:
            dictionary_id (int): The ID of the dictionary to use.
            query (str): The query to include in the prompt.
            dbms (str): The database management system to consider.
            language (str): The language for the prompt.
            log (bool): Whether to include debug information.

        Returns:
            Tuple[str, Optional[str]]: A tuple containing the generated prompt and optional debug information.
        """
        prompt, log_content = self._prompt_manager.prompt_generator(
            dictionary_id, query, language, dbms, activate_log=log
        )  # type: ignore
        return prompt, log_content
