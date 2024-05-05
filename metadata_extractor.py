"""
Per lavorare con un database già pronto, ho usato SQLite come motore e chinhook come sample. Per estrarre i dati nel formato
che ci piace, ho fatto in modo di generare automaticamente il JSON strutturato secondo la progettazione iniziale. In realtà non
ci serve particolarmente avendo già il file JSON.
"""

import sqlite3  # Importa la libreria per interagire con database SQLite
import json  # Importa la libreria per manipolare dati JSON

class DatabaseMetadataExtractor:
    # Costruttore della classe che va inizializzata col file
    def __init__(self, db_path):
        self.db_path = db_path

    """Definisco extract_metadata per connettermi al database tramite funzioni di sqlite, estrarre le informazioni che mi interessano
    e metterle in JSON"""
    def extract_metadata(self):
        try:
            # Connessione al database SQLite
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.cursor()  # Creazione di un cursore per eseguire query
                # Query per ottenere i nomi delle tabelle nel database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()  # Recupero dei risultati della query

                # Struttura iniziale dello schema del database
                database_schema = {
                    "database_name": "Chinook",
                    "database_description": "Database sample",
                    "tables": []}

                # Elaborazione di ciascuna tabella
                for table_name in tables:
                    table_name = table_name[0]  # Estrazione del primo elemento che corrisponde al nome della tabella
                    table_info = self._get_table_info(cursor, table_name)  # Ottenimento delle informazioni della tabella
                    database_schema["tables"].append(table_info)  # Aggiunta delle informazioni al dizionario dello schema
                return database_schema  # Ritorno dello schema del database
        except sqlite3.DatabaseError as e:  # Gestione degli errori di connessione
            print(f"An error occurred while connecting to the database: {e}")
            return {}  # Ritorno di un dizionario vuoto in caso di errore

    """Metodo privato ("privato" un po' per finta perché è Python) per ottenere le informazioni dettagliate di una tabella"""
    def _get_table_info(self, cursor, table_name):
        # Esecuzione di PRAGMA, cioè comandi per facilitare le query SQL forniti da SQLite, per ottenere informazioni sulle colonne
        columns = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        foreign_keys = self._get_foreign_keys(cursor, table_name)  # Ottenimento delle chiavi esterne
        indexes = self._get_indexes(cursor, table_name)  # Ottenimento degli indici
        description = self.auto_generate_description(table_name, columns)  # Generazione automatica della descrizione della tabella

        columns_info = []  # Lista per le informazioni delle colonne
        synonyms = []  # Lista per i sinonimi (attualmente non utilizzata)
        for column in columns:
            formatted_column_info = self._format_column_info(column, foreign_keys)  # Formattazione delle informazioni della colonna
            columns_info.append(formatted_column_info)  # Aggiunta delle informazioni formattate alla lista

        # Ritorno del dizionario con tutte le informazioni della tabella
        return {
            "table_name": table_name,
            "synonyms": synonyms,
            "description": description,
            "columns": columns_info,
            "indexes": indexes
        }

    """Metodo privato per ottenere le chiavi esterne di una tabella"""
    def _get_foreign_keys(self, cursor, table_name):
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")  # Esecuzione di PRAGMA per le chiavi esterne
        foreign_keys = {}
        for fk in cursor.fetchall():  # Iterazione sui risultati
            # Creazione di un dizionario per ogni chiave esterna
            foreign_keys[fk[3]] = {"table": fk[2], "to": fk[4]}

        return foreign_keys  # Ritorno del dizionario delle chiavi esterne

    """Metodo privato per ottenere gli indici di una tabella"""
    def _get_indexes(self, cursor, table_name):
        cursor.execute(f"PRAGMA index_list({table_name})")  # Esecuzione di PRAGMA per gli indici
        indexes = []
        for idx in cursor.fetchall():  # Iterazione sui risultati
            # Aggiunta delle informazioni dell'indice alla lista
            index_info = {"name": idx[1], "unique": bool(idx[2])}
            indexes.append(index_info)

        return indexes  # Ritorno della lista degli indici

    """Metodo privato per formattare le informazioni di una colonna"""
    def _format_column_info(self, column, foreign_keys):
        # Determinazione delle proprietà della colonna come nullabilità e chiave primaria
        is_nullable = not column[3]
        is_primary_key = column[5] == 1
        column_name = column[1]
        synonyms = []  # Lista di sinonimi (attualmente non utilizzata)
        foreign_key_info = foreign_keys.get(column_name)  # Ottenimento delle informazioni della chiave esterna
        description = self.generate_column_description(column_name, column[2])  # Generazione della descrizione della colonna

        # Ritorno del dizionario con tutte le informazioni della colonna
        return {
            "column_name": column_name,
            "synonyms": synonyms,
            "description": description,
            "data_type": column[2],
            "primary_key": is_primary_key,
            "foreign_key": foreign_key_info,
            "nullable": is_nullable,
            "default_value": column[4] if column[4] is not None else None,
            "constraints": [
                "NOT NULL" if not is_nullable else "NULL",
                "AUTOINCREMENT" if is_primary_key and column[2].upper() == "INTEGER" else ""
            ]
        }

    """Metodo per generare una descrizione base di una colonna (per ora solo che tipo di dato contiene, 
    ma è da elaborare meglio o rimuovere)"""
    def generate_column_description(self, column_name, data_type):
        return f"The {column_name} column, storing {data_type} data."

    """Metodo per generare automaticamente una descrizione di una tabella basata sulle sue colonne"""
    def auto_generate_description(self, table_name, columns):
        column_descriptions = []
        for col in columns:  # Iterazione sulle colonne
            description = f"{col[1]} ({col[2]})"  # Formattazione della descrizione della colonna
            column_descriptions.append(description)

        #Generazione della descrizione completa della tabella
        description = f"This table, '{table_name}', contains the following columns: {', '.join(column_descriptions)}."
        return description

"""Codice per eseguire il preprocessore se il file è eseguito come script principale"""
if __name__ == "__main__":
    db_path = 'chinook.db'
    extractor = DatabaseMetadataExtractor(db_path)
    database_schema = extractor.extract_metadata()

    # Salvataggio dello schema del database in un file JSON
    with open('database_schema.json', 'w') as f:
        json.dump(database_schema, f, indent=4)
