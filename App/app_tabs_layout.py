import json
import streamlit as st
import time
import streamlit.components.v1 as components
from index_manager import IndexManager

# Configurazione della pagina
st.set_page_config(
    page_title="ChatSQL",
    page_icon="favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={}
)

# Definizione di un font esterno
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&amp;display=swap" rel="stylesheet">
    <style>
        html, body {
            font-family: "Poppins", sans-serif !important;
        }
    </style>
""" , unsafe_allow_html= True)

# Icone per user e AI
avatarUser = "assets/icon_user.png"
avatarAI = "assets/icon_ai.png"

# Titolo dell'app
st.title("ChatSQL")

# Barra laterale
with st.sidebar:
    st.title("ChatSQL")
    st.subheader("Da linguaggio naturale a SQL")
    text_input = st.text_input(label="Cerca un dizionario dati", key="input_dz", autocomplete="ciao", placeholder="Cerca...", label_visibility="visible")
    if text_input:
        st.write("Hai inserito: ", text_input)

# Suddivisione del layout in tab
tab1, tab2 = st.tabs(["ChatSQL", "Dizionario dati"])

# Contenitore per i messaggi della chat
#contenitore = tab1.container(height=None, border=False)

manager = IndexManager()

documents = [
    (0, {"text":"Passeggiata mattutina lungo la spiaggia di sabbia, osservando l'alba", "intent":"descrizione delle attività"}, None),
    (1, {"text":"Costruire castelli di sabbia con i bambini, un'attività divertente per la famiglia", "intent":"attività familiari"}, None),
    (2, {"text":"Assaporare un cocktail di frutta tropicale seduti al bar sulla spiaggia", "intent":"cibo e bevande"}, None),
    (3, {"text":"Nuotare nelle acque cristalline del mare aperto", "intent":"sport acquatici"}, None),
    (4, {"text":"Raccogliere conchiglie lungo la riva, un hobby rilassante durante le vacanze", "intent":"attività di tempo libero"}, None),
    (5, {"text":"Ammirare il tramonto sul mare, un momento magico e suggestivo", "intent":"osservazione della natura"}, None),
    (6, {"text":"Cenare in riva al mare con vista sulle onde, una serata romantica", "intent":"esperienze culinarie"}, None),
    (7, {"text":"Partecipare a lezioni di surf per imparare a cavalcare le onde", "intent":"apprendimento di sport acquatici"}, None),
    (8, {"text":"Esplorare i fondali marini attraverso immersioni guidate", "intent":"avventure subacquee"}, None),
    (9, {"text":"Godersi il fresco della sera in una passeggiata lungomare", "intent":"attività serali"}, None)
]

manager.createIndex(documents)

# Disabilitare l'input testuale
def disableInput():
    st.session_state.inputdisabled = True

# Disabilitare i consigli
def disableAdvices():
    st.session_state.advicesdisabled = True

# Inizializzare la variabile di controllo sull'input
if "inputdisabled" not in st.session_state:
    st.session_state.inputdisabled = False

# Inizializzare la variabile di controllo sui consigli
if "advicesdisabled" not in st.session_state:
    st.session_state.advicesdisabled = False

# Inizializzare la cronologia della chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.welcome_mex = False

# Visualizzare la cronologia della chat
def display_chat_history() -> None:
    for message in st.session_state.messages:
        with tab1.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])

# Visualizzare la risposta in modalità ChatBOT-like
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Barra orizzontale
#tab2.divider()

# Visualizzare i messaggi nella cronologia
display_chat_history()

# Messaggio di benvenuto
if not st.session_state.welcome_mex:
    with tab1.chat_message("assistant", avatar=avatarAI):
        welcome = "Benvenuto! Tramite ChatSQL, puoi inserire una richiesta da convertire in una query SQL per interrogare un database. Come posso aiutarti?"
        st.markdown(welcome)
        st.session_state.messages.append({"role": "assistant", "avatar": avatarAI, "content": welcome})
        st.session_state.welcome_mex = True

# Esempi di richieste in linguaggio naturale
optimal_requests = [
    "Passeggiata mattutina lungo la spiaggia di sabbia, osservando l'alba",
    "Costruire castelli di sabbia con i bambini, un'attività divertente per la famiglia",
    "Assaporare un cocktail di frutta tropicale seduti al bar sulla spiaggia",
    "Raccogliere conchiglie lungo la riva, un hobby rilassante durante le vacanze"
]

# Layout con due colonne per riga
contenitore = ""
auto_request = ""

if not st.session_state.advicesdisabled:
    contenitore = tab1.container()
    with contenitore:
        st.subheader("Per iniziare, prova una delle seguenti richieste:")
        first_button_cols = st.columns(2)
        second_button_cols = st.columns(2)

        if first_button_cols and first_button_cols[0].button(optimal_requests[0]):
            auto_request = optimal_requests[0]
        elif first_button_cols and first_button_cols[1].button(optimal_requests[1]):
            auto_request = optimal_requests[1]
        elif second_button_cols and second_button_cols[0].button(optimal_requests[2]):
            auto_request = optimal_requests[2]
        elif second_button_cols and second_button_cols[1].button(optimal_requests[3]):
            auto_request = optimal_requests[3]

# Elemento nascosto per ancorare la fine della chat
tab1.markdown('<span id="phantom" style="visibility:hidden"></span>', unsafe_allow_html=True)

if request := (st.chat_input("Inserisci la richiesta", key="chat_SQL_input", disabled=st.session_state.inputdisabled, on_submit=disableInput) or auto_request):
    # Disabilitare gli aiuti dopo la prima richiesta dell'utente
    disableAdvices()

    # Script personalizzato per scorrere automaticamente alla fine della chat e cambiare tab
    components.html(
        """
            <script>
                var btn = window.parent.document.querySelector('[role="tablist"]').children[0];
                btn.click();
                var element = window.parent.document.getElementById('phantom');
                element.scrollIntoView({ behavior: 'smooth' });
            </script>
        """, height=0)
    
    # Visualizzare la richiesta dell'utente
    with tab1.chat_message("user", avatar=avatarUser):
        st.markdown(request)
    st.session_state.messages.append({"role": "user", "avatar": avatarUser, "content": request})

    if request != "":
        # Costruzione e visualizzazione della risposta
        response = ""
        with tab1.chat_message("assistant", avatar=avatarAI):
            with st.spinner('Caricamento...'):
                time.sleep(2)
                result_text = manager.getResult(request)
                response = result_text[0]["text"]
            st.write_stream(response_generator(response))

        st.session_state.messages.append({"role": "assistant", "avatar": avatarAI, "content": response})
        st.session_state.inputdisabled = False
        st.rerun()

with tab2:
    # Lettura del dizionario dati
    with open('../DizionarioDati/Ordini/ENG/orders.json', 'r') as file:
        schema = json.load(file)
        st.json(schema)