from typing import Optional, Union
from core.port.incoming.schema_validator_use_case import SchemaValidatorUseCase
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.dictionary_repository import DictionaryRepository
from core.port.incoming.dictionary_use_case import DictionaryUseCase
from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto, ResponseStatusEnum
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.responses.dictionaries_response_dto import DictionariesResponseDto
from tools.exceptions import DictionaryError


class DictionaryService(DictionaryUseCase):
    def __init__(
        self,
        dictionary_repository: DictionaryRepository,
        index_manager: IndexManagerPort,
        file_repository: FileRepository,
        schema_validator: SchemaValidatorUseCase,
    ) -> None:
        """Initialize the DictionaryService with necessary repositories and validators.

        Args:
            dictionary_repository (DictionaryRepository): Repository for accessing and managing dictionary data.
            index_manager (IndexManagerPort): Manager for indexing and retrieving index data.
            file_repository (FileRepository): Repository for file operations.
            schema_validator (SchemaValidatorUseCase): Validator for dictionary schema validation.
        """
        self._dictionary_repository = dictionary_repository
        self._index_manager = index_manager
        self._file_repository = file_repository
        self._schema_validator = schema_validator

    def get_dictionary_list(self) -> DictionariesResponseDto:
        """Retrieve the list of all dictionaries.

        Returns:
            DictionariesResponseDto: A response DTO containing the list of dictionaries and status.
        """
        dictionaries = self._dictionary_repository.get_all_dictionaries()
        return DictionariesResponseDto(data=dictionaries, status=ResponseStatusEnum.OK)

    def get_dictionary_by_id(
        self, id: int
    ) -> Union[DictionaryResponseDto, ResponseDto]:
        """Retrieve a dictionary by its ID.

        Args:
            id (int): The ID of the dictionary to retrieve.

        Returns:
            Union[DictionaryResponseDto, ResponseDto]: A response DTO with the dictionary data or an error message.
        """
        found_dic = self._dictionary_repository.get_dictionary_by_id(id)

        if found_dic is not None:
            return DictionaryResponseDto(data=found_dic, status=ResponseStatusEnum.OK)

        return ResponseDto(
            message=DictionaryError.dictionary_not_found(id),
            status=ResponseStatusEnum.NOT_FOUND,
        )

    def get_dictionary_file_path(self, id: int) -> Optional[str]:
        """Retrieve the file path of a dictionary by its ID.

        Args:
            id (int): The ID of the dictionary.

        Returns:
            Optional[str]: The path of the dictionary file or None if the dictionary is not found or an error occurred.
        """
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return None

        return self._file_repository.get_file_path(id)

    def get_dictionary_preview(self, id: int) -> DictionaryResponseDto:
        """Retrieve a preview of a dictionary by its ID.

        Args:
            id (int): The ID of the dictionary.

        Returns:
            DictionaryResponseDto: A response DTO with the dictionary preview data or an error message.
        """
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        dictionary_preview_dto = self._file_repository.get_preview(id)

        return DictionaryResponseDto(
            data=dictionary_preview_dto, status=ResponseStatusEnum.OK
        )

    async def create_dictionary(
        self, dictionary: DictionaryDto, content: str
    ) -> DictionaryResponseDto:
        """Create a new dictionary and save its file content.

        Args:
            dictionary (DictionaryDto): The dictionary data to create.
            content (str): The content of the dictionary file.

        Returns:
            DictionaryResponseDto: A response DTO with the created dictionary data or an error message.
        """
        if not content:
            return DictionaryResponseDto(
                data=None,
                message=DictionaryError.missing_dictionary_file(),
                status=ResponseStatusEnum.BAD_REQUEST,
            )
        else:
            if not self.__file_size_checker(content):
                return DictionaryResponseDto(
                    data=None,
                    message=DictionaryError.file_too_large(),
                    status=ResponseStatusEnum.CONTENT_TOO_LARGE,
                )

            found_dic = self._dictionary_repository.get_dictionary_by_name(
                dictionary.name
            )

            if found_dic:
                return DictionaryResponseDto(
                    data=None,
                    message=DictionaryError.dictionary_already_exists(dictionary.name),
                    status=ResponseStatusEnum.CONFLICT,
                )

            # Validate dictionary schema
            is_valid = self._schema_validator.validate(content)

            if not is_valid:
                return DictionaryResponseDto(
                    data=None,
                    message=DictionaryError.format_error(),
                    status=ResponseStatusEnum.BAD_REQUEST,
                )

            new_dic = self._dictionary_repository.create_dictionary(
                dictionary.name, dictionary.description
            )

            self._file_repository.save(new_dic.id, content)

            self._index_manager.create_index(new_dic.id)

            return DictionaryResponseDto(data=new_dic, status=ResponseStatusEnum.OK)

    def update_dictionary_metadata(
        self, id: int, dictionary: DictionaryDto
    ) -> DictionaryResponseDto:
        """Update the metadata of an existing dictionary.

        Args:
            id (int): The ID of the dictionary to update.
            dictionary (DictionaryDto): The updated dictionary data.

        Returns:
            DictionaryResponseDto: A response DTO with the updated dictionary data or an error message.
        """
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        dic_with_name = self._dictionary_repository.get_dictionary_by_name(
            dictionary.name
        )
        if dic_with_name is not None and dic_with_name.id != id:
            return DictionaryResponseDto(
                data=None,
                message=DictionaryError.dictionary_already_exists(dictionary.name),
                status=ResponseStatusEnum.CONFLICT,
            )

        new_dic = self._dictionary_repository.update_dictionary(
            id, dictionary.name, dictionary.description
        )

        return DictionaryResponseDto(data=new_dic, status=ResponseStatusEnum.OK)

    async def update_dictionary_file(
        self, id: int, content: str
    ) -> DictionaryResponseDto:
        """Update the file content of an existing dictionary.

        Args:
            id (int): The ID of the dictionary to update.
            content (str): The new content of the dictionary file.

        Returns:
            DictionaryResponseDto: A response DTO with the updated dictionary data or an error message.
        """

        if not self.__file_size_checker(content):
            return DictionaryResponseDto(
                data=None,
                message=DictionaryError.file_too_large(),
                status=ResponseStatusEnum.CONTENT_TOO_LARGE,
            )

        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        # Validate dictionary schema
        is_valid = self._schema_validator.validate(content)

        if not is_valid:
            return DictionaryResponseDto(
                data=None,
                message=DictionaryError.format_error(),
                status=ResponseStatusEnum.BAD_REQUEST,
            )

        self._file_repository.save(id, content)

        self._index_manager.create_index(id)

        return found_dic_response

    def delete_dictionary(self, id: int) -> ResponseDto:
        """Delete a dictionary and its associated file and index.

        Args:
            id (int): The ID of the dictionary to delete.

        Returns:
            ResponseDto: A response DTO indicating the result of the deletion operation.
        """
        found_dic_response = self.get_dictionary_by_id(id)

        if found_dic_response.status is not ResponseStatusEnum.OK:
            return found_dic_response

        self._dictionary_repository.delete_dictionary(id)
        self._file_repository.delete(id)
        self._index_manager.delete_index(id)

        return ResponseDto(status=ResponseStatusEnum.OK)

    def __file_size_checker(self, content: str) -> bool:
        """Check if the size of the given content is within the allowed limit.

        Args:
            content (str): The content to check the size of.

        Returns:
            bool: True if the size of the content is within the allowed limit (1 MB), False otherwise.
        """
        max_size_in_bytes = 1 * 1024 * 1024
        return len(content) <= max_size_in_bytes
