from abc import ABC, abstractmethod
from models.dictionary_preview_dto import DictionaryPreviewDto


class FileRepository(ABC):

    @abstractmethod
    def save(self, id: int, file):
        """Save a file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.
            file (Any): The file content to be saved.

        Returns:
            None
        """
        pass

    @abstractmethod
    def load(self, id: int) -> str:
        """Load and return the file content associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.

        Returns:
            str: The content of the file.
        """
        pass

    @abstractmethod
    def delete(self, id: int):
        """Delete the file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file to be deleted.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get_preview(self, id: int) -> DictionaryPreviewDto:
        """Retrieve a preview of the dictionary associated with a specific ID.

        Args:
            id (int): The unique identifier for the dictionary.

        Returns:
            DictionaryPreviewDto: The preview data of the dictionary.
        """
        pass

    @abstractmethod
    def get_json_schema(self, id: int):
        """Retrieve the JSON schema associated with a specific ID.

        Args:
            id (int): The unique identifier for the schema.

        Returns:
            dict: The JSON schema.
        """
        pass

    @abstractmethod
    def extract_index_metadata(self, id: int) -> list:
        """Extract metadata for indexing from the file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.

        Returns:
            list: The extracted index metadata.
        """
        pass

    @abstractmethod
    def extract_schema_metadata(self, id: int, tuples: list) -> str:
        """Extract schema metadata from the file associated with a specific ID.

        Args:
            id (int): The unique identifier for the file.
            tuples (list): A list of tuples used for metadata extraction.

        Returns:
            str: The extracted schema metadata as a string.
        """
        pass
