from indexer import Indexer  # Importazione della classe Indexer dal modulo indexer

"""Definizione della funzione principale del programma"""
def main():
    schema_path = 'database_schema.json'  # Percorso del file dello schema del database
    indexer = Indexer(schema_path)  # Creazione di un'istanza di Indexer con il percorso dello schema

    # Messaggi di benvenuto all'utente
    print("Questo è un test preliminare.")
    print("Fai una richiesta al database.")
    print("Scrivi 'basta' per terminare l'applicazione.\n")

    # Ciclo infinito per gestire l'input dell'utente fino a che non decide di terminare
    # Si può migliorare ma ancora non so come
    while True:
        query = input("Inserisci la query: ")  # Richiesta di input da parte dell'utente
        if query.lower() == 'basta':  # Controllo se l'utente desidera terminare il programma
            print("Terminazione.")  # Messaggio di congedo
            break  # Interruzione del ciclo

        search_results = indexer.search(query)  # Ricerca nel database usando la query fornita

        # Controllo e visualizzazione dei risultati di ricerca
        if search_results:
            print("\nRisultati rilevanti in base alla richiesta:")
            for table_description, score in search_results:
                print(f"Table: {table_description}, Punteggio di rilevanza: {score:.4f}")
        else:
            print("\nNessuna tabella trovata. Scrivi con più precisione.")
        
        print()  # Stampa di una linea vuota per separare le diverse iterazioni

"""Se il file è eseguito come script principale, avvia la funzione main()"""
if __name__ == "__main__":
    main()
