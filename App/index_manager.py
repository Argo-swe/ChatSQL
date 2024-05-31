import sys
from txtai.embeddings import Embeddings
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
        
    def setDataDictName(self, data_dict_name):
        self.data_dict_name = data_dict_name

    def createIndex(self, documents):
        self.embeddings.index(documents)

    def __getTuples(self, user_request):
        query_limit = 20
        sql_query = f"""
            SELECT table_name, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE 
            similar(':x', 'column_description') and
            similar(':x', 'column_description_multilingual') and
            score >= 0.25
            GROUP BY table_name HAVING
            avg_score >= 0.25
            ORDER BY max_score DESC
            LIMIT {query_limit}
        """
        #similar(':x', 'table_description_with_column_name_and_synonyms') and
        tuples = self.embeddings.search(sql_query, limit=query_limit*10, parameters={"x": user_request})
        relevant_tuples = self.__getRelevantTuples(tuples)
        return relevant_tuples

    def __getRelevantTuples(self, tuples):
        relevant_tuples = []
        score = 0
        max_score = tuples[0]['max_score']
        for tuple in enumerate(tuples):
            scoring_distance = score - tuple[1]['max_score']
            if tuple[1]['max_score'] >= 0.45:
                relevant_tuples.append([tuple[1]['table_name'], scoring_distance, tuple[1]['max_score']])
                score = tuple[1]['max_score']
            elif scoring_distance <= 0.2:
                relevant_tuples.append([tuple[1]['table_name'], scoring_distance, tuple[1]['max_score']])
                score = tuple[1]['max_score']
        return relevant_tuples
    
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
    manager.promptGenerator("give me the total amount of each order")

if __name__ == "__main__":
    main()
