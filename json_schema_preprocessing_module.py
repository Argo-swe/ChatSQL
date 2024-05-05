"""
Lo schema del database, in formato JSON, potrebbe non venire compreso da un NLP come il linguaggio naturale.
L'idea dietro questo modulo è ottenere dallo schema le informazioni necessarie da strutturare come testo, in modo che ogni
elemento da trasformare in vettore (detto "documento") sia la descrizione testuale della tabella e delle sue colonne.
Questo è l'esempio del preprocessing della tabella album:
"Table: Table albums described as: Album of music, full of tracks to listen to. Common constraints: NOT NULL Column AlbumId 
(INTEGER) is used for Unique identificative for the album. Specific constraints: AUTOINCREMENT This column is a primary key.
Column Title (NVARCHAR(160)) is used for The title of the album. Specific constraints:  Column ArtistId (INTEGER) is used for
Identificative of the artist who composed the album. Specific constraints:  Foreign key referencing artists on ArtistId."
Quindi è ancora grezzo ma penso sia una buona partenza.
"""

import json  # Importazione del modulo json

class JSONSchemaPreprocessor:
    """Costruttore per inizializzare l'oggetto JSONSchemaPreprocessor"""
    def __init__(self, schema_path):
        # Caricamento dello schema JSON dal percorso fornito
        self.schema = self.load_schema(schema_path)

    """Metodo per caricare uno schema JSON da file"""
    def load_schema(self, path):
        # Apertura del file in modalità lettura
        with open(path, 'r') as file:
            # Caricamento e ritorno dei dati JSON dal file
            return json.load(file)

    """Metodo per il preprocessing dello schema"""
    def preprocess_schema(self):
        # Lista per raccogliere le tabelle formattate
        formatted_tables = []
        # Iterazione su ciascuna tabella nello schema
        for table in self.schema['tables']:
            # Processamento di ciascuna tabella
            formatted_table = self.process_table(table)
            # Aggiunta della tabella processata alla lista
            formatted_tables.append(formatted_table)
        return formatted_tables

    """Metodo per processare una singola tabella"""
    def process_table(self, table):
        # Lista per raccogliere le colonne con vincoli
        columns_with_constraints = []
        # Iterazione su ciascuna colonna nella tabella
        for col in table['columns']:
            # Selezione delle colonne che hanno vincoli
            if 'constraints' in col:
                columns_with_constraints.append(col)
        # Identificazione dei vincoli comuni tra le colonne
        common_constraints = self.identify_common_constraints(columns_with_constraints)

        # Generazione della descrizione della tabella
        table_desc = self.generate_table_description(table, common_constraints)

        # Lista per raccogliere le descrizioni delle colonne
        column_descriptions = []
        # Iterazione su ciascuna colonna della tabella
        for col in table['columns']:
            # Generazione della descrizione per ciascuna colonna
            column_description = self.generate_column_description(col, common_constraints)
            column_descriptions.append(column_description)

        # Combinazione della descrizione della tabella con le descrizioni delle colonne
        return f"{table_desc} {' '.join(column_descriptions)}"

    """Metodo per identificare vincoli comuni tra diverse colonne"""
    def identify_common_constraints(self, columns):
        # Se non ci sono colonne, ritorna un insieme vuoto
        if not columns:
            return set()
        # Imposta vincoli comuni basati sulla prima colonna
        common = set(columns[0]['constraints'])
        # Intersezione dei vincoli tra tutte le colonne
        for column in columns[1:]:
            common.intersection_update(column['constraints'])
        return common

    """Metodo per generare la descrizione di una tabella"""
    def generate_table_description(self, table, common_constraints):
        # Descrizione dei vincoli comuni, se presenti
        constraints_desc = ""
        if common_constraints:
            constraints_desc = "Common constraints: " + ", ".join(common_constraints)

        # Formattazione della descrizione della tabella
        return f"Table {table['table_name']} described as: {table['description']}. {constraints_desc}"

    """Metodo per generare la descrizione di una colonna"""
    def generate_column_description(self, column, common_constraints):
        # Descrizione di base della colonna
        desc = f"Column {column['column_name']} ({column['data_type']}) is used for {column.get('description', 'No description provided')}."
        
        # Gestione dei vincoli specifici della colonna
        individual_constraints = []
        for con in column.get('constraints', []):
            if con not in common_constraints:
                individual_constraints.append(con)

        # Aggiunta dei vincoli specifici alla descrizione
        if individual_constraints:
            desc += " Specific constraints: " + ", ".join(individual_constraints)

        # Gestione della chiave primaria
        if column.get('primary_key', False):
            desc += " This column is a primary key."

        # Gestione delle chiavi esterne
        if 'foreign_key' in column and column['foreign_key']:
            foreign_table = column['foreign_key']['table']
            foreign_column = column['foreign_key']['to']
            desc += f" Foreign key referencing {foreign_table} on {foreign_column}."

        # Gestione del vincolo di non nullabilità
        if not column.get('nullable', True) and "NOT NULL" not in common_constraints:
            desc += " This column is mandatory (cannot be null)."

        return desc


"""Qua scrivo un main che permetta al modulo di essere lanciato in caso si voglia solo testare la generazione dello schema preprocessato"""
if __name__ == "__main__":
    schema_path = 'path_to_your_schema.json'
    preprocessor = JSONSchemaPreprocessor(schema_path)
    processed_schemas = preprocessor.preprocess_schema()
    print(processed_schemas)
