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
                    "intent": table['description'],
                    "column_name": column['name'],
                    "columns": column_names,
                    "column_description": column['description'],
                    "column_descriptions": column_descriptions,
                    "column_type": column['type'],
                    "column_types": column_types,
                    "column_reference": column['references'],
                    "column_references": column_references,
                    "text": column['description']
                    # "is column of": table['name']
                }
                documents.append(doc)
                
        return documents
    
def main():
    # Load schema data
    with open('../diz_dati_1.json', 'r') as file:
        schema = json.load(file)

    # Extract schema into documents
    extractor = SchemaExtractor(schema)
    extracted_documents = extractor.extract()

    # Initialize txtai embeddings model
    embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2", "content": True})

    # Index documents
    indexable_documents = []
    for idx, document in enumerate(extracted_documents):
        indexable_documents.append((idx, document, None))

    embeddings.index(indexable_documents)

    # Perform search
    result = embeddings.search("SELECT table_name, column_name, column_description, column_reference, MAX(score) FROM txtai WHERE similar('all users who payed their orders with paypal') GROUP BY table_name, column_name")

    # Process results
    tables = {}
    for entry in result:
        table_name = entry["table_name"]
        column_detail = {
            "column_name": entry["column_name"],
            "column_description": entry["column_description"],
            "column_references": entry.get("column_reference", "None")
        }
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(column_detail)

    # Print results in the desired format
    for table_name, columns in tables.items():
        print(f"Table name: {table_name}")
        print("Contains the following columns:")
        for column in columns:
            column_name = column['column_name']
            column_description = column['column_description']
            column_references = column.get('column_references', 'None')  # Using get for safe access
            print(f"Column named: {column_name}, described by: {column_description}. References: {column_references}")
        print() 
    
if __name__ == '__main__':
    main()