"""
Questo modulo serve a pulire la query in modo che sia più facilmente comprensibile possibile per qualunque modello scegliamo.
Questo significa che la query va:
NORMALIZZATA: messa in una forma standard. Vuol dire senza punteggiatura e senza maiuscole.
TOKENIZZATA: il testo della query va spezzato in segmenti più piccoli.
LEMMATIZZATA: ogni token viene lemmatizzato, ovvero riportato al suo lemma originale (il vocabolo che si troverebbe nel dizionario).
FILTRATA DALLE STOP-WORDS: le stop-words sono termini molto comuni che costituiscono del rumore per il modello. Vanno rimossi.
Ci sarebbe una parte di applicazione dei sinonimi, ma è meglio sfruttare i campi presenti nel dizionario dati.
"""

import spacy
# from nltk.corpus import wordnet as wn

class UserQueryPreprocessor:
    """Costruttore per inizializzare l'oggetto UserQueryPreprocessor"""
    def __init__(self, synonym_map=None):
        # Caricamento del modello linguistico inglese di spaCy
        self.nlp = spacy.load('en_core_web_sm')
        # Inizializzazione di una mappa dei sinonimi, se fornita, altrimenti usa un dizionario vuoto
        self.synonym_map = synonym_map or {}

    """Metodo per normalizzare il testo"""
    def normalize(self, text):
        # Conversione del testo in minuscolo e rimozione di tutti i caratteri di punteggiatura
        text = text.lower().translate(str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))
        return text

    """Metodo per tokenizzare il testo e lemmatizzarlo"""
    def tokenize_and_lemmatize(self, text):
        # Analisi del testo con il modello spaCy
        doc = self.nlp(text)
        # Lista per raccogliere i token
        tokens = []
        # Iterazione su ogni token nel documento
        for token in doc:
            # Controllo che il token non sia uno stop word o un segno di punteggiatura
            if not token.is_stop and not token.is_punct:
                # Aggiunta del lemma del token alla lista dei token
                tokens.append(token.lemma_)

        return tokens

    """Applicazione sinonimi con spaCy ma non mi interessa più averla qui"""
    # def apply_synonyms(self, tokens):
    #     new_tokens = []
    #     for token in tokens:
    #         if token in self.synonym_map:
    #             new_tokens.append(self.synonym_map[token])
    #         else:
    #             synonyms = wn.synsets(token, pos=wn.VERB)
    #             if synonyms:
    #                 lemmas = synonyms[0].lemmas()
    #                 if lemmas:
    #                     new_tokens.append(lemmas[0].name())
    #                 else:
    #                     new_tokens.append(token)
    #             else:
    #                 new_tokens.append(token)
    #     return new_tokens

    """Effettivo preprocessing"""
    def preprocess(self, query):
        # Normalizzazione della query
        normalized_text = self.normalize(query)
        # Tokenizzazione e lemmatizzazione del testo normalizzato
        tokens = self.tokenize_and_lemmatize(normalized_text)
        # Unione dei token in una stringa e ritorno del risultato
        return ' '.join(tokens)