import sys
from txtai.embeddings import Embeddings
from tools.schema_multi_extractor import Schema_Multi_Extractor
import os
import json

class IndexManager:
    def __init__(self):
        self.embeddings = Embeddings(
            content=True,
            defaults=False,
            indexes={
                "column_description": {
                    "path": "sentence-transformers/all-MiniLM-L12-v2"
                },
                "column_description_multilingual": {
                    "path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                },
                "table_description_with_column_name_and_synonyms": {
                    "path": "sentence-transformers/all-MiniLM-L12-v2",
                    "columns": {
                        "text": "relevant_information"
                    }
                }
            }
        )
        self.embeddings_complete = Embeddings(content=True, defaults=False)
        self.path = "../Indici"
        self.log_name = "chatsql_log.txt"

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

        extracted_documents = Schema_Multi_Extractor.extract_second_index(data_dict_name)
        documents = []
        for idx, document in enumerate(extracted_documents):
            documents.append((idx, document, None))
        self.embeddings_complete.index(documents)

    # Metodo per salvare gli indici
    def saveIndex(self, data_dict_name):
        self.embeddings.save(f"{self.path}/{data_dict_name}/idx")
        self.embeddings_complete.save(f"{self.path}/{data_dict_name}/idx_complete")
    
    # Metodo per caricare gli indici già salvati
    def loadIndex(self, data_dict_name):
        self.embeddings.load(f"{self.path}/{data_dict_name}/idx")
        self.embeddings_complete.load(f"{self.path}/{data_dict_name}/idx_complete")

    # Metodo per eseguire la ricerca semantica (rimosso il "private" per i test di unità)
    def getTuples(self, user_request, activate_log):
        query_limit = 20
        sql_query = f"""
            SELECT table_name, text, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE 
            similar(':x', 'column_description') and
            similar(':x', 'column_description_multilingual') and
            score >= 0.2
            GROUP BY table_name
            HAVING avg_score >= 0.25
            ORDER BY max_score DESC
            LIMIT {query_limit}
        """
        # Da aggiungere questa condizione
        #similar(':x', 'table_description_with_column_name_and_synonyms') and
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
                relevant_tuples.append(tuple[1]['table_name'])
                score = tuple[1]['max_score']
            elif scoring_distance <= 0.25:
                if activate_log:
                    log.write("La tabella " + tuple[1]["table_name"] + " viene mantenuta poiché la differenza di punteggio rispetto alla tabella precedente è inferiore a 0.25\n")
                relevant_tuples.append(tuple[1]['table_name'])
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
        log = open(self.log_name, "r")
        return log.read()
    
    # Metodo per generare il prompt dopo la doppia estrazione
    def promptGenerator(self, user_request, activate_log):
        tuples = self.getTuples(user_request, activate_log)
        relevant_tuples = self.getRelevantTuples(tuples, activate_log)
        relevant_tables = ", ".join([f"'{table}'" for table in relevant_tuples])
        sql_query = f"""
            SELECT table_name, fields_number, column_name, column_type, column_reference
            FROM txtai
            WHERE table_name IN ({relevant_tables})
        """
        complete_results = self.embeddings_complete.search(sql_query, self.embeddings_complete.count())
        # Costruzione del prompt
        dyn_string = "Suggested prompt:" + "\n"
        dyn_ref_string = ""
        i = 0
        limit = 0
        for result in complete_results:
            if result["column_reference"]:
                dyn_ref_string += "Foreign key: " + result["table_name"] + "." + result["column_name"] + "->" + json.loads(result["column_reference"])["table_name"] + "." + json.loads(result["column_reference"])["field_name"] + "\n"
            
            if (i == 0):
                dyn_string += "Table schema: " + result["table_name"] + " (" + result["column_name"] + ": " + result["column_type"] + ", "
                limit = int(result["fields_number"])
                i += 1
            elif (i + 1 < limit):
                dyn_string += result["column_name"] + ": " + result["column_type"] + ", "
                i += 1
            else:
                dyn_string += result["column_name"] + ": " + result["column_type"] + ")\n"
                i = 0
        
        dyn_string += f"{dyn_ref_string}"
        dyn_string += f"Answer with the right SQL query for MariaDB: {user_request}"
        return dyn_string

def main():
    # Piccolo script per testare la classe
    """ manager = IndexManager()

    data_dict_name = "orders"

    manager.createOrLoadIndex(data_dict_name)

    prompt = manager.promptGenerator("all information about products that belong to an order placed by a user whose first name is antonio", activate_log=True)

    print(prompt) """

if __name__ == "__main__":
    main()
