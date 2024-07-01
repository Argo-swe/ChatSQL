import sys
from txtai.embeddings import Embeddings
from tools.schema_multi_extractor import Schema_Multi_Extractor
import os
import time
from pathlib import Path
import shutil

current_dir = Path(__file__).resolve().parent
indexesOutFileBasePath = "/opt/chatsql/indexes"
logsOutFileBasePath = "/opt/chatsql/logs"
logsFileOutFileBasePath = f"{logsOutFileBasePath}/chatsql_log.txt"

os.makedirs(indexesOutFileBasePath, exist_ok=True)
os.makedirs(logsOutFileBasePath, exist_ok=True)

class IndexManager:
    def __init__(self):
        # Modelli per la lingua inglese
        self.embeddings = Embeddings(
            content=True,
            indexes={
                "table_description": {
                    "path": "sentence-transformers/all-MiniLM-L12-v2"
                },
                "column_description": {
                    "path": "sentence-transformers/all-MiniLM-L12-v2",
                    "columns": {
                        "text": "column_description"
                    }
                }
            }
        )
        # Modelli per la lingua italiana
        """self.embeddings = Embeddings(
            content=True,
            indexes={
                "table_description": {
                    "path": "efederici/sentence-BERTino"
                },
                "column_description": {
                    "path": "efederici/sentence-BERTino",
                    "columns": {
                        "text": "column_description"
                    }
                }
            }
        )"""

    # Metodo per individuare se l'indice esiste già per un determinato dizionario dati
    def createOrLoadIndex(self, dictionary_id):
        createIDX = True
        path = f"{indexesOutFileBasePath}/index_{dictionary_id}"
        if os.path.exists(path):
            createIDX = False
        if createIDX:
            self.createIndex(dictionary_id)
            return True
        else:
            self.loadIndex(dictionary_id)
            return False

    # Metodo per la creazione dei due sottoindici
    def createIndex(self, dictionary_id, save_index=True):
        extracted_documents = Schema_Multi_Extractor.extract_first_index(dictionary_id)
        documents = []
        for idx, document in enumerate(extracted_documents):
            documents.append((idx, document, None))
        self.embeddings.index(documents)
        if save_index:
            self.saveIndex(dictionary_id)

    # Metodo per salvare l'indice
    def saveIndex(self, dictionary_id):
        self.embeddings.save(f"{indexesOutFileBasePath}/index_{dictionary_id}")

    # Metodo per caricare l'indice già salvato
    def loadIndex(self, dictionary_id):
        self.embeddings.load(f"{indexesOutFileBasePath}/index_{dictionary_id}")

    # Metodo per eliminare l'indice
    def deleteIndex(self, dictionary_id):
        delete_path = f"{indexesOutFileBasePath}/index_{dictionary_id}"
        if os.path.exists(delete_path):
            shutil.rmtree(delete_path)

    # Metodo per eseguire la ricerca semantica (rimosso il "private" per i test di unità)
    def getTuples(self, user_request, activate_log):
        query_limit = 20
        sql_query = f"""
            SELECT table_name, text, table_pos, column_description, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE
            similar(':x', 'table_description') AND
            similar(':x', 'column_description') AND
            score >= 0.2
            GROUP BY table_name
            HAVING max_score >= 0.3 OR avg_score >= 0.28
            ORDER BY max_score DESC
            LIMIT {query_limit}
        """
        tuples = self.embeddings.search(sql_query, limit=query_limit*10, parameters={"x": user_request})
        if activate_log:
            self.semanticSearchLog(user_request, tuples)
        return tuples

    # Metodo per generare i log della ricerca semantica
    def semanticSearchLog(self, user_request, tuples):
        log = self.getLogFile("w")
        if log == False:
            return log
        log.write(f'{self.getDebugHeader()} - Details of the prompt generation process.\n')
        log.write(f'Request: {user_request}\n\n')
        log.write(f'{self.getDebugHeader()} - Phase 1 - first extraction\n')
        log.write("List of relevant tables:\n")
        if not tuples:
            log.write("No relevant tables found.\n")
        log.write("\n")
        for i, tuple in enumerate(tuples):
            log.write(f'Table {i + 1} | {tuple["table_name"]}: {tuple["max_score"]}\n')
            log.write(f'Description of the table: {tuple["text"]}\n')
            log.write("Ranking of the most relevant terms in the description:\n")
            token_importance = self.embeddings.explain(user_request, [tuple["text"]], limit=1)[0]
            for token, score in sorted(token_importance["tokens"], key=lambda x: x[1], reverse=True):
                log.write(token + ": " + str(score) + "\n")
            log.write(f'\nDescription of the most relevant column: {tuple["column_description"]}\n')
            log.write("Ranking of the most relevant terms in the description:\n")
            token_importance = self.embeddings.explain(user_request, [tuple["column_description"]], limit=1)[0]
            for token, score in sorted(token_importance["tokens"], key=lambda x: x[1], reverse=True):
                log.write(token + ": " + str(score) + "\n")
            log.write("\n")
        log.close()
        return True

    # Metodo per raffinare i risultati della ricerca semantica
    def getRelevantTuples(self, tuples, activate_log):
        if activate_log:
            log = self.getLogFile("a")
            if log == False:
                return log
            log.write(f'{self.getDebugHeader()} - Phase 2 - second extraction\n')
            log.write("List of pertinent tables:\n")
        relevant_tuples = []
        score = 0
        if not tuples:
            if activate_log:
                log.write("No tables found.\n\n")
        for tuple in tuples:
            scoring_distance = score - tuple["max_score"]
            if tuple["max_score"] >= 0.45:
                if activate_log:
                    log.write(
                        f'The table {tuple["table_name"]} is kept '
                        "because it has a sufficiently high score.\n")
                relevant_tuples.append(tuple)
                score = tuple["max_score"]
            elif scoring_distance <= 0.25:
                if activate_log:
                    log.write(
                        f'The table {tuple["table_name"]} is kept '
                        "because the score difference with the previous table "
                        "is less than 0.25.\n")
                relevant_tuples.append(tuple)
                score = tuple["max_score"]
            else:
                if activate_log:
                    log.write(
                        "The remaining tables are discarded "
                        "because the score is not high enough "
                        "and the score difference with the previous tables "
                        "is greater than 0.25.\n")
                break
        if activate_log:
            log.close()
        return relevant_tuples

    # Metodo per ottenere l'header del log
    def getDebugHeader(self, level="DEBUG", system="ChatSQL"):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return f'[{timestamp}] [{system}] [{level}]'

    # Metodo per ottenere un oggetto relativo al file di log
    def getLogFile(self, mode):
        try:
            os.makedirs(logsOutFileBasePath, exist_ok=True)
            file = open(logsFileOutFileBasePath, mode)
            return file
        except Exception:
            return False

    # Metodo per leggere il file di log
    def readLogFile(self):
        try:
            with open(logsFileOutFileBasePath, 'r') as file:
                return file.read()
        except Exception:
            return False

    # Metodo per generare il prompt dopo la doppia estrazione
    def promptGenerator(self, dictionary_id, user_request, lang="english", dbms="MariaDB", activate_log=False):
        tuples = self.getTuples(user_request, activate_log)
        relevant_tuples = self.getRelevantTuples(tuples, activate_log)
        if not relevant_tuples:
            return (f"""Sorry, the ChatBOT was unable to find any relevant results for "{user_request}".\n"""
                """We invite you to try again with a different request.""")
        # Costruzione del prompt
        schema = Schema_Multi_Extractor.get_json_schema(dictionary_id)
        # Legenda dei simboli
        dyn_string = (
            "Suggested prompt:\n"
            "In table schema the character ':' separates the column name from its type\n"
            "Foreign keys have the following schema: table name (column name) references table name (column name)\n\n")
        dyn_ref_string = "FOREIGN KEYS:\n"
        for table in relevant_tuples:
            # Estraggo dal file JSON le informazioni sulla tabella
            table_schema = schema["tables"][table["table_pos"]]
            dyn_key_string = f'PRIMARY KEY: ({", ".join(table_schema["primary_key"])})\n'
            dyn_desc_string = (
                f'Table description: {table_schema["description"]}\n'
                "The table contains the following columns:\n")
            column_def = []
            for column in table_schema["columns"]:
                column_def.append(column["name"] + ": " + column["type"])
                dyn_desc_string += f'{column["name"]}: {column["description"]}\n'
            dyn_string += f'Table schema: {table_schema["name"]} ({", ".join(column_def)})\n'
            dyn_string += dyn_key_string
            dyn_string += dyn_desc_string + "\n"
            if "foreign_keys" in table_schema:
                foreign_keys = table_schema["foreign_keys"]
                for foreign_key in foreign_keys:
                    dyn_ref_string += (
                        f'FOREIGN KEY {table_schema["name"]} ('
                        f'{", ".join(foreign_key["foreign_key_column_names"])}) references '
                        f'{foreign_key["reference_table_name"]} ('
                        f'{", ".join(foreign_key["reference_column_names"])})\n')
        dyn_string += dyn_ref_string + "\n"
        dyn_string += f"User request: {user_request}.\n"
        dyn_string += f"Convert user request to a suitable SQL query for {dbms}.\n"
        dyn_string += f"Answer in {lang}."
        return dyn_string

def main():
    # Piccolo script per testare la classe
    """manager = IndexManager()

    index_name = "orders"
    #index_name = "ordini"

    manager.createOrLoadIndex(index_name)

    user_request = "all information about products that belong to an order placed by a user whose first name is alex"

    prompt = manager.promptGenerator(index_name, user_request, activate_log=True)

    print(prompt)"""

if __name__ == "__main__":
    main()
