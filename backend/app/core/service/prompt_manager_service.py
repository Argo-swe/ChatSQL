from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort
from core.service.dictionary_service import DictionaryService
from models.prompt_dto import PromptDto
from models.responses.prompt_response_dto import PromptResponseDto
from models.responses.string_data_response_dto import StringDataResponseDto
from core.port.incoming.prompt_use_case import PromptUseCase
from models.responses.response_dto import ResponseDto, ResponseStatusEnum


class PromptManagerService(PromptUseCase):

    def __init__(
        self, dictionary_service: DictionaryService, prompt_manager: PromptManagerPort
    ) -> None:
        self._dictionary_service = dictionary_service
        self._prompt_manager = prompt_manager

    def generate_prompt(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> StringDataResponseDto:
        found_dic_response = self._dictionary_service.get_dictionary_by_id(
            dictionary_id
        )

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        if query is None or query == "":
            return StringDataResponseDto(
                message="Query cannot be empty", status=ResponseStatusEnum.BAD_REQUEST
            )

        prompt, _ = self.__generate_prompt(dictionary_id, query, language, dbms, False)

        return StringDataResponseDto(data=prompt, status=ResponseStatusEnum.OK)

    def generate_prompt_with_debug(
        self, dictionary_id: int, query: str, dbms: str, language: str
    ) -> PromptResponseDto:
        found_dic_response = self._dictionary_service.get_dictionary_by_id(
            dictionary_id
        )

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        if query is None or query == "":
            return ResponseDto(
                message="Query cannot be empty", status=ResponseStatusEnum.BAD_REQUEST
            )

        prompt, log_content = self.__generate_prompt(
            dictionary_id, query, language, dbms, True
        )
        prompt_dto = PromptDto(prompt=prompt, debug=log_content)

        return PromptResponseDto(data=prompt_dto, status=ResponseStatusEnum.OK)

    def __generate_prompt(
        self, dictionary_id: int, query: str, dbms: str, language: str, log: bool
    ) -> tuple[str, str | None]:
        prompt, log_content = self._prompt_manager.prompt_generator(
            dictionary_id, query, language, dbms, activate_log=log
        )  # type: ignore
        return prompt, log_content
