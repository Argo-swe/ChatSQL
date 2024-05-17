import streamlit as st
import time
import streamlit.components.v1 as components
from index_manager import IndexManager

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

# Inizializzare la cronologia della chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.welcome_mex = False

# Visualizzare la cronologia della chat
def display_chat_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Visualizzare la risposta in modalità ChatBOT-like
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Titolo dell'app
st.title("ChatSQL")

# Barra laterale
with st.sidebar:
    st.title("ChatSQL")
    st.subheader("Da linguaggio naturale a SQL")

# Barra orizzontale
st.divider()

# Visualizzare i messaggi nella cronologia
display_chat_history()

# Messaggio di benvenuto
if not st.session_state.welcome_mex:
    with st.chat_message("assistant"):
        welcome = "Benvenuto! Tramite ChatSQL, puoi inserire una richiesta da convertire in una query SQL per interrogare un database. Come posso aiutarti?"
        st.markdown(welcome)
        st.session_state.messages.append({"role": "assistant", "content": welcome})
        st.session_state.welcome_mex = True

# Esempi di richieste in linguaggio naturale
optimal_requests = [
    "Passeggiata mattutina lungo la spiaggia di sabbia, osservando l'alba",
    "Costruire castelli di sabbia con i bambini, un'attività divertente per la famiglia",
    "Assaporare un cocktail di frutta tropicale seduti al bar sulla spiaggia",
    "Raccogliere conchiglie lungo la riva, un hobby rilassante durante le vacanze"
]

# Layout con due colonne per riga
first_button_cols = st.columns(2)
second_button_cols = st.columns(2)

auto_request = ""

if first_button_cols[0].button(optimal_requests[0]):
    auto_request = optimal_requests[0]
elif first_button_cols[1].button(optimal_requests[1]):
    auto_request = optimal_requests[1]
elif second_button_cols[0].button(optimal_requests[2]):
    auto_request = optimal_requests[2]
elif second_button_cols[1].button(optimal_requests[3]):
    auto_request = optimal_requests[3]

# Elemento nascosto per ancorare la fine della chat
st.markdown('<div id="phantom"></div>', unsafe_allow_html=True)

if request := (st.chat_input("Inserisci la richiesta") or auto_request):

    # Script personalizzato per scorrere automaticamente alla fine della chat
    components.html(
    """
        <script>
            var element = window.parent.document.getElementById('phantom');
            element.scrollIntoView({ behavior: 'smooth' });
        </script>
    """, height=0)
    
    # Visualizzare la richiesta dell'utente
    with st.chat_message("user"):
        st.markdown(request)
    st.session_state.messages.append({"role": "user", "content": request})

    if request != "":
        # Costruzione e visualizzazione della risposta
        response = ""
        with st.chat_message("assistant"):
            with st.spinner('Caricamento...'):
                time.sleep(2)
                result_text = manager.getResult(request)
                response = result_text[0]["text"]
            st.write_stream(response_generator(response))

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
