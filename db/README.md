# Database di ChatSQL
---
## Introduzione
L'utilizzo del database è basato sull'engine SQLite. Utilizziamo questa soluzione perché richiede minima configurazione, è uno degli engine più leggeri e minimali e si basa su un comodo sistema single-file, per cui ciascun database corrisponde a un singolo file binario `.db`

## Modalità d'utilizzo
Essendo il database un singolo file, le connessioni e operazioni con la base di dati sono intermediate da librerie che necessitano solamente l'accesso a tale file.
### Creazione del database
Per creare il database:
- Scaricare con un package manager sqlite3 (esempio Windows: `winget install sqlite.sqlite`)
- Selezionare come working directory `db` ed eseguire `sqlite3`
- All'interno del terminale sqlite, eseguire `.open chatsql.db`;
- All'interno del terminale sqlite, eseguire `.read schema.sql` popolerà il database con le informazioni contenute nello scipt SQL.

### Comandi utili del terminale sqlite3
#### Connettersi al database
`.open chatsql.db` (va eseguito ad ogni nuova sessione).

#### Uscire dal terminale
`.exit`.

#### Generare un dump del database
All'interno del terminale sqlite:
```
.output nome_del_file.sql --Imposta l'output al file argomento
.dump
.output stdout  --Riporta l'output nel terminale
```
Per eseguire il dump di una sola tabella, si può eseguire `.dump nome_tabella`.

#### Eseguire script SQL
`.read nome_script.sql`.


#### Esportare entry in CSV / altri formati
```
.headers on -- Mantiene gli header nell'output, serve a ricreare la tabella se assente, da omettere altrimenti
.mode csv -- Altri formati utili sono "insert", per avere frasi SQL, "html" per avere tabelle html, "json" per formato JSON
.output nome_file.csv
SELECT ...  -- Query da utilizzare
.output stdout  -- Riporta l'output nel terminale
```
#### Importare informazioni in SQL / altri formati
Il processo è grossomodo analogo a esportare, con un solo accorgimento:
Quando viene dato il nome della tabella su cui importare il file, se la tabella NON esiste, la prima riga del file in input deve avere header.
Viceversa, se la tabella esiste, la prima riga NON deve evere header.
Lo stesso accorgimento è necessario per i formati `html` o `list`, `json` non ha differenza tra `.headers on` o `.headers off` e nemmeno `insert` (che tuttavia non genera output importabile direttamente).
Il processo è il seguente:
```
.mode csv
.import nome_file.csv nome_tabella
```

### Linee guida sulla persistenza del database attraverso il repository
Poiché versionare file binari come il `.db` è poco utile, è necessario utilizzare e mantenere aggiornati file che mantengano dati in forma ordinata, come ad esempio uno `schema.sql`, o dei file `.csv` che vengano poi inseriti da uno script `.sql`.