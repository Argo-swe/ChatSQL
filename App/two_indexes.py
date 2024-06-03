import json
import sys
from txtai.embeddings import Embeddings
from txtai.pipeline import Translation
import timeit

"""
Try this queries: 
    _________

    1. all users who paid for their orders with PayPal
    _________
    
    Prompt
        Table schema: orders (id: integer, username: string, order_date: date, payment_method: string)
        Table schema: users (username: string, email: string, name: string, surname: string)
        Foreign key: orders.username->users.username
        Answer with the right SQL query for: all users who paid for their orders with PayPal
    
    ChatBOT answer:
        SELECT DISTINCT u.*
        FROM users u
        JOIN orders o ON u.username = o.username
        WHERE o.payment_method = 'PayPal';
    _________
    
    2. total cost of orders placed by users with PayPal
    _________

    Prompt
        Table schema: order_items (order_id: integer, product_id: integer, quantity: integer)
        Table schema: orders (id: integer, username: string, order_date: date, payment_method: string)
        Table schema: products (id: integer, name: string, price: decimal, category: integer)
        Foreign key: order_items.order_id->orders.id
        Foreign key: order_items.product_id->products.id
        Foreign key: orders.username->users.username
        Foreign key: products.category->categories.id
        Answer with the right SQL query for: total cost of orders placed by users with PayPal

    ChatBOT answer:
        SELECT SUM(oi.quantity * p.price) AS total_cost
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.payment_method = 'PayPal';
    _________

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
            for column in table['columns']:
                #str_list = ["table_name"]
                #if table["table_synonyms"] is not None:
                    #str_list.extend(table_synonym for table_synonym in table["table_synonyms"])
                #str_list = "the relation called " + table["name"]
                #if table["is_referenced_by"] is not None:
                    #str_list += " is referenced by this tables: "
                    #str_list += ', '.join(table_name for table_name in table["is_referenced_by"])
                #else:
                    #str_list += ""
                    #str_list.extend(column_synonym for column_synonym in column["column_synonyms"])
                #if column["references"]:
                    #str_list.append(column['references']["table_name"])
                str_list = table['description'] + ": " + column["name"]
                #str_list += ', '.join(table_name for table_name in table["is_referenced_by"])
                if column["column_synonyms"] is not None:
                    str_list += ", "
                    str_list += ', '.join(column_synonym for column_synonym in column["column_synonyms"])
                print(str_list)
                doc = {
                    "table_name": table['name'],
                    "table_description": str_list,
                    "column_synonyms": str_list,
                    "text": column['description']
                }
                documents.append(doc)

                # Inserimento sinonimi colonna
                """ if column["column_synonyms"] is not None:
                    str_list = [column_synonym for column_synonym in column["column_synonyms"]]
                    str_list.append(column['description'])
                    doc = {
                        "table_name": table['name'],
                        "text": str_list
                    }
                    documents.append(doc) """

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
    with open('DizionarioDati/Ordini/ENG/orders.json', 'r') as file:
        schema = json.load(file)

    # Estrazione dei campi e selezione dei dati per l'indexing
    extractor = SchemaExtractor(schema)
    documents_didx = extractor.extract()
    documents_kidx = extractor.extract_All()

    # Prova di subindex
    #embeddings = Embeddings(
        #content=True,
        #defaults=False,
        #indexes={
            #"keyword": {
            #"keyword": True
            #},
            #"dense": {
            #"path": "sentence-transformers/all-MiniLM-L6-v2"
            #}
        #}
    #)

    # Due embeddings (ricerca semantica e ricerca per keyword)
    #embeddings_didx = Embeddings(content=True, defaults=False, path="sentence-transformers/all-MiniLM-L6-v2")
    embeddings_didx = Embeddings(
        content=True,
        defaults=False,
        indexes={
            "column_description": {
                #"path": "sentence-transformers/all-MiniLM-L6-v2"
                "path": "sentence-transformers/all-MiniLM-L12-v2"
                #"path": "sentence-transformers/all-mpnet-base-v2"
            },
             "column_description_multilingual": {
                "path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                #"path": "sentence-transformers/distiluse-base-multilingual-cased-v2"
            },
            "table_description": {
                "path": "sentence-transformers/all-MiniLM-L12-v2",
                "columns": {
                    "text": "table_description"
                }
            },
            "table_description_multilingual": {
                "path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                #"path": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                "columns": {
                    "text": "table_description"
                }
            },
            "column_synonyms": {
                "path": "sentence-transformers/all-MiniLM-L6-v2",
                "columns": {
                    "text": "column_synonyms"
                }
            },
            "column_synonyms_multilingual": {
                "path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                "columns": {
                    "text": "column_synonyms"
                }
            }
        }
    )
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

    # Prova di traduzione automatica
    """ translate = Translation("facebook/mbart-large-50-many-to-one-mmt", findmodels=False)
    user_query_translated = translate(user_query, target="en")
    print(user_query_translated) """

    # Costruzione della query SQL per trovare le tabelle rilevanti
    """ sql_query = 
        SELECT table_name, text, MAX(score) as max, COUNT(*) as num_fields, column_synonyms
        FROM txtai WHERE similar(':x', 'column_description') and similar(':x', 'table_description') and similar(':x', 'column_synonyms') and score >= 0.2
        GROUP BY table_name
        ORDER BY table_name ASC
    """
    """ sql_query = 
        SELECT table_name, text, MAX(score) as max, COUNT(*) as num_fields, column_synonyms
        FROM txtai WHERE similar(':x', 'column_description') and similar(':x', 'column_description_2') 
        and similar(':x', 'table_description') and similar(':x', 'table_description_2') 
        and similar(':x', 'column_synonyms') and similar(':x', 'column_synonyms_2') and score >= 0.2
        GROUP BY table_name
        ORDER BY table_name ASC """
    """ sql_query = 
        SELECT table_name, text, MAX(score) as max, COUNT(*) as num_fields, column_synonyms
        FROM txtai WHERE similar(':x', 'column_description') and similar(':x', 'column_description_2')
        and similar(':x', 'table_description') and similar(':x', 'table_description_2') and score >= 0.2
        GROUP BY table_name
        ORDER BY table_name ASC """
    """ sql_query = SELECT DISTINCT table_name
            FROM txtai WHERE 
            similar(':x', 'column_description') and
            similar(':x', 'column_description_multilingual') and
            similar(':x', 'table_description') and
            similar(':x', 'table_description_multilingual') and
            similar(':x', 'column_synonyms') and 
            similar(':x', 'column_synonyms_multilingual') and
            score >= 0.3
            ORDER BY table_name ASC """
    """ sql_query =  SELECT table_name, text, score AS max
            FROM txtai WHERE 
            similar(':x', 'column_description') and
            similar(':y', 'column_description_multilingual') and
            score >= 0.2
            ORDER BY table_name ASC """
    #results = embeddings_didx.search(sql_query, embeddings_didx.count(), parameters={"x": user_query_translated, "y": user_query})
    """results = []
    relevant_table = []
    limit = 20
    for i in range(limit):
        #exclude_str = ", ".join([f"'{table[1]['table_name']}'" for table in enumerate(results)])
        exclude_str = ", ".join([f"'{table['table_name']}'" for table in results])
        print(exclude_str)
        sql_query = f
                SELECT table_name, score
                FROM txtai WHERE 
                table_name NOT IN ({exclude_str}) and
                similar(':x', 'column_description') and
                similar(':x', 'column_description_multilingual')
                and score >= 0.25
                ORDER BY score DESC LIMIT 1 
        relevant_table = embeddings_didx.search(sql_query, parameters={"x": user_query})
        if (relevant_table):
            results += relevant_table
        else:
            break
        print(results)
    print(i)"""
    """relevant_tables = []
        relevant_table = []
        limit = 20
        for i in range(limit):
            excluded_tables = ", ".join([f"'{table['table_name']}'" for table in relevant_tables])
            sql_query = f
                SELECT table_name, score
                FROM txtai WHERE 
                table_name NOT IN ({excluded_tables}) and
                similar(':x', 'column_description') and
                similar(':x', 'column_description_multilingual') and
                similar(':x', 'table_description_with_column_name_and_synonyms')
                and score >= 0.25
                ORDER BY score DESC
                LIMIT 1

            relevant_table = self.embeddings.search(sql_query, parameters={"x": user_request})
            if (relevant_table):
                relevant_tables += relevant_table
            else:
                break
        return relevant_tables"""
    query_limit = 20
    sql_query = f"""
        SELECT table_name, MAX(score) AS max_score, AVG(score) AS avg_score
        FROM txtai WHERE 
        similar(':x', 'column_description') and
        similar(':x', 'column_description_multilingual') and
        score >= 0.2
        GROUP BY table_name
        ORDER BY max_score DESC 
        LIMIT {query_limit}
    """
    results = embeddings_didx.search(sql_query, limit=query_limit*10, parameters={"x": user_query})
    #HAVING max >= 0.45 OR (max >= 0.28 AND num_fields > 1)
    # Visualizzazione del risultato nel formato {'table_name', 'text', 'sum', 'avg', 'num_fields'}
    for i in enumerate(results):
        print(i)

    # Arresto del programma per testare i due indici separatamente
    sys.exit()
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