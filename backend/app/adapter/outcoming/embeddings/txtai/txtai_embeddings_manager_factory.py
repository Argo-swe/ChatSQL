from adapter.outcoming.embeddings.txtai.txtai_index_manager_adapter import (
    TxtaiIndexManagerAdapter,
)
from adapter.outcoming.embeddings.txtai.txtai_prompt_manager_adapter import (
    TxtaiPromptManagerAdapter,
)
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
from core.port.outcoming.embeddings.prompt_manager_port import PromptManagerPort
from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.embeddings.embeddings_abstract_factory import (
    EmbeddingsAbstractFactory,
)


class TxtaiEmbeddingsManagerFactory(EmbeddingsAbstractFactory):

    def __init__(self, config: dict) -> None:
        """Initialize the factory with a configuration.

        Args:
            config (dict): A dictionary containing configuration settings.
        """
        self._config = config

    def create_index_manager(self, file_repository: FileRepository) -> IndexManagerPort:
        if "txtai" in self._config:
            return TxtaiIndexManagerAdapter(
                file_repository,
                self._config["txtai"].get("embeddings_table_path"),
                self._config["txtai"].get("embeddings_columns_path"),
            )
        else:
            return TxtaiIndexManagerAdapter(file_repository)

    def create_prompt_manager_with_dependencies(
        self, index_manager: IndexManagerPort, file_repository: FileRepository
    ) -> PromptManagerPort:
        return TxtaiPromptManagerAdapter(index_manager, file_repository)

    def create_prompt_manager(
        self, file_repository: FileRepository
    ) -> PromptManagerPort:
        index_manager = self.create_index_manager(file_repository)
        return self.create_prompt_manager_with_dependencies(
            index_manager, file_repository
        )
