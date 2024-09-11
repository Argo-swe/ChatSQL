from adapter.incoming.schema_validator.json_schema_validator_adapter import (
    JsonSchemaValidatorAdapter,
)
from core.port.incoming.schema_validator_use_case import SchemaValidatorUseCase


class SchemaValidatorFactory:
    @staticmethod
    def create(config: dict) -> SchemaValidatorUseCase:
        """Creates an instance of a schema validator adapter based on the configuration.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            SchemaValidatorUseCase: An instance of a class implementing the SchemaValidatorUseCase interface.

        Raises:
            ValueError: If the validation file type specified in the configuration is unknown or unsupported.
        """
        manager_type = config.get("validation_file_type")

        if manager_type == "json":
            return JsonSchemaValidatorAdapter()
        else:
            raise ValueError(f"Unknown validation file type: {manager_type}")
