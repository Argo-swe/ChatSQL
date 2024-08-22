from abc import ABC, abstractmethod
from models.dictionary_dto import DictionaryDto
from models.responses.response_dto import ResponseDto
from models.responses.dictionary_response_dto import DictionaryResponseDto
from models.responses.dictionaries_response_dto import DictionariesResponseDto


class DictionaryUseCase(ABC):

    @abstractmethod
    def get_dictionary_list(self) -> DictionariesResponseDto:
        """Retrieve a list of all dictionaries.

        Returns:
            DictionariesResponseDto: A list of available dictionaries.
        """
        pass

    @abstractmethod
    def get_dictionary_by_id(self, id: int) -> DictionaryResponseDto:
        """Retrieve a specific dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary.

        Returns:
            DictionaryResponseDto: The dictionary data associated with the given ID.
        """
        pass

    @abstractmethod
    def get_dictionary_file(self, id: int) -> str:
        """Retrieve the file content of a specific dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary.

        Returns:
            str: The file content of the dictionary.
        """
        pass

    @abstractmethod
    def get_dictionary_preview(self, id: int) -> DictionaryResponseDto:
        """Retrieve a preview of a specific dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary.

        Returns:
            DictionaryResponseDto: A preview of the dictionary data.
        """
        pass

    @abstractmethod
    def create_dictionary(
        self, dictionary: DictionaryDto, file: str
    ) -> DictionaryResponseDto:
        """Create a new dictionary with the provided metadata and file.

        Args:
            dictionary (DictionaryDto): The metadata of the dictionary to be created.
            file (str): The file content to be associated with the dictionary.

        Returns:
            DictionaryResponseDto: The newly created dictionary data.
        """
        pass

    @abstractmethod
    def update_dictionary_metadata(
        self, id: int, dictionary: DictionaryDto
    ) -> DictionaryResponseDto:
        pass

    @abstractmethod
    def update_dictionary_file(self, id: int, file: str) -> DictionaryResponseDto:
        """Update the metadata of an existing dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary to be updated.
            dictionary (DictionaryDto): The updated metadata for the dictionary.

        Returns:
            DictionaryResponseDto: The updated dictionary data.
        """
        pass

    @abstractmethod
    def delete_dictionary(self, id: int) -> ResponseDto:
        """Delete a dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary to be deleted.

        Returns:
            ResponseDto: The response indicating the success of the deletion.
        """
        pass
