import os
import aiofiles
from models.dictionary_preview_dto import DictionaryPreviewDto
from core.port.outcoming.file_repository import FileRepository
from tools.utils import Utils


class JsonFileAdapter(FileRepository):

    def __init__(self, file_path: str) -> None:
        self._out_file_base_path = file_path
        os.makedirs(self._out_file_base_path, exist_ok=True)

    async def save(self, id: int, file):
        async with aiofiles.open(self._generate_schema_file_name(id), "wb") as out_file:
            await out_file.write(file)

    def load(self, id: int) -> str:
        return self._generate_schema_file_name(id)

    def delete(self, id: int):
        if os.path.exists(self._generate_schema_file_name(id)):
            os.remove(self._generate_schema_file_name(id))

    def get_preview(self, id: int) -> DictionaryPreviewDto:
        dictionary_preview = {}
        schema = Utils.read_json_file_content(self._generate_schema_file_name(id))
        if schema is None:
            return DictionaryPreviewDto()
        dictionary_preview["database_name"] = schema["database_name"]
        dictionary_preview["database_description"] = schema["database_description"]
        tables = []
        for table in schema["tables"]:
            temp = {"name": table["name"], "description": table["description"]}
            tables.append(temp)
        dictionary_preview["tables"] = tables
        return DictionaryPreviewDto(dictionary_preview)

    def _generate_schema_file_name(self, id: int) -> str:
        return f"{self._out_file_base_path}/dic_schema_{id}.json"
