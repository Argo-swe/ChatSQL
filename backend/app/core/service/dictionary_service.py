from core.port.incoming.schema_validator_use_case import SchemaValidatorUseCase
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.dictionary_repository import DictionaryRepository
from core.port.incoming.dictionary_use_case import DictionaryUseCase
from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from tools.utils import Utils


class DictionaryService(DictionaryUseCase):

    def __init__(
        self,
        dictionary_repository: DictionaryRepository,
        index_manager: IndexManagerPort,
        file_repository: FileRepository,
        schema_validator: SchemaValidatorUseCase,
    ) -> None:
        self._dictionary_repository = dictionary_repository
        self._index_manager = index_manager
        self._file_repository = file_repository
        self._schema_validator = schema_validator

    def get_dictionary_list(self) -> DictionariesResponseDto:
        dictionaries = self._dictionary_repository.get_all_dictionaries()
        return DictionariesResponseDto(data=dictionaries, status=ResponseStatusEnum.OK)

    def get_dictionary_by_id(self, id: int) -> DictionaryResponseDto | ResponseDto:
        found_dic = self._dictionary_repository.get_dictionary_by_id(id)

        if found_dic is not None:
            return DictionaryResponseDto(data=found_dic, status=ResponseStatusEnum.OK)

        return ResponseDto(
            message=f"Dictionary with id {id} not found",
            status=ResponseStatusEnum.NOT_FOUND,
        )

    def get_dictionary_file(self, id: int) -> str | None:
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return None

        return self._file_repository.load(id)

    def get_dictionary_preview(self, id: int) -> DictionaryResponseDto:
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        dictionary_preview_dto = self._file_repository.get_preview(id)

        return DictionaryResponseDto(
            data=dictionary_preview_dto, status=ResponseStatusEnum.OK
        )

    async def create_dictionary(
        self, dictionary: DictionaryDto, content
    ) -> DictionaryResponseDto:
        if (
            dictionary.name is not None
            and dictionary.description is not None
            and content
        ):
            found_dic = self._dictionary_repository.get_dictionary_by_name(
                dictionary.name
            )

            if found_dic:
                return DictionaryResponseDto(
                    data=None,
                    message=f"Dictionary with name '{dictionary.name}' already exists",
                    status=ResponseStatusEnum.CONFLICT,
                )

            new_dic = self._dictionary_repository.create_dictionary(
                dictionary.name, dictionary.description
            )

            # validate dictionary schema
            is_valid = self._schema_validator.validate(Utils.string_to_json(content))

            if not is_valid:
                return DictionaryResponseDto(
                    data=None,
                    message="Dictionary schema is bad formatted",
                    status=ResponseStatusEnum.BAD_REQUEST,
                )

            self._file_repository.save(new_dic.id, content)  # type: ignore

            self._index_manager.create_index(new_dic.id)  # type: ignore

            return DictionaryResponseDto(data=new_dic, status=ResponseStatusEnum.OK)

        if not content:
            return DictionaryResponseDto(
                data=None,
                message="Dictionary file is mandatory",
                status=ResponseStatusEnum.BAD_REQUEST,
            )

        return DictionaryResponseDto(
            data=None,
            message="Dictionary name and description are mandatory",
            status=ResponseStatusEnum.BAD_REQUEST,
        )

    def update_dictionary_metadata(
        self, id: int, dictionary: DictionaryDto
    ) -> DictionaryResponseDto:
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        dic_with_name = self._dictionary_repository.get_dictionary_by_name(
            dictionary.name
        )
        if dic_with_name is not None and dic_with_name.id != id:
            return DictionaryResponseDto(
                data=None,
                message=f"Dictionary with name '{dictionary.name}' already exists",
                status=ResponseStatusEnum.CONFLICT,
            )

        new_dic = self._dictionary_repository.update_dictionary(
            id, dictionary.name, dictionary.description
        )

        return DictionaryResponseDto(data=new_dic, status=ResponseStatusEnum.OK)

    async def update_dictionary_file(self, id: int, content) -> DictionaryResponseDto:
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        # validate dictionary schema
        is_valid = self._schema_validator.validate(Utils.string_to_json(content))

        if not is_valid:
            return DictionaryResponseDto(
                data=None,
                message="Dictionary schema is bad formatted",
                status=ResponseStatusEnum.BAD_REQUEST,
            )

        self._file_repository.save(id, content)

        self._index_manager.create_index(id)

        return found_dic_response

    def delete_dictionary(self, id: int) -> ResponseDto:
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        self._dictionary_repository.delete_dictionary(id)
        self._file_repository.delete(id)
        self._index_manager.delete_index(id)

        return ResponseDto(status=ResponseStatusEnum.OK)
