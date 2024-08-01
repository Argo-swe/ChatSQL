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

## Formattazione codice

Per automatizzare la formattazione del codice sono stati implementati i linter per Frontend e Backend.
Installando le dipendenze del frontend verrà attivata il controllo automatico pre-commit del codice statico e dello stile.
```bash
cd frontend
npm i
```
Ogni volta prima di eseguire un commit verranno eseguiti i controlli e solo in caso di successo il commit verrà portato a termine.

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
    _Se si sta usando `nvm (Node Version Manager)` basta eseguire il comando_
   `    nvm use`
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

_perchè una variabile sia accessibile al codice processato (utilizzabile dall'utente) deve essere preceduta da `KITE_`\_

per utilizzare la variabile basta utilizzare

```
import.meta.env.VITE_KEY_2  // = VALUE_2
import.meta.env.KEY         // = undefined (vedi nota sopra)
```

### Localizzazione

Per gestire il multilingua viene utilizzata la libreria `vue-i18n` (versione 9).\
La documentazione è reperibile [qui](https://vue-i18n.intlify.dev/guide/essentials/started.html)

I file di lingua sono posizionati nella cartella `frontend/locales` e nominati con `SIGLA_LINGUA.json`. Internamente sono strutturati con una mappa chiave valore.

Le stringhe semplici e dirette sono inserite nel gruppo `text`, tutte in minuscolo, uno script all'avvio genera le realtive coppie chiave/valore con la prima lettera maiuscola.

#### Modificare i file di lingua

Un plugin utile alla compilazione e la verifica dei file di lingua per VScode è [i18n json editor](https://marketplace.visualstudio.com/items?itemName=thibault-vanderseypen.i18n-json-editor).\

Una volta installato aprire le relative configurazioni tramite il menu "Extensions" -> pulsante a ingranaggio -> Settings e impostare:\

- disabilitare il blocco sulle chiavi in UPPERCASE;
- aggiungere alle `supportedFolders` il termine `"locales"` _(dopo questa modifica va riavviato VScode)_.

Cliccare col tasto destro sulla cartella `frontend/locales` e cliccare `i18n json editor` alla fine delle modifiche ricordarsi di premere il tasto `Save` in alto a destra.
