import json
from txtai.embeddings import Embeddings

class SchemaExtractor:
    def __init__(self, data):
        self.data = data
    
    def extract(self):
        documents = []
        for table in self.data['tables']:
            column_names = [column['name'] for column in table['columns']]
            column_descriptions = [column['description'] for column in table['columns']]
            column_types = [column['type'] for column in table['columns']]
            column_references = [column['references'] for column in table['columns']]

            for column in table['columns']:
                doc = {
                    "table_name": table['name'],
                    "columns": column_names,
                    "column_description": column_descriptions,
                    "column_type": column_types,
                    "column_reference": column_references,
                    "intent": table['description'],
                    "column_name": column['name'],
                    "text": column['description'],
                    # "is column of": table['name']
                }
                documents.append(doc)
                
        return documents
    
def main():

    with open('../diz_dati_1.json', 'r') as file:
        schema = json.load(file)

    extractor = SchemaExtractor(schema)
    extracted_documents = extractor.extract()

    embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2", "content": True})

    indexable_documents = []
    for idx, document in enumerate(extracted_documents):
        indexable_documents.append((idx, document, None))

    embeddings.index(indexable_documents)

    result = embeddings.search("SELECT table_name, columns, column_description, column_reference, MAX(score) FROM txtai WHERE similar('all users who payed their orders with paypal') GROUP BY table_name")
    for i in enumerate(result):
        print("Table: " + i[1]["table_name"]) 
        print("With columns: ")
        print("  " + i[1]["columns"])
        print("Described by:")
        print("  " + i[1]["column_description"])
        print("And references:")
        print("  " + i[1]["column_reference"] + "\n")
    
if __name__ == '__main__':
    main()