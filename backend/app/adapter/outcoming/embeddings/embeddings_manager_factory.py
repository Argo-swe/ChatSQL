from adapter.outcoming.embeddings.txtai.txtai_embeddings_manager_factory import (
    TxtaiEmbeddingsManagerFactory,
)
from core.port.outcoming.embeddings.embeddings_abstract_factory import (
    EmbeddingsAbstractFactory,
)


class EmbeddingsManagerFactory:
    @staticmethod
    def create(config: dict) -> EmbeddingsAbstractFactory:
        manager_type = config.get("embeddings_type")

        if manager_type == "txtai":
            return TxtaiEmbeddingsManagerFactory(config)
        else:
            raise ValueError(f"Unknown embeddings factory type: {manager_type}")
