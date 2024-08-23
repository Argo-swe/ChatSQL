from abc import ABC, abstractmethod
from typing import List
from models.dictionary_dto import DictionaryDto


class DictionaryRepository(ABC):
    @abstractmethod
    def get_all_dictionaries(self) -> List[DictionaryDto]:
        """Retrieve all available dictionaries.

        Returns:
            List[DictionaryDto]: A list of all dictionaries. Each dictionary is represented by a `DictionaryDto` object.
        """

    @abstractmethod
    def get_dictionary_by_id(self, id: int) -> DictionaryDto:
        """Retrieve a specific dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary.

        Returns:
            DictionaryDto: The dictionary data associated with the given ID.
        """

    @abstractmethod
    def get_dictionary_by_name(self, name: str) -> DictionaryDto:
        """Retrieve a specific dictionary by its name.

        Args:
            name (str): The name of the dictionary.

        Returns:
            DictionaryDto: The dictionary data associated with the given name.
        """

    @abstractmethod
    def create_dictionary(self, name: str, description: str) -> DictionaryDto:
        """Create a new dictionary with the provided name and description.

        Args:
            name (str): The name of the dictionary to be created.
            description (str): The description of the dictionary.

        Returns:
            DictionaryDto: The newly created dictionary data.
        """

    @abstractmethod
    def update_dictionary(self, id: int, name: str, description: str) -> DictionaryDto:
        """Update the name and description of an existing dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary to be updated.
            name (str): The updated name of the dictionary.
            description (str): The updated description of the dictionary.

        Returns:
            DictionaryDto: The updated dictionary data.
        """

    @abstractmethod
    def delete_dictionary(self, id: int):
        """Delete a dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary to be deleted.

        Returns:
            None
        """
