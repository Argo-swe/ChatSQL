from adapter.outcoming.file.json_file_adapter import JsonFileAdapter
from core.port.outcoming.file_repository import FileRepository


class FileFactory:
    @staticmethod
    def create(config: dict) -> FileRepository:
        """Creates an instance of a file repository adapter based on the configuration.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            FileRepository: An instance of a class implementing the FileRepository interface.

        Raises:
            ValueError: If the file type specified in the configuration is unknown or unsupported.
        """
        manager_type = config.get("file_type")

        if manager_type == "json":
            return JsonFileAdapter()
        else:
            raise ValueError(f"Unknown file type: {manager_type}")
