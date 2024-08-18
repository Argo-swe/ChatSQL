from abc import ABC, abstractmethod


class DictionaryRepository(ABC):

    @abstractmethod
    def get_all_dictionaries(self):
        pass

    @abstractmethod
    def get_dictionary_by_id(self, id: int):
        pass

    @abstractmethod
    def get_dictionary_by_name(self, name: str):
        pass

    @abstractmethod
    def create_dictionary(self, name: str, description: str):
        pass

    @abstractmethod
    def update_dictionary(self, id: int, name: str, description: str):
        pass

    @abstractmethod
    def delete_dictionary(self, id: int):
        pass
