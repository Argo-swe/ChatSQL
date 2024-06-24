<h1 align="center">ChatSQL</h1>
<h2 align="center">Documentazione</h2>
<p align="center">La documentazione di progetto è visibile <a href="https://github.com/Argo-swe/Docs" target="_blank"><b>qui</b></a>.</p>

## Tecnologie
- NodeJS v20.14.0
- Python v3.10.14
- VueJS v3.4.21

## Avviare il progetto
1. Creare i due file `backend/.env.local` e `backend/.env.local` per gestire i valori da utilizzare in locale per le variabili d'ambiente.\
Si possono copiare i relativi file `.env`, popolando le variabili richieste.\
Vedi relative sottosezioni delle variabili d'ambiente.
1. eseguire il comando
    ```
    docker compose up
    ```
    vengono avviati due container:
    - frontend: sviluppato in VueJs ed espone l'interfacci utente
    - backend: espone l'interfaccia di backend e i funzionamenti di ricerca semantica

## Backend
L'interfaccia di backend esposta è raggiungibile all'indirizzo [http://localhost:8000/docs](http://localhost:8000/docs)

### Variabili d'ambiente
Creare un file locale il file `backend/.env.local` inserendo le variabili che si vogliono modificare rispetto al file `backend/.env` o che hanno valori da impostare
```
KEY=VALUE
```

nel codice python per utilizzare la variabile
```
import os

PYTHON_VARIABLE = os.getenv("KEY", DEFAULT_VALUE)
```
#### Variabili con valore da impostare per sicurezza
- JWT_SECRET

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

Creare un file locale il file `frontend/.env.local` inserendo le variabili che si vogliono modificare rispetto al file `frontend/.env` o che hanno valori da impostare
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
