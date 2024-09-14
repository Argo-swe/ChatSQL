from abc import ABC, abstractmethod


class SchemaValidatorUseCase(ABC):

    @abstractmethod
    def validate(self, dictionary_content: str) -> bool:
        """Validate the schema of a data dictionary, which can be represented in different formats.

        Args:
            dictionary_content (str): The content of the dictionary as a string.

        Returns:
            bool: True if the schema is valid, False otherwise.
        """
