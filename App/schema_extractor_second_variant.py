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
                    "intent": column['synonyms'],
                    "column_name": column['name'],
                    "columns": column_names,
                    "column_description": column['description'],
                    "column_descriptions": column_descriptions,
                    "column_type": column['type'],
                    "column_types": column_types,
                    "column_reference": column['references'],
                    "column_references": column_references,
                    "text": column['description']
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

    query = input("Please enter your query: ")

    sql_query = f"SELECT id, table_name, columns, column_description, column_reference, MAX(score) FROM txtai WHERE similar('{query}') GROUP BY table_name"
    results = embeddings.search(sql_query)

    unique_tables = set()
    for result in results:
        document_id = int(result['id'])
        table_name = extracted_documents[document_id]['table_name']
        unique_tables.add(table_name)

    table_data = {}
    for table_name in unique_tables:
        table_data[table_name] = {
            "table_name": table_name,
            "columns": []
        }
        for doc in extracted_documents:
            if doc['table_name'] == table_name:
                table_data[table_name]['columns'].append({
                    "column_name": doc['column_name'],
                    "column_description": doc['column_description'],
                    "column_references": doc['column_reference']
                })

    print("\nGiven the following tables with respective columns:\n")
    for table_name, data in table_data.items():
        print(f"Table name: {table_name}")
        print("Contains the following columns:")
        for column in data['columns']:
            print(f"Column named: {column['column_name']}, described by: {column['column_description']}. External references: {column['column_references']}")
        print()

    print(f"Answer with the right SQL query for: {query}")

if __name__ == '__main__':
    main()
