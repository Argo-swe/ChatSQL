import re
import streamlit as st

class LoginManager:
    # temporanee per testare le credenziali , successivamente aggiungere funzione con connessione a db 
    tmp_username = "adminADMIN1"
    tmp_password = "Admin123123!"

    min_length = 8
    max_length = 20

    @staticmethod
    def check_not_null(credential):
        return bool(credential)

    @staticmethod
    def check_min_length(credential):
        return len(credential) >= LoginManager.min_length

    @staticmethod
    def check_max_length(credential):
        return len(credential) <= LoginManager.max_length

    # La password deve contenere: un numero, una lettera maiuscola, un carattere speciale
    @staticmethod
    def check_password(password):
        return re.match(r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[!@#$&*]).{8,}$', password) is not None

    # Controllo di code injection
    @staticmethod
    def check_injection(input_string):
        # Regex pattern per intercettare caratteri pericolosi
        pattern = re.compile(r"[;\'\"\-\-#]" )
        return pattern.search(input_string) is None

    @staticmethod
    def check_db(username, password):
        return username == LoginManager.tmp_username and password == LoginManager.tmp_password

    @staticmethod
    def verify(username, password):
        """Errore nell'inserimento delle password."""
        if not LoginManager.check_not_null(username):
            st.error("L'username non può essere vuoto.")
            return False
        if not LoginManager.check_not_null(password):
            st.error("La password non può essere vuota.")
            return False
        if not LoginManager.check_min_length(username):
            st.error("L'username deve avere almenno 8 caratteri.")
            return False
        if not LoginManager.check_max_length(username):
            st.error("L'username non può essere più lunga di 20 caratteri.")
            return False
        if not LoginManager.check_min_length(password):
            st.error("La password deve avere almenno 8 caratteri.")
            return False
        if not LoginManager.check_password(password):
            st.error("La Password deve includere almeno un numero,una maiuscola e un carattere spaciale.")
            return False
        if not LoginManager.check_injection(username) or not LoginManager.check_injection(password):
            st.error("La password deve contenere almeno uno tra questi caratteri: ;, ', \", --, #.")
            return False
        if not LoginManager.check_db(username, password):
            st.error("Le credenziali non sono presenti nel database.")
            return False
        return True

    @st.experimental_dialog("Login")
    def show_dialog():
        """Finestra di dialogo per il login."""
        with st.form("login_form"):
            st.write("Inserisci le credenziali d'accesso:")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Accedi")

            if submit_button:
                if LoginManager.verify(username, password):
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                    # per ora non succede nulla
                else:
                    st.session_state.logged_in = False
                    # dovrebbe rimanere lì con un messaggio di errore
