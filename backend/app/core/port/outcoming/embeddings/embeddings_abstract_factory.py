from abc import ABC, abstractmethod

from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort


class EmbeddingsAbstractFactory(ABC):

    def __init__(self, config: dict) -> None:
        """Initialize the factory with a configuration.

        Args:
            config (dict): A dictionary containing configuration settings.
        """
        self._config = config

    @abstractmethod
    def create_index_manager(self, file_repository: FileRepository) -> IndexManagerPort:
        """Create and return an instance of IndexManagerPort.

        Args:
            file_repository (FileRepository): The repository used for file operations.

        Returns:
            IndexManagerPort: An instance of an index manager.
        """
        pass

    @abstractmethod
    def create_prompt_manager_with_dependencies(
        self, index_manager: IndexManagerPort, file_repository: FileRepository
    ) -> PromptManagerPort:
        """Create and return an instance of PromptManagerPort with its dependencies.

        Args:
            index_manager (IndexManagerPort): The index manager to be used by the prompt manager.
            file_repository (FileRepository): The repository used for file operations.

        Returns:
            PromptManagerPort: An instance of a prompt manager with its dependencies.
        """
        pass

    @abstractmethod
    def create_prompt_manager(
        self, file_repository: FileRepository
    ) -> PromptManagerPort:
        """Create a prompt manager by first creating its dependencies.

        Args:
            file_repository (FileRepository): The repository used for file operations.

        Returns:
            PromptManagerPort: An instance of a prompt manager.
        """
        pass
