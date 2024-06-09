<h1 align="center">ChatSQL</h1>
<h2 align="center">Documentazione</h2>
<p align="center">La documentazione di progetto è visibile <a href="https://github.com/Argo-swe/Docs" target="_blank"><b>qui</b></a>.</p>

## Tecnologie
- NodeJS v20.14.0
- Python v3.10
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
L'interfaccia di backend esposta è raggiungibile all'indirizzo [http://localhost:5000/api-doc](http://localhost:5000/api-doc)


## Frontend
### Rigenerare i metodi per interfacciarsi col `backend`
1. Avviare il container del `backend`
    ```
    docker compose up backend
    ```
1. (Solo la prima volta) Installare i pacchetti
    ```
    npm i
    ```
1. Spostarsi nella cartella `frontend` e eseguire la chiamata di aggiornamento dell'interfaccia
    ```
    npm run build-api
    ```
