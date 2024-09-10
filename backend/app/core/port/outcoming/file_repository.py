from abc import ABC, abstractmethod
from typing import Union
from models.dictionary_preview_dto import DictionaryPreviewDto


class FileRepository(ABC):

    @abstractmethod
    def save(self, id: int, file: str):
        """Save a file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.
            file (str): The file content to be saved.

        Returns:
            None
        """

    @abstractmethod
    def get_file_path(self, id: int) -> str:
        """Return the path of the file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.

        Returns:
            str: The path of the file.
        """

    @abstractmethod
    def delete(self, id: int):
        """Delete the file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file to be deleted.

        Returns:
            None
        """

    @abstractmethod
    def get_preview(self, id: int) -> Union[DictionaryPreviewDto, None]:
        """Retrieve a preview of the dictionary associated with a specific ID.

        Args:
            id (int): The unique identifier for the dictionary.

        Returns:
            DictionaryPreviewDto: The preview data of the dictionary.
        """

    @abstractmethod
    def extract_index_metadata(self, id: int) -> list:
        """Extract metadata for indexing from the file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.

        Returns:
            list: The extracted index metadata.
        """

    @abstractmethod
    def extract_schema_metadata(self, id: int, tuples: list) -> str:
        """Extract schema metadata from the file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.
            tuples (list): A list of tuples used for metadata extraction.

        Returns:
            str: The extracted schema metadata as a string.
        """
