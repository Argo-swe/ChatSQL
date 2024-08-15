from adapter.outcoming.file.json_file_adapter import JsonFileAdapter
from core.port.outcoming.file_repository import FileRepository


class FileFactory:
    @staticmethod
    def create(config: dict) -> FileRepository:
        manager_type = config.get("file_type")

        if manager_type == "json":
            return JsonFileAdapter()
        else:
            raise ValueError(f"Unknown file type: {manager_type}")
