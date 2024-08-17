from adapter.outcoming.embeddings.txtai.txtai_index_manager_adapter import (
    TxtaiIndexManagerAdapter,
)
from adapter.outcoming.embeddings.txtai.txtai_prompt_manager_adapter import (
    TxtaiPromptManagerAdapter,
)
from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.embeddings.embeddings_abstract_factory import (
    EmbeddingsAbstractFactory,
)


class TxtaiEmbeddingsManagerFactory(EmbeddingsAbstractFactory):

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        if "txtai" not in config:
            raise KeyError("Key 'txtai' not found in dictionary")

    def create_index_manager(
        self, file_repository: FileRepository
    ) -> TxtaiIndexManagerAdapter:
        txtai_config = self._config["txtai"]
        if (
            "embeddings_table_path" in txtai_config
            and "embeddings_columns_path" in txtai_config
        ):
            return TxtaiIndexManagerAdapter(
                file_repository,
                txtai_config["embeddings_table_path"],
                txtai_config["embeddings_columns_path"],
            )
        else:
            raise KeyError(
                "Key 'embeddings_table_path' or 'embeddings_columns_path' not found in dictionary"
            )

    def create_prompt_manager_with_dependencies(
        self, index_manager: TxtaiIndexManagerAdapter, file_repository: FileRepository
    ) -> TxtaiPromptManagerAdapter:
        return TxtaiPromptManagerAdapter(index_manager, file_repository)

    def create_prompt_manager(
        self, file_repository: FileRepository
    ) -> TxtaiPromptManagerAdapter:
        index_manager = self.create_index_manager(file_repository)
        return self.create_prompt_manager_with_dependencies(
            index_manager, file_repository
        )
