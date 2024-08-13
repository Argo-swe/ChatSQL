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

    def extract_schema_metadata(self, id: int, tuples: list) -> str:
        schema = self.get_json_schema(id)
        dyn_string = (
            "Suggested prompt:\n"
            "In table schema the character ':' separates the column name from its type\n"
            "Foreign keys have the following schema: table name (column name) references table name (column name)\n\n"
        )
        dyn_ref_string = "FOREIGN KEYS:\n"
        for table in tuples:
            table_schema = schema["tables"][table["table_pos"]]
            dyn_key_string = (
                f'PRIMARY KEY: ({", ".join(table_schema["primary_key"])})\n'
            )
            dyn_desc_string = (
                f'Table description: {table_schema["description"]}\n'
                "The table contains the following columns:\n"
            )
            column_def = [
                f'{column["name"]}: {column["type"]}'
                for column in table_schema["columns"]
            ]
            dyn_desc_string += "\n".join(
                f'{column["name"]}: {column["description"]}'
                for column in table_schema["columns"]
            )
            dyn_string += (
                f'Table schema: {table_schema["name"]} ({", ".join(column_def)})\n'
            )
            dyn_string += dyn_key_string
            dyn_string += dyn_desc_string + "\n"
            if "foreign_keys" in table_schema:
                for foreign_key in table_schema["foreign_keys"]:
                    dyn_ref_string += (
                        f'FOREIGN KEY {table_schema["name"]} ('
                        f'{", ".join(foreign_key["foreign_key_column_names"])}) references '
                        f'{foreign_key["reference_table_name"]} ('
                        f'{", ".join(foreign_key["reference_column_names"])})\n'
                    )
        dyn_string += dyn_ref_string + "\n"
        return dyn_string

    def get_json_schema(self, id: int):
        return Utils.read_json_file_content(self._generate_schema_file_name(id))

    def _generate_schema_file_name(self, id: int) -> str:
        return f"{self._out_file_base_path}/dic_schema_{id}.json"
