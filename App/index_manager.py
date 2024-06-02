import sys
from txtai.embeddings import Embeddings
from
import os

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
                        "text": "intent"
                    }
                }
            }
        )
        self.path = "Indici"
        self.log_name = "chatsql_log.txt"
        
    def setDataDictName(self, data_dict_name):
        self.data_dict_name = data_dict_name

    def createIndex(self):
        documents = 
        self.embeddings.index(documents)

    def __getTuples(self, user_request):
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
        #similar(':x', 'table_description_with_column_name_and_synonyms') and
        tuples = self.embeddings.search(sql_query, limit=query_limit*10, parameters={"x": user_request})
        
        relevant_tuples = self.__getRelevantTuples(tuples, user_request, 1)
        return relevant_tuples

    def __getRelevantTuples(self, tuples, user_request, is_log):
        if is_log:
            log = self.semanticSearchLog(user_request, tuples)
            log.write("\nFase 2 - seconda estrazione\n")
            log.write("Lista delle tabelle rilevanti:\n")
        relevant_tuples = []
        score = 0
        max_score = tuples[0]['max_score']
        for tuple in enumerate(tuples):
            scoring_distance = score - tuple[1]['max_score']
            if tuple[1]['max_score'] >= 0.45:
                if is_log == 1:
                    log.write("La tabella " + tuple[1]["table_name"] + " viene mantenuta poiché ha un punteggio sufficientemente alto\n")
                relevant_tuples.append([tuple[1]['table_name'], scoring_distance, tuple[1]['max_score'], tuple[1]['avg_score']])
                score = tuple[1]['max_score']
            elif scoring_distance <= 0.25:
                if is_log == 1:
                    log.write("La tabella " + tuple[1]["table_name"] + " viene mantenuta poiché la differenza di punteggio rispetto alla tabella precedente è inferiore a 0.25\n")
                relevant_tuples.append([tuple[1]['table_name'], scoring_distance, tuple[1]['max_score'], tuple[1]['avg_score']])
                score = tuple[1]['max_score']
            else:
                if is_log == 1:
                    log.write("Le tabelle rimamenti vengono scartate poiché lo score non è abbastanza alto e la differenza di punteggio rispetto alle tabelle immediatamente precedenti è eccessivamente alta\n")
                break
        log.close()
        return relevant_tuples
    
    def semanticSearchLog(self, user_request, tuples):
        log = open(self.log_name, "w")
        log.write("Richiesta: " + user_request + "\n\n")
        log.write("Fase 1 - prima estrazione\n")
        log.write("Le tabelle vengono estratte in base al punteggio massimo ottenuto confrontando la richiesta utente con la descrizione dei campi della tabella\n")
        log.write("Lista delle tabelle pertinenti (punteggio maggiore di 0.28):\n")
        for tuple in enumerate(tuples):
            log.write(tuple[1]["table_name"] + ": " + str(tuple[1]["max_score"]) + "\n")
            log.write("Descrizione colonna: " + tuple[1]["text"] + "\n\n")
            
        tokens_importance = self.embeddings.explain(user_request, [tuple["text"] for tuple in tuples])

        log.write("La descrizione delle colonne è composta da tanti termini\n")
        log.write("Questa è la classifica di importanza dei termini di ciascuna descrizione:\n")
        for token_importance in tokens_importance:
            log.write(token_importance["text"] + "\n")
            for token, score in sorted(token_importance["tokens"], key=lambda x: x[1], reverse=True):
                log.write(token + ": " + str(score) + "\n")
            log.write("\n")
        return log

    def readLogFile(self):
        log = open(self.log_name, "r")
        print(log.read())
    
    def saveIndex(self):
        self.embeddings.save(f"{self.path}/{self.data_dict_name}")
    
    def loadIndex(self):
        #self.embeddings.load(f"{self.path}/{self.data_dict_name}")
        self.embeddings.load(f"Indici/idx")

    def createOrLoadIndex(self, documents):
        createIDX = True
        path = f"{self.path}/{self.data_dict_name}"
        if os.path.exists(path):
            createIDX = False
        if createIDX:
            self.createIndex(documents)
            self.saveIndex()
            return True
        else:
            self.loadIndex()
            return False
        
    def promptGenerator(self, user_request):
        relevant_tuples = self.__getTuples(user_request)

        formatted_results = []
        """ if result:
            for item in result:
                formatted_string = f"Documento scelto: {item['text']}\nPunteggio di rilevanza: {item['score']:.4f}"
                formatted_results.append(formatted_string)
            formatted_output = "\n".join(formatted_results)
        else:
            formatted_output = "Nisba" """
        
        for i in enumerate(relevant_tuples):
            print(i)

def main():
    manager = IndexManager()

    """ documents = [
        (0, {"text":"Passeggiata mattutina lungo la spiaggia di sabbia, osservando l'alba", "intent":"descrizione delle attività"}, None),
        (1, {"text":"Costruire castelli di sabbia con i bambini, un'attività divertente per la famiglia", "intent":"attività familiari"}, None),
        (2, {"text":"Assaporare un cocktail di frutta tropicale seduti al bar sulla spiaggia", "intent":"cibo e bevande"}, None),
        (3, {"text":"Nuotare nelle acque cristalline del mare aperto", "intent":"sport acquatici"}, None),
        (4, {"text":"Raccogliere conchiglie lungo la riva, un hobby rilassante durante le vacanze", "intent":"attività di tempo libero"}, None),
        (5, {"text":"Ammirare il tramonto sul mare, un momento magico e suggestivo", "intent":"osservazione della natura"}, None),
        (6, {"text":"Cenare in riva al mare con vista sulle onde, una serata romantica", "intent":"esperienze culinarie"}, None),
        (7, {"text":"Partecipare a lezioni di surf per imparare a cavalcare le onde", "intent":"apprendimento di sport acquatici"}, None),
        (8, {"text":"Esplorare i fondali marini attraverso immersioni guidate", "intent":"avventure subacquee"}, None),
        (9, {"text":"Godersi il fresco della sera in una passeggiata lungomare", "intent":"attività serali"}, None) 
    ] """

    manager.setDataDictName("orders")

    manager.loadIndex()

    #manager.createOrLoadIndex(documents)

    """ prompt = "bella giornata al mare"
    result = manager.getResult(prompt)
    manager.printFormattedResult(result) """
    #print(manager.data_dict_name)
    """ utils_folder_path = os.path.dirname(os.path.realpath(__file__))
    dictionaries_folder_path = os.path.abspath(os.path.join(utils_folder_path, "Indici")) """
    #print(dictionaries_folder_path)
    manager.promptGenerator("all information about products that belong to an order placed by a user whose first name is antonio")

if __name__ == "__main__":
    main()
