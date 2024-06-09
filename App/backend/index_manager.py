import sys
from txtai.embeddings import Embeddings
from tools.schema_multi_extractor import Schema_Multi_Extractor
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent

class IndexManager:
    def __init__(self):
        self.embeddings = Embeddings(
            content=True,
            defaults=False,
            indexes={
                "column_description": {
                    "path": "sentence-transformers/all-MiniLM-L12-v2"
                },
                "table_description": {
                    "path": "sentence-transformers/all-MiniLM-L12-v2",
                    "columns": {
                        "text": "table_description"
                    }
                }
            }
        )
        self.path = f"{current_dir}/assets/Indici"
        self.log_name = f"{current_dir}/chatsql_log.txt"

    # Metodo per individuare se l'indice esiste già per un determinato dizionario dati
    def createOrLoadIndex(self, data_dict_name):
        createIDX = True
        path = f"{self.path}/{data_dict_name}"
        if os.path.exists(path):
            createIDX = False
        if createIDX:
            self.createIndex(data_dict_name)
            self.saveIndex(data_dict_name)
            return True
        else:
            self.loadIndex(data_dict_name)
            return False

    # Metodo per la creazione dei due sottoindici
    def createIndex(self, data_dict_name):
        extracted_documents = Schema_Multi_Extractor.extract_first_index(data_dict_name)
        documents = []
        for idx, document in enumerate(extracted_documents):
            documents.append((idx, document, None))
        self.embeddings.index(documents)

    # Metodo per salvare gli indici
    def saveIndex(self, data_dict_name):
        self.embeddings.save(f"{self.path}/{data_dict_name}/idx")
    
    # Metodo per caricare gli indici già salvati
    def loadIndex(self, data_dict_name):
        self.embeddings.load(f"{self.path}/{data_dict_name}/idx")

    # Metodo per eseguire la ricerca semantica (rimosso il "private" per i test di unità)
    def getTuples(self, user_request, activate_log):
        query_limit = 20
        sql_query = f"""
            SELECT table_name, text, table_pos, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE 
            similar(':x', 'column_description') AND
            similar(':x', 'table_description') AND
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
        log = open(self.log_name, "w")
        log.write("Richiesta: " + user_request + "\n\n")
        log.write("Fase 1 - prima estrazione\n")
        log.write("Lista delle tabelle pertinenti:\n")
        for tuple in enumerate(tuples):
            log.write(tuple[1]["table_name"] + ": " + str(tuple[1]["max_score"]) + "\n")
            log.write("Descrizione della colonna più rilevante: " + tuple[1]["text"] + "\n\n")
            
        tokens_importance = self.embeddings.explain(user_request, [tuple["text"] for tuple in tuples])
        log.write("Classifica di importanza dei termini di ciascuna descrizione:\n")
        for token_importance in tokens_importance:
            log.write("Testo: " + token_importance["text"] + "\n")
            for token, score in sorted(token_importance["tokens"], key=lambda x: x[1], reverse=True):
                log.write(token + ": " + str(score) + "\n")
            log.write("\n")
        log.close()
    
    # Metodo per raffinare i risultati della ricerca semantica
    def getRelevantTuples(self, tuples, activate_log):
        if activate_log:
            log = open(self.log_name, "a")
            log.write("\nFase 2 - seconda estrazione\n")
            log.write("Lista delle tabelle rilevanti:\n")
        relevant_tuples = []
        score = 0
        for tuple in enumerate(tuples):
            scoring_distance = score - tuple[1]['max_score']
            if tuple[1]['max_score'] >= 0.45:
                if activate_log:
                    log.write("La tabella " + tuple[1]["table_name"] + " viene mantenuta poiché ha un punteggio sufficientemente alto\n")
                relevant_tuples.append(tuple[1])
                score = tuple[1]['max_score']
            elif scoring_distance <= 0.25:
                if activate_log:
                    log.write("La tabella " + tuple[1]["table_name"] + " viene mantenuta poiché la differenza di punteggio rispetto alla tabella precedente è inferiore a 0.25\n")
                relevant_tuples.append(tuple[1])
                score = tuple[1]['max_score']
            else:
                if activate_log:
                    log.write("Le tabelle rimanenti vengono scartate poiché lo score non è abbastanza alto e la differenza di punteggio rispetto alle tabelle immediatamente precedenti è superiore a 0.25\n")
                break
        if activate_log:
            log.close()
        return relevant_tuples

    # Metodo per leggere il file di log
    def readLogFile(self):
        try:
            with open(self.log_name, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return False
    
    # Metodo per generare il prompt dopo la doppia estrazione
    def promptGenerator(self, data_dict_name, user_request, activate_log):
        tuples = self.getTuples(user_request, activate_log)
        relevant_tuples = self.getRelevantTuples(tuples, activate_log)
        if not relevant_tuples:
            return f'The request "{user_request}" did not produce any relevant results'
        # Costruzione del prompt
        schema = Schema_Multi_Extractor.get_json_schema(data_dict_name)
        # Legenda dei simboli
        dyn_string = (
            "Suggested prompt:\n"
            "In table schema the character ':' separates the column name from its type\n"
            "Foreign keys have the following schema: table name (column name) references table name (column name)\n\n")
        dyn_ref_string = "FOREIGN KEYS:\n"
        for table in relevant_tuples:
            table_schema = schema["tables"][table["table_pos"]]
            dyn_key_string = (
                f'PRIMARY KEY: ({', '.join(table_schema["primary_key"])})\n')
            dyn_desc_string = (
                f'Table description: {table_schema["description"]}\n'
                'The table contains the following columns:\n')
            column_def = []
            for column in table_schema["columns"]:
                column_def.append(column["name"] + ": " + column["type"])
                dyn_desc_string += (
                    f'{column["name"]}: {column["description"]}\n')
            dyn_string += (
                f'Table schema: {table_schema["name"]} ({', '.join(column_def)})\n')
            dyn_string += dyn_key_string
            dyn_string += dyn_desc_string + "\n"
            if "foreign_keys" in table_schema:
                foreign_keys = table_schema["foreign_keys"]
                for foreign_key in foreign_keys:
                    dyn_ref_string += (
                        f'FOREIGN KEY {table_schema["name"]} ('
                        f'{", ".join(foreign_key["foreign_key_column_names"])}) references '
                        f'{foreign_key["reference_table_name"]} ('
                        f'{', '.join(foreign_key["reference_column_names"])})\n')
        dyn_string += dyn_ref_string + "\n"
        dyn_string += f"Answer with the right SQL query for MariaDB: {user_request}"
        return dyn_string

def main():
    # Piccolo script per testare la classe
    manager = IndexManager()
    
    data_dict_name = "orders"

    manager.createIndex(data_dict_name)

    prompt = manager.promptGenerator(data_dict_name, "all information on users who paid for their orders with PayPal", activate_log=True)

    print(prompt)

if __name__ == "__main__":
    main()
