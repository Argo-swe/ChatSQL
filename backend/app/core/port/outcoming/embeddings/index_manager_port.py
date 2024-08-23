from abc import ABC, abstractmethod


class IndexManagerPort(ABC):

    @abstractmethod
    def get_embeddings(self):
        """Retrieve embeddings used for indexing.

        Returns:
            Any: The embeddings data.
        """

    @abstractmethod
    def create_or_load_index(self, dictionary_id: int):
        """Create a new index or load an existing one for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            Any: The index data.
        """

    @abstractmethod
    def create_index(self, dictionary_id: int, save_index: bool = True):
        """Create a new index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.
            save_index (bool, optional): Whether to save the index after creation (default is True).

        Returns:
            Any: The created index data.
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
            Any: The loaded index data.
        """

    @abstractmethod
    def delete_index(self, dictionary_id: int):
        """Delete the index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            None
        """
