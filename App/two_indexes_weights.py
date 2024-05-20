import json
#import sys
from txtai.embeddings import Embeddings
import timeit

"""
    Semantic search - Attempts:
        1. give me the email of the user whose name starts with the letter a
        2. all users who paid for their orders with PayPal
        3. a user who paid for his orders with PayPal
        4. all information on users who paid for their orders with PayPal
        5. the total amount of each order
        6. the username of all users
        7. all information about products that belong to an order placed by antonio
        8. all information about products that belong to an order placed by a user whose birth name is antonio
        9. all information about products that belong to an order placed by a user whose first name is antonio
        10. all information about products that belong to an order placed by a user whose surname is bonaparte 
"""

class SchemaExtractor:
    # Setup della classe
    def __init__(self, data):
        self.data = data

    # Funzione per verificare il tempo di esecuzione della search
    def timer(self, embeddings, query):
        elapsed = timeit.timeit(lambda: embeddings.search(query), number=250)
        print(f"{elapsed / 250} seconds per query")
    
    # Estrazione per il primo indice (ricerca semantica tramite LLM)
    def extract(self):
        documents = []
        for table in self.data['tables']:
            # Inserimento descrizione tabella
            doc = {
                "table_name": table['name'],
                "text": table['description'],
                "weights": 0.5
                }
            documents.append(doc)

            # Inserimento sinonimi tabella
            if table["table_synonyms"] is not None:
                str_list = [table_synonym for table_synonym in table["table_synonyms"]]
                #str_list.append(table['description'])
                doc = {
                "table_name": table['name'],
                "text": str_list,
                "weights": 0.5
                }
                documents.append(doc)
            
            for column in table['columns']:
                # Inserimento descrizione colonna
                doc = {
                    "table_name": table['name'],
                    "text": column['description'],
                    "weights": 1
                }
                documents.append(doc)

                # Inserimento sinonimi colonna
                if column["column_synonyms"] is not None:
                    str_list = [column_synonym for column_synonym in column["column_synonyms"]]
                    #str_list.append(column['description'])
                    doc = {
                        "table_name": table['name'],
                        "text": str_list,
                        "weights": 0.8
                    }
                    documents.append(doc)

        return documents
    
    # Estrazione per il secondo indice (ricerca per keyword al fine di generare il prompt senza passare per il dizionario dati)
    def extract_All(self):
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
    
def main():
    # Lettura del dizionario dati
    with open('../DizionarioDati/Ordini/ENG/orders.json', 'r') as file:
        schema = json.load(file)

    # Estrazione dei campi e selezione dei dati per l'indexing
    extractor = SchemaExtractor(schema)
    documents_didx = extractor.extract()
    documents_kidx = extractor.extract_All()

    # Due embeddings (ricerca semantica e ricerca per keyword)
    embeddings_didx = Embeddings(content=True, defaults=False, path="sentence-transformers/all-MiniLM-L6-v2")
    embeddings_kidx = Embeddings(content=True, defaults=False, keyword=True)

    indexable_documents_didx = []
    for idx, document in enumerate(documents_didx):
        indexable_documents_didx.append((idx, document, None))

    indexable_documents_kidx = []
    for idx, document in enumerate(documents_kidx):
        indexable_documents_kidx.append((idx, document, None))

    # Primo indice
    embeddings_didx.index(indexable_documents_didx)

    # Salvataggio dell'indice in un'apposita directory
    embeddings_didx.save("Indici/idx")
    
    # Inserimento della richiesta dell'utente in linguaggio naturale
    user_query = input("Please enter your request: ")

    # Costruzione della query SQL per trovare le tabelle rilevanti
    sql_query = """
        SELECT table_name, text, AVG(score) as media, SUM(score * weights) / SUM(weights) AS media_pesata
        FROM txtai WHERE similar(':x')
        GROUP BY table_name
        HAVING media >= 0.2 AND media_pesata >= 0.2
        ORDER BY table_name ASC
    """
    results = embeddings_didx.search(sql_query, embeddings_didx.count(), parameters={"x": user_query})

    # Visualizzazione del risultato nel formato {'table_name', 'text', 'media', 'media_pesata'}
    for i in enumerate(results):
        print(i)

    # Arresto del programma per testare i due indici separatamente
    #sys.exit()
    #extractor.timer(embeddings_didx, sql_query)

    # Secondo indice
    embeddings_kidx.index(indexable_documents_kidx)

    # Salvataggio dell'indice in un'apposita directory
    embeddings_kidx.save("Indici/idx_2")

    # Costruzione della query SQL per estrarre i dati relativi alle tabelle rilevanti
    sql_query = """
        SELECT table_name, fields_number, column_name, column_type, column_reference
        FROM txtai
        WHERE similar(':x')
        ORDER BY table_name ASC
    """
    complete_results = embeddings_kidx.search(sql_query, embeddings_kidx.count(), parameters={"x": {result[1]["table_name"] for result in enumerate(results)}})

    #extractor.timer(embeddings_kidx, sql_query)

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
    dyn_string += f"Answer with the right SQL query for: {user_query}"
    print(f"{dyn_string}")
    
if __name__ == '__main__':
    main()