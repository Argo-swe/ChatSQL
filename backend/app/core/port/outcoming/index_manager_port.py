from abc import ABC, abstractmethod


class IndexManagerPort(ABC):

    @abstractmethod
    def create_or_load_index(self, dictionary_id: int):
        pass

    @abstractmethod
    def create_index(self, dictionary_id: int, save_index=True):
        pass

    @abstractmethod
    def save_index(self, dictionary_id: int):
        pass

    @abstractmethod
    def load_index(self, dictionary_id: int):
        pass

    @abstractmethod
    def delete_index(self, dictionary_id: int):
        pass
