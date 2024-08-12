import os
import aiofiles
from core.port.outcoming.index_manager_port import IndexManagerPort
from tools.dictionary_validator import DictionaryValidator
from models.dictionary_internal_structure.table_dto import TableDto
from models.dictionary_preview_dto import DictionaryPreviewDto
from core.port.outcoming.dictionary_repository import DictionaryRepository
from core.port.incoming.dictionary_use_case import DictionaryUseCase
from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from tools.schema_multi_extractor import SchemaMultiExtractor
from tools.utils import Utils


class DictionaryService(DictionaryUseCase):

    def __init__(
        self,
        dictionary_repository: DictionaryRepository,
        index_manager: IndexManagerPort,
    ) -> None:
        self._dictionary_repository = dictionary_repository
        self._index_manager = index_manager
        self._out_file_base_path = "/opt/chatsql/dictionary_schemas"
        os.makedirs(self._out_file_base_path, exist_ok=True)

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

        return self.__generate_schema_file_name(id)

    def get_dictionary_preview(self, id: int) -> DictionaryResponseDto:
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        # FIXME: ragionare se ha senso spostare il metodo "extract_preview"
        dictionary_sub_schema = SchemaMultiExtractor.extract_preview(id)

        dictionary_preview_dto = DictionaryPreviewDto(
            database_name=dictionary_sub_schema["database_name"],
            database_description=dictionary_sub_schema["database_description"],
            tables=[TableDto(**table) for table in dictionary_sub_schema["tables"]],
        )

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
            is_valid = DictionaryValidator.validate(Utils.string_to_json(content))

            if not is_valid:
                return DictionaryResponseDto(
                    data=None,
                    message="Dictionary schema is bad formatted",
                    status=ResponseStatusEnum.BAD_REQUEST,
                )

            async with aiofiles.open(
                self.__generate_schema_file_name(new_dic.id), "wb"  # type: ignore
            ) as out_file:
                await out_file.write(content)

            # create txtai index
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
        is_valid = DictionaryValidator.validate(Utils.string_to_json(content))

        if not is_valid:
            return DictionaryResponseDto(
                data=None,
                message="Dictionary schema is bad formatted",
                status=ResponseStatusEnum.BAD_REQUEST,
            )

        async with aiofiles.open(
            self.__generate_schema_file_name(id), "wb"
        ) as out_file:
            await out_file.write(content)

        # update txtai index
        self._index_manager.create_index(id)

        return found_dic_response

    def delete_dictionary(self, id: int) -> ResponseDto:
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        self._dictionary_repository.delete_dictionary(id)

        if os.path.exists(self.__generate_schema_file_name(id)):
            os.remove(self.__generate_schema_file_name(id))

        # delete txtai index
        self._index_manager.delete_index(id)

        return ResponseDto(status=ResponseStatusEnum.OK)

    def __generate_schema_file_name(self, id: int) -> str:
        return f"{self._out_file_base_path}/dic_schema_{id}.json"
