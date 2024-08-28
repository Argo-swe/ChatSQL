from txtai.embeddings import Embeddings
from core.port.outcoming.file_repository import FileRepository
from core.port.outcoming.embeddings.index_manager_port import IndexManagerPort
import os
import shutil

_indexes_out_file_base_path = "/opt/chatsql/indexes"
os.makedirs(_indexes_out_file_base_path, exist_ok=True)


class TxtaiIndexManagerAdapter(IndexManagerPort):
    def __init__(
        self,
        file_repository: FileRepository,
        table_path=None,
        column_path=None,
    ):
        print("\nTxtai settings...")
        if table_path is None:
            table_path = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        print(f"table_description_search_model_path: {table_path}")
        if column_path is None:
            column_path = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        print(f"column_description_search_model_path: {column_path}")
        print("\n")

        self._embeddings = Embeddings(
            content=True,
            indexes={
                "table_description": {"path": table_path},
                "column_description": {
                    "path": column_path,
                    "columns": {"text": "column_description"},
                },
            },
        )
        self._file_repository = file_repository
        self._indexes_out_file_base_path = _indexes_out_file_base_path

    def get_embeddings(self):
        return self._embeddings

    def create_or_load_index(self, dictionary_id: int):
        if os.path.exists(self.__index_file_path(dictionary_id)):
            self.load_index(dictionary_id)
            return False
        else:
            self.create_index(dictionary_id)
            return True

    def create_index(self, dictionary_id: int, save_index=True):
        extracted_documents = self._file_repository.extract_index_metadata(
            dictionary_id
        )
        documents = [
            (idx, document, None) for idx, document in enumerate(extracted_documents)
        ]
        self._embeddings.index(documents)
        if save_index:
            self.save_index(dictionary_id)

    def save_index(self, dictionary_id: int):
        self._embeddings.save(self.__index_file_path(dictionary_id))

    def load_index(self, dictionary_id: int):
        self._embeddings.load(self.__index_file_path(dictionary_id))

    def delete_index(self, dictionary_id: int):
        delete_path = self.__index_file_path(dictionary_id)
        if os.path.exists(delete_path):
            shutil.rmtree(delete_path)

    def __index_file_path(self, dictionary_id: int) -> str:
        return f"{self._indexes_out_file_base_path}/index_{dictionary_id}"
