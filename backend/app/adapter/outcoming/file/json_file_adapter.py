import os
import aiofiles
from models.dictionary_internal_structure.table_dto import TableDto
from models.dictionary_preview_dto import DictionaryPreviewDto
from core.port.outcoming.file_repository import FileRepository
from tools.utils import Utils


class JsonFileAdapter(FileRepository):

    def __init__(self, file_path="/opt/chatsql/dictionary_schemas") -> None:
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
        schema = self.get_json_schema(id)
        if schema is None:
            return DictionaryPreviewDto()
        dictionary_preview["database_name"] = schema["database_name"]
        dictionary_preview["database_description"] = schema["database_description"]
        tables = []
        for table in schema["tables"]:
            temp = {"name": table["name"], "description": table["description"]}
            tables.append(temp)
        dictionary_preview["tables"] = tables
        return DictionaryPreviewDto(
            database_name=dictionary_preview["database_name"],
            database_description=dictionary_preview["database_description"],
            tables=[TableDto(**table) for table in dictionary_preview["tables"]],
        )

    def extract_index_metadata(self, id: int) -> list:
        documents = []
        schema = self.get_json_schema(id)
        for pos, table in enumerate(schema["tables"]):
            for column in table["columns"]:
                doc = {
                    "table_name": table["name"],
                    "text": table["description"],
                    "table_pos": pos,
                    "column_description": column["description"],
                }
                documents.append(doc)
        return documents

    def get_json_schema(self, id: int):
        return Utils.read_json_file_content(self._generate_schema_file_name(id))

    def _generate_schema_file_name(self, id: int) -> str:
        return f"{self._out_file_base_path}/dic_schema_{id}.json"
