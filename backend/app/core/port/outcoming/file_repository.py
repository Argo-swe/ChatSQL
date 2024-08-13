from abc import ABC, abstractmethod
from models.dictionary_preview_dto import DictionaryPreviewDto


class FileRepository(ABC):

    @abstractmethod
    def save(self, id: int, file):
        pass

    @abstractmethod
    def load(self, id: int) -> str:
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

    @abstractmethod
    def get_preview(self, id: int) -> DictionaryPreviewDto:
        pass

    @abstractmethod
    def get_json_schema(self, id: int):
        pass

    @abstractmethod
    def extract_index_metadata(self, id: int) -> list:
        pass
