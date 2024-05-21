class SchemaMultiExtractor:
    def __init__(self, data):
        self.data = data

    #Estrazione di OGNI possibile elemento del dizionario dati
    def extract_all(self):
        documents = []
        #Creo le liste coi dati delle colonne senza descriverle individualmente
        for table in self.data['tables']:
            column_names = [column['name'] for column in table['columns']]
            column_descriptions = [column['description'] for column in table['columns']]
            column_types = [column['type'] for column in table['columns']]
            column_references = [column['references'] for column in table['columns']]

            #Creo un documento con tutti i possibili dati per ogni colonna in visione di una group by table_name nella search
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
    
    #Estrazione della tabella, della sua descrizione e della lista di colonne che possiede
    def extract_table_and_column_list(self):
        documents = []
        for table in self.data['tables']:
            column_names = [column['name'] for column in table['columns']]

            #Qua mi importa solo di avere i dati relativi alle tabelle
            for table in table['columns']:
                doc = {
                    "table_name": table['name'],
                    "table_synonyms": table['table_synonyms'],
                    "table_description": table['description'],
                    "columns": column_names
                }
                documents.append(doc)

        return documents 

    #Estrazione della tabella, della sua descrizione, delle sue colonne e della loro descrizione
    def extract_table_and_columns(self):
        documents = []
        for table in self.data['tables']:
            column_names = [column['name'] for column in table['columns']]
            column_descriptions = [column['description'] for column in table['columns']]

            for column in table['columns']:
                doc = {
                    "table_name": table['name'],
                    "table_synonyms": table['table_synonyms'],
                    "table_description": table['description'],
                    "columns": column_names,
                    "column_descriptions": column_descriptions
                }
                documents.append(doc)

        return documents
    
    #Estrazione per il primo indice (ricerca semantica tramite LLM)
    def extract_first_index(self):
        documents = []
        for table in self.data['tables']:
            for column in table['columns']:
                doc = {
                    "table_name": table['name'],
                    "text": column['description']
                }
                documents.append(doc)

                # Inserimento sinonimi colonna
                if column["column_synonyms"] is not None:
                    str_list = [column_synonym for column_synonym in column["column_synonyms"]]
                    str_list.append(column['description'])
                    doc = {
                        "table_name": table['name'],
                        "text": str_list
                    }
                    documents.append(doc)

        return documents

    #Estrazione del secondo indice per ricerca tramite keyword
    def extract_second_index(self):
        documents = []
        for table in self.data['tables']:
            # Numero di campi della tabella
            column_names = [column['name'] for column in table['columns']]
            fields_number = len(column_names)

            for column in table['columns']:
                doc = {
                    "table_name": table['name'],
                    "table_description": table['description'],
                    "column_name": column['name'],
                    "column_description": column['description'],
                    "column_type": column['type'],
                    # Il campo column_reference andrebbe suddiviso in due sotto-campi per evitare la dipendenza dal formato JSON in fase di generazione del prompt
                    "column_reference": column['references'],
                    "fields_number": fields_number,
                    "text": table['name'],
                }
                documents.append(doc)
                
        return documents