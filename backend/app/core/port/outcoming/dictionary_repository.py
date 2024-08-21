from abc import ABC, abstractmethod


class DictionaryRepository(ABC):

    @abstractmethod
    def get_all_dictionaries(self):
        """Retrieve all available dictionaries.

        Returns:
            A list of all dictionaries.
        """
        pass

    @abstractmethod
    def get_dictionary_by_id(self, id: int):
        """Retrieve a specific dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary.

        Returns:
            The dictionary data associated with the given ID.
        """
        pass

    @abstractmethod
    def get_dictionary_by_name(self, name: str):
        """Retrieve a specific dictionary by its name.

        Args:
            name (str): The name of the dictionary.

        Returns:
            The dictionary data associated with the given name.
        """
        pass

    @abstractmethod
    def create_dictionary(self, name: str, description: str):
        """Create a new dictionary with the provided name and description.

        Args:
            name (str): The name of the dictionary to be created.
            description (str): The description of the dictionary.

        Returns:
            The newly created dictionary data.
        """
        pass

    @abstractmethod
    def update_dictionary(self, id: int, name: str, description: str):
        """Update the name and description of an existing dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary to be updated.
            name (str): The updated name of the dictionary.
            description (str): The updated description of the dictionary.

        Returns:
            The updated dictionary data.
        """
        pass

    @abstractmethod
    def delete_dictionary(self, id: int):
        """Delete a dictionary by its ID.

        Args:
            id (int): The unique identifier of the dictionary to be deleted.

        Returns:
            None
        """
        pass
