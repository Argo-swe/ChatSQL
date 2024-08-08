from txtai.embeddings import Embeddings
from tools.schema_multi_extractor import SchemaMultiExtractor
import os
import shutil

indexes_out_file_base_path = "/opt/chatsql/indexes"
os.makedirs(indexes_out_file_base_path, exist_ok=True)


class IndexManager:
    def __init__(self):
        # Modelli per la lingua inglese
        self.embeddings = Embeddings(
            content=True,
            indexes={
                "table_description": {
                    "path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                },
                "column_description": {
                    "path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                    "columns": {"text": "column_description"},
                },
            },
        )
        self.indexes_out_file_base_path = indexes_out_file_base_path

    def create_or_load_index(self, dictionary_id):
        path = f"{self.indexes_out_file_base_path}/index_{dictionary_id}"
        if os.path.exists(path):
            self.load_index(dictionary_id)
            return False
        else:
            self.create_index(dictionary_id)
            return True

    def create_index(self, dictionary_id, save_index=True):
        extracted_documents = SchemaMultiExtractor.extract_first_index(dictionary_id)
        documents = [
            (idx, document, None) for idx, document in enumerate(extracted_documents)
        ]
        self.embeddings.index(documents)
        if save_index:
            self.save_index(dictionary_id)

    def save_index(self, dictionary_id):
        self.embeddings.save(f"{self.indexes_out_file_base_path}/index_{dictionary_id}")

    def load_index(self, dictionary_id):
        self.embeddings.load(f"{self.indexes_out_file_base_path}/index_{dictionary_id}")

    def delete_index(self, dictionary_id):
        delete_path = f"{self.indexes_out_file_base_path}/index_{dictionary_id}"
        if os.path.exists(delete_path):
            shutil.rmtree(delete_path)
