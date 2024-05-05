"""
Lo scopo di questo modulo è quello di prendere i documenti generati dal JSONSchemaPreprocessor, trasformarli in vettori e aggiungerli 
in un indice. La query dell'utente verrà a sua volta vettorializzata ("embedded"), e si andrà, tramite la search, sempre fornita dalla libreria
di txtai.embeddings, a cercare il migliore match tra query ed elementi nell'indice.
Questa è la versione più basilare possibile.
"""


# Importazione delle classi necessarie da moduli esterni
from txtai.embeddings import Embeddings
from json_schema_preprocessing_module import JSONSchemaPreprocessor
from user_query_preprocessing_module import UserQueryPreprocessor

class Indexer:
    """Costruttore per inizializzare l'oggetto Indexer"""
    def __init__(self, schema_path):
        # Inizializzazione del processore dello schema JSON con il percorso fornito
        self.schemaProcessor = JSONSchemaPreprocessor(schema_path)
        # Preprocessing dello schema e memorizzazione del risultato
        self.preprocessedSchema = self.schemaProcessor.preprocess_schema()
        
        # Creazione di un'istanza di Embeddings con specifico modello di trasformatori di testo
        self.embeddings = Embeddings({"model": "sentence-transformers", "path": "sentence-transformers/all-MiniLM-L6-v2"})
        # Indicizzazione dello schema preprocessato
        self.index_schema()
        
        # Inizializzazione del processore delle query utente
        self.queryProcessor = UserQueryPreprocessor()

    """Metodo per indicizzare lo schema preprocessato"""
    def index_schema(self):
        # Lista per raccogliere le descrizioni da indicizzare
        descriptions = []
        # Enumerazione delle descrizioni preprocessate e loro indicizzazione
        for idx, description in enumerate(self.preprocessedSchema):
            # Aggiunta di ciascuna descrizione alla lista con un indice associato
            descriptions.append((idx, description, None))
        
        # Utilizzo dell'oggetto Embeddings per creare l'indice
        self.embeddings.index(descriptions)

    """Metodo per cercare all'interno dell'indice basato su una query"""
    def search(self, query):
        # Preprocessing della query utente
        processed_query = self.queryProcessor.preprocess(query)
        # Ricerca degli embeddings più simili alla query preprocessata, limitando a 3 risultati
        # Questa è una brutta scelta ma non ho capito come farmi dare a prescindere i pertinenti
        results = self.embeddings.search(processed_query, limit=3)
        # Lista per raccogliere i risultati formattati
        formatted_results = []
        # Ciclo per formattare ogni risultato con la descrizione dello schema e il punteggio di similarità
        for result in results:
            # Creazione di una tupla con la descrizione e il punteggio
            formatted_result = (self.preprocessedSchema[result[0]], result[1])
            # Aggiunta del risultato formattato alla lista
            formatted_results.append(formatted_result)
        # Ritorno della lista di risultati formattati
        return formatted_results
