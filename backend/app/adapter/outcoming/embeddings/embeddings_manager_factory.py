from adapter.outcoming.embeddings.txtai.txtai_embeddings_manager_factory import (
    TxtaiEmbeddingsManagerFactory,
)
from core.port.outcoming.embeddings.embeddings_abstract_factory import (
    EmbeddingsAbstractFactory,
)


class EmbeddingsManagerFactory:
    @staticmethod
    def create(config: dict) -> EmbeddingsAbstractFactory:
        """Creates an instance of an embeddings manager factory based on the configuration.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            EmbeddingsAbstractFactory: An instance of a class implementing the EmbeddingsAbstractFactory interface.

        Raises:
            ValueError: If the embeddings type specified in the configuration is unknown or unsupported.
        """
        manager_type = config.get("embeddings_type")

        if manager_type == "txtai":
            return TxtaiEmbeddingsManagerFactory(config)
        else:
            raise ValueError(f"Unknown embeddings factory type: {manager_type}")
