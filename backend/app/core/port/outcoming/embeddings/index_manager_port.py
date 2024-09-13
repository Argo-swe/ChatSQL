from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class IndexManagerPort(ABC, Generic[T]):

    @abstractmethod
    def get_embeddings(self) -> T:
        """Retrieve embeddings used for indexing.

        Returns:
            T: The embeddings data.
        """

    @abstractmethod
    def create_or_load_index(self, dictionary_id: int) -> bool:
        """Create a new index or load an existing one for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            bool:
                - `True` if a new index is created.
                - `False` if an existing index is found and loaded.
        """

    @abstractmethod
    def create_index(self, dictionary_id: int, save_index: bool):
        """Create a new index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.
            save_index (bool, optional): Whether to save the index after creation (default is True).

        Returns:
            None
        """

    @abstractmethod
    def save_index(self, dictionary_id: int):
        """Save the index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            None
        """

    @abstractmethod
    def load_index(self, dictionary_id: int):
        """Load the index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            None
        """

    @abstractmethod
    def delete_index(self, dictionary_id: int):
        """Delete the index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            None
        """
