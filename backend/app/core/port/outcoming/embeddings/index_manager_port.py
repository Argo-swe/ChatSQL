from abc import ABC, abstractmethod


class IndexManagerPort(ABC):

    @abstractmethod
    def get_embeddings(self):
        """Retrieve embeddings used for indexing.

        Returns:
            Any: The embeddings data.
        """
        pass

    @abstractmethod
    def create_or_load_index(self, dictionary_id: int):
        """Create a new index or load an existing one for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            Any: The index data.
        """
        pass

    @abstractmethod
    def create_index(self, dictionary_id: int, save_index: bool = True):
        """Create a new index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.
            save_index (bool, optional): Whether to save the index after creation (default is True).

        Returns:
            Any: The created index data.
        """
        pass

    @abstractmethod
    def save_index(self, dictionary_id: int):
        """Save the index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            None
        """
        pass

    @abstractmethod
    def load_index(self, dictionary_id: int):
        """Load the index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            Any: The loaded index data.
        """
        pass

    @abstractmethod
    def delete_index(self, dictionary_id: int):
        """Delete the index for a specific dictionary.

        Args:
            dictionary_id (int): The unique identifier of the dictionary.

        Returns:
            None
        """
        pass
