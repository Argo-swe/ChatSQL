import json
import streamlit as st
import time
import streamlit.components.v1 as components
from pathlib import Path
import sys
sys.path.append("backend")
from index_manager import IndexManager
from login_interface import LoginManager

current_dir = Path(__file__).resolve().parent

# Configurazione della pagina
st.set_page_config(
    page_title="ChatSQL",
    page_icon=f"{current_dir}/assets/favicon.ico",
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
avatarUser = f"{current_dir}/assets/icon_user.png"
avatarAI = f"{current_dir}/assets/icon_ai.png"

# Inizializzare variabile login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Inizializzare la variabile index manager
if "index_manager" not in st.session_state:
  st.session_state.index_manager = IndexManager()
  st.session_state.index_manager.createOrLoadIndex("orders")

# Inizializzare la variabile di controllo sull'input
if "inputdisabled" not in st.session_state:
    st.session_state.inputdisabled = False

# Inizializzare la cronologia della chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.welcome_mex = False

# Disabilitare l'input testuale
def disableInput():
    st.session_state.inputdisabled = True

# Visualizzare la cronologia della chat
def display_chat_history() -> None:
    for message in st.session_state.messages:
        with tab1.chat_message(message["role"], avatar=message["avatar"]):
            if message["role"] == "concierge" or message["role"] == "user":
                st.markdown(message["content"])
            else:
                st.code(message["content"])

# Titolo dell'app
st.title("ChatSQL")

# Barra laterale
with st.sidebar:
    st.title("ChatSQL")
    st.subheader("Da linguaggio naturale a SQL")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
    st.divider()
    st.markdown("Prova una delle seguenti richieste:")
    request_list = [
        "all information about products that belong to an order placed by a user whose first name is alex",
        "give me the email of the user whose name starts with the letter a",
        "the surname of users who paid for all their orders with PayPal",
        "the total amount of each order",
        "total cost of orders placed by users with PayPal",
        "all information on users who paid for their orders with PayPal",
        "the username of all users",
        "the total price of each order",
        "all information about products that belong to an order placed by alex71",
        "total cost of orders placed by users with PayPal",
        "all information on products that belong to the food category and that refer to an order placed by a user whose name is alex",
        "the name of the users who purchased three quantities of the same product yesterday"
    ]
    for request in request_list:
        st.code(request)

    st.divider()
    # Add login button
    if not st.session_state.logged_in:
        if st.button("Login"):
            LoginManager.show_dialog()
    else:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# Suddivisione del layout in tab
tab1, tab2, tab3 = st.tabs(["ChatSQL", "Dizionario dati", "Debug"])

# Visualizzare un'anteprima del dizionario dati in linguaggio naturale
@st.cache_data
def view_data_dict(dict_name) -> None:
    # Lettura del dizionario dati
    path = f"DizionarioDati/Ordini/ENG/{dict_name}"
    dict_preview = ""
    with open(path, 'r') as file:
        schema = json.load(file)
        dict_preview += f"""
        Il dizionario dati descrive un database chiamato {schema['database_name']}.
        \nIl database ha la seguente descrizione: {schema['database_description']}.
        \nIl database contiene le seguenti tabelle: """
        st.write(dict_preview)
        
        for table in schema['tables']:
            dict_preview = f"""
            \n{table['name']}: {table['description']}.
            \nLa tabella contiene le seguenti colonne: """
            
            for column in table['columns']:
                dict_preview += f"""
                \n{column['name']}: {column['description']}. """
            
            with st.container(border=True):
                st.write(dict_preview)

# Visualizzare i messaggi nella cronologia
display_chat_history()

# Messaggio di benvenuto
if not st.session_state.welcome_mex:
    with tab1.chat_message("assistant", avatar=avatarAI):
        welcome = "Benvenuto! Tramite ChatSQL, puoi inserire una richiesta da convertire in una query SQL per interrogare un database. Come posso aiutarti?"
        st.markdown(welcome)
        st.session_state.messages.append({"role": "concierge", "avatar": avatarAI, "content": welcome})
        st.session_state.welcome_mex = True

# Elemento nascosto per ancorare la fine della chat
tab1.markdown('<span id="phantom" style="visibility: hidden"></span>', unsafe_allow_html=True)

if request := (st.chat_input("Inserisci la richiesta...", key="chat_SQL_input", disabled=st.session_state.inputdisabled, on_submit=disableInput)):

    # Script personalizzato per scorrere automaticamente alla fine della chat e cambiare tab
    components.html("""
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
                time.sleep(1.5)
                response = st.session_state.index_manager.promptGenerator(request, activate_log=True)
            st.code(response)

        st.session_state.messages.append({"role": "assistant", "avatar": avatarAI, "content": response})
        st.session_state.inputdisabled = False
        st.rerun()

with tab2:
    dict_name = "orders.json"
    with st.expander("Descrizione del database"):
        view_data_dict(dict_name)

with tab3:
    raw_log = st.session_state.index_manager.readLogFile()
    if raw_log:
        with st.expander("Log file"):
            log = raw_log.replace('\n', '<br>')
            st.markdown(log, unsafe_allow_html=True)
        st.download_button(
            label="Scarica file (.txt)", 
            data=raw_log,
            file_name="chatsql_log.txt"
        )
    
