import streamlit as st
from index_manager import IndexManager
import os

sidebar, content = st.columns([0.3, 0.7])
sidebar.write("""
    # ChatSQL
    ## Poc
    """)

IndexManager.createOrLoadIndex()

with content:
    messages = st.container(height=None)
    if prompt := st.chat_input("Input query"):
        messages.chat_message("user").write(prompt)

        result_text = IndexManager.getResult(prompt)

        messages.chat_message("assistant").write((result_text[0]["text"]))