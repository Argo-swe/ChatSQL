from abc import ABC, abstractmethod


class SchemaValidatorUseCase(ABC):

    @abstractmethod
    def validate(self, dictionary) -> bool:
        pass
