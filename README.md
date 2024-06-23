<h1 align="center">ChatSQL</h1>
<h2 align="center">Documentazione</h2>
<p align="center">La documentazione di progetto è visibile <a href="https://github.com/Argo-swe/Docs" target="_blank"><b>qui</b></a>.</p>

## Tecnologie
- NodeJS v20.14.0
- Python v3.10.14
- VueJS v3.4.21

## Avviare il progetto
Per avviare il progetto eseguire il comando
```
docker compose up
```
vengono avviati due container:
- frontend: sviluppato in VueJs ed espone l'interfacci utente
- backend: espone l'interfaccia di backend e i funzionamenti di ricerca semantica

## Backend
L'interfaccia di backend esposta è raggiungibile all'indirizzo [http://localhost:8000/docs](http://localhost:8000/docs)

### Variabili d'ambiente
Modificare il file `backend/.env` inserendo
```
KEY=VALUE
```

nel codice python per utilizzare la variabile
```
import os

PYTHON_VARIABLE = os.getenv("KEY", DEFAULT_VALUE)
```

## Frontend
### Rigenerare i metodi per interfacciarsi col `backend`
1. Avviare il container del `backend`
    ```
    docker compose up backend
    ```
1. Spostarsi nella cartella `frontend`
1. Impostare le versione di node corretta (vedi sopra)\
    *Se si sta usando `nvm (Node Version Manager)` basta eseguire il comando*
        ```
        nvm use
        ```
1. (Solo la prima volta) Installare i pacchetti
    ```
    npm i
    ```
1. Eseguire la chiamata di aggiornamento dell'interfaccia backend
    ```
    npm run build-api
    ```
### Variabili d'ambiente
Modificare il file `frontend/env.d.ts` inserendo la definizione della variabile di ambiente
```
interface ImportMetaEnv {
    KEY: string,
    VITE_KEY_2: string
}
```

modificare il file `frontend/.env` inserendo i valori da utilizzare
```
KEY=VALUE
VITE_KEY_2=VALUE_2
```
*perchè una variabile sia accessibile al codice processato (utilizzabile dall'utente) deve essere preceduta da `KITE_`*

per utilizzare la variabile basta utilizzare
```
import.meta.env.VITE_KEY_2  // = VALUE_2
import.meta.env.KEY         // = undefined (vedi nota sopra)
```
