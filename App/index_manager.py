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
                    "text": "relevant_information"
                }
            }
        }
    )

    def createIndex(self, documents):
        self.embeddings.index(documents)

    def getResult(self, user_request):
        query_limit = 20
        sql_query = f"""
            SELECT table_name, MAX(score) AS max_score, AVG(score) AS avg_score
            FROM txtai WHERE 
            similar(':x', 'column_description') and
            similar(':x', 'column_description_multilingual') and
            similar(':x', 'table_description_with_column_name_and_synonyms') and
            score >= 0.2
            GROUP BY table_name HAVING
            avg_score >= 0.25
            ORDER BY max_score DESC
            LIMIT {query_limit}
        """
        relevant_tables = self.embeddings.search(sql_query, limit=query_limit*10, parameters={"x": user_request})
        
        return relevant_tables
    
    def saveIndex(self):
        self.embeddings.save("idx")
    
    def loadIndex(self):
        self.embeddings.load("idx")

    def createOrLoadIndex(self, documents):
        createIDX = True
        if "idx" in next(os.walk(os.getcwd())):
            createIDX = False
        if createIDX:
            self.createIndex(documents)
            self.saveIndex()
            return True
        else:
            self.loadIndex()
            return False
        
    def printFormattedResult(self, result):
        formatted_results = []
        if result:
            for item in result:
                formatted_string = f"Documento scelto: {item['text']}\nPunteggio di rilevanza: {item['score']:.4f}"
                formatted_results.append(formatted_string)
            formatted_output = "\n".join(formatted_results)
        else:
            formatted_output = "Nisba"
        
        print(formatted_output)

def main():
    manager = IndexManager()
    documents = [
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
    ]

    manager.createOrLoadIndex(documents)

    prompt = "bella giornata al mare"
    result = manager.getResult(prompt)
    manager.printFormattedResult(result)

if __name__ == "__main__":
    main()
