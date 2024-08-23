from abc import ABC, abstractmethod


class SchemaValidatorUseCase(ABC):

    @abstractmethod
    def validate(self, dictionary) -> bool:
        """Validate the given dictionary schema.

        Args:
            dictionary (Any): The dictionary schema to be validated.

        Returns:
            bool: True if the schema is valid, False otherwise.
        """
