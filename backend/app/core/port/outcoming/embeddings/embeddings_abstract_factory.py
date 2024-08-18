from abc import ABC, abstractmethod

from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort


class EmbeddingsAbstractFactory(ABC):

    def __init__(self, config: dict) -> None:
        self._config = config

    @abstractmethod
    def create_index_manager(self, file_repository: FileRepository) -> IndexManagerPort:
        pass

    @abstractmethod
    def create_prompt_manager_with_dependencies(
        self, index_manager: IndexManagerPort, file_repository: FileRepository
    ) -> PromptManagerPort:
        pass

    def create_prompt_manager(
        self, file_repository: FileRepository
    ) -> PromptManagerPort:
        index_manager = self.create_index_manager(file_repository)
        return self.create_prompt_manager_with_dependencies(
            index_manager, file_repository
        )
