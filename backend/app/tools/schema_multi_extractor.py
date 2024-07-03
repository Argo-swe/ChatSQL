from pathlib import Path
from .utils import Utils

class Schema_Multi_Extractor:
    """
    A class used for dictionary extraction methods
    """
    __dictionary_schema_dir_path = "/opt/chatsql/dictionary_schemas"

    """
    # Ritorna lo schema del dizionario dati
    """
    def get_json_schema(dictionary_id: int):
        file_path = f'{Schema_Multi_Extractor.__dictionary_schema_dir_path}/dic_schema_{dictionary_id}.json'
        schema = Utils.read_json_file_content(file_path)
        return schema

    """
    # Estrazione delle seguenti informazioni:
    # nome del database
    # descrizione del database
    # lista delle tabelle (nome + descrizione)
    """
    def extract_preview(dictionary_id: int):
        dictionary_preview = {}
        schema = Schema_Multi_Extractor.get_json_schema(dictionary_id)
        dictionary_preview["database_name"] = schema['database_name']
        dictionary_preview["database_description"] = schema['database_description']
        tables = []
        
        for table in schema['tables']:
            temp = {
                "name": table['name'],
                "description": table['description']
            }
            tables.append(temp)
        dictionary_preview["tables"] = tables
        return dictionary_preview

    # Estrazione di tutti gli elementi del dizionario dati
    def extract_all(dictionary_id: int):
        documents = []
        schema = Schema_Multi_Extractor.get_json_schema(dictionary_id)
        # Creo le liste con i dati delle colonne senza descriverle individualmente
        for table in schema['tables']:
            column_names = [column['name'] for column in table['columns']]
            column_descriptions = [column['description'] for column in table['columns']]
            column_types = [column['type'] for column in table['columns']]
            column_references = [column['references'] for column in table['columns']]

            # Creo un documento con tutti i dati per ogni colonna in vista di una group by table_name nella search
            for column in table['columns']:
                doc = {
                    "table_name": table['name'],
                    "table_description": table['description'],
                    "column_name": column['name'],
                    "columns": column_names,
                    "column_description": column['description'],
                    "column_descriptions": column_descriptions,
                    "column_type": column['type'],
                    "column_types": column_types,
                    "column_reference": column['references'],
                    "column_references": column_references
                }
                documents.append(doc)
        return documents

    # Estrazione della tabella, della sua descrizione e della lista di colonne che possiede
    def extract_table_and_column_list(dictionary_id: int):
        documents = []
        schema = Schema_Multi_Extractor.get_json_schema(dictionary_id)
        for table in schema['tables']:
            column_names = [column['name'] for column in table['columns']]
            doc = {
                "table_name": table['name'],
                "table_synonyms": table['table_synonyms'],
                "table_description": table['description'],
                "columns": column_names
            }
            documents.append(doc)
        return documents

    # Estrazione della tabella, della sua descrizione, delle sue colonne e della loro descrizione
    def extract_table_and_columns(dictionary_id: int):
        documents = []
        schema = Schema_Multi_Extractor.get_json_schema(dictionary_id)
        for table in schema['tables']:
            column_names = [column['name'] for column in table['columns']]
            column_descriptions = [column['description'] for column in table['columns']]
            doc = {
                "table_name": table['name'],
                "table_synonyms": table['table_synonyms'],
                "table_description": table['description'],
                "columns": column_names,
                "column_descriptions": column_descriptions
            }
            documents.append(doc)
        return documents

    """
    # Estrazione delle seguenti informazioni (formato per LLM):
    # nome della tabella
    # descrizione della tabella
    # posizione della tabella nel dizionario dati
    # descrizione della colonna
    """
    def extract_first_index(dictionary_id: int):
        documents = []
        schema = Schema_Multi_Extractor.get_json_schema(dictionary_id)
        for pos, table in enumerate(schema['tables']):
            for column in table['columns']:
                str_list = table['description'] + ": "
                if column["column_synonyms"] is not None:
                    str_list += ', '.join(column_synonym for column_synonym in column["column_synonyms"])
                doc = {
                    "table_name": table['name'],
                    "text": table["description"],
                    "table_pos": pos,
                    "column_description": column['description']
                }
                documents.append(doc)
        return documents

    # Estrazione per il secondo indice (attualmente non utilizzato)
    def extract_second_index(dictionary_id: int):
        documents = []
        schema = Schema_Multi_Extractor.get_json_schema(dictionary_id)
        for table in schema['tables']:
            # Numero di campi della tabella
            fields_number = len(table['columns'])

            for column in table['columns']:
                doc = {
                    "table_name": table['name'],
                    "table_description": table['description'],
                    "primary_key": ', '.join(table['primary_key']),
                    "column_name": column['name'],
                    "column_description": column['description'],
                    "column_type": column['type'],
                    "fields_number": fields_number,
                    "text": table["name"]
                }
                documents.append(doc)
        return documents
