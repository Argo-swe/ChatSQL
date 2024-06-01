import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Dictionaries",
    page_icon="assets/favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={}
)

st.title("Dictionaries list")

# dictionary validation
def validate_dictionary():
    return True

# add dictionary modal
@st.experimental_dialog("Add a dictionary")
def dictionary_modal(operation, update_index):
    with st.form("my_form"):
        name_container = st.container()
        description_container = st.container()
        file_container = st.container()

        if not operation == 'dic_update':
            default_name = st.session_state["data"]["name"][update_index] if operation == 'desc_update' and update_index else ""
            default_description = st.session_state["data"]["description"][update_index] if operation == 'desc_update' and update_index else ""
            name = name_container.text_input("Name", default_name, None, "name")
            description = description_container.text_input("Description", default_description, None, "description")

        if not operation == 'desc_update':
            uploaded_file = file_container.file_uploader("Choose a file", None, False, "uploaded_file")

        submitted = st.form_submit_button("Submit")
        if submitted:
            has_error = False

            if not operation == 'dic_update':
                if name == "":
                    has_error = True
                    name_container.warning("Insert a name")

                if description == "":
                    has_error = True
                    description_container.warning("Insert a description")

            if not (operation == 'desc_update' or validate_dictionary()):
                has_error = True
                file_container.warning("Insert a description")

            if not has_error:
                st.success("Submitted")
                st.rerun()
            else:
                st.stop

# display add button
_,c1= st.columns([4,1])
if c1.button("\+ Add a dictionary", type="secondary"):
    dictionary_modal('add', None)

# dictionaries dataset
# TODO: change mock data with DB data
st.session_state.data = pd.DataFrame(
    {
        "id": [1, 2, 3],
        "name": ["Musica", "Ristorante", "Cinema"],
        "description": ["Dizionario riferito alla musica", "Dizionario riferito alla ristorazione", "Dizionario riferito al cinema"],
    }
)

# delete handler
def delete_dictionary(dictionary_index):
    print("delete", dictionary_index)
    print(st.session_state["data"])
    st.session_state["data"] = (
        st.session_state["data"].drop(dictionary_index, axis=0).reset_index(drop=True)
    )
    print(st.session_state["data"])
    st.session_state["data_editor"].data = st.session_state["data"]

modified_df = st.session_state["data"].copy()

# display table
event = st.dataframe(
    st.session_state["data"],
    width=1000,
    key="data_editor",
    column_config={
        "id": st.column_config.NumberColumn(
            "ID",
            help="Dictionary id"
        ),
        "name": st.column_config.TextColumn(
            "Name",
            help="Dictionary name"
        ),
        "description": st.column_config.TextColumn(
            "Description",
            help="Dictionary description"
        )
    },
    hide_index=True,
    selection_mode="single-row",
    on_select="rerun"
)

# delete modal form
@st.experimental_dialog("Delete dictionary")
def delete_dictionary_confirmation(dictionary_index, dictionary_name):
    with st.form("delete_form"):

        st.text(f"Sei sicuro di voler eliminare il dizionario con nome {dictionary_name}")

        submitted = st.form_submit_button("OK")
        if submitted:
            # TODO: handle delete entity from database
            if True:
                delete_dictionary(dictionary_index) # handle tith page refresh
                #st.rerun()
                st.success("deleted")
            else:
                st.stop

# display buttons to update single dictionary
if len(event.selection.rows) > 0:
    event.selection
    _,c1,c2,c3= st.columns([2,1,1,1])

    if c1.button("Update dictionary file", type="primary"):
        dictionary_modal('dic_update', None)

    if c2.button("Update dictionary description", type="primary"):
        dictionary_modal('desc_update', event.selection.rows[0])

    if c3.button("Delete dictionary", type="primary"):
        delete_dictionary_confirmation(event.selection.rows[0], "NAME")
