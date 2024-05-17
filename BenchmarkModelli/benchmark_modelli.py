import json
from txtai.embeddings import Embeddings

class SchemaExtractor:
    def __init__(self, data):
        self.data = data
    
    def extract(self):
        documents = []
        for table in self.data['tables']:
            # Ho provato ad aggiungere una riga all'indice, per inserire informazioni sulla tabella senza sovraccaricare le colonne
            #str_list = [
                    #table['name'],
                    #table['description']
                #]
            #if table["table_synonyms"] is not None:
                    #str_list.extend(table_synonym for table_synonym in table["table_synonyms"])
            #doc = {
                #"table_name": table['name'],
                #"intent": table["name"],
                #"text": table['description'],
                #"text": str_list,
            #}
            #documents.append(doc)

            for column in table['columns']:
                str_list = [
                    column['name'],
                    column['description']
                ]

                if column["column_synonyms"] is not None:
                    str_list.extend(column_synonym for column_synonym in column["column_synonyms"])

                doc = {
                    "table_name": table['name'],
                    #"intent": table["description"],
                    #"text": column['description'],
                    "text": str_list,
                }
                documents.append(doc)
                
        return documents
    
def main():

    with open('../dizionario_dati/orders.json', 'r') as file:
        schema = json.load(file)

    extractor = SchemaExtractor(schema)
    extracted_documents = extractor.extract()

    embeddings = Embeddings({"path": "google-bert/bert-base-uncased", "content": True})
    #google-bert/bert-base-uncased
    #FacebookAI/roberta-large
    #distilbert/distilbert-base-uncased
    #openai/clip-vit-large-patch14
    #sentence-transformers/all-MiniLM-L6-v2
    #sentence-transformers/all-mpnet-base-v2
    #sentence-transformers/distilbert-base-nli-mean-tokens
    #efederici/sentence-bert-base
    #efederici/e5-base-multilingual-4096
    #efederici/sentence-BERTino

    indexable_documents = []
    for idx, document in enumerate(extracted_documents):
        indexable_documents.append((idx, document, None))

    embeddings.index(indexable_documents)

    result = embeddings.search("SELECT table_name, text, AVG(score) FROM txtai WHERE similar('all users who payed their orders with paypal') GROUP BY table_name")
    
    for i in enumerate(result):
        print(i) 

if __name__ == '__main__':
    main()
