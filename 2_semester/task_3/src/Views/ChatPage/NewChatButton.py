import streamlit as st

from Controllers import ChatController

def NewChatButton(user_id: int, chat_controller: ChatController) -> None:
    new_chat_button = st.button("Новый чат")

    if new_chat_button:
        chat_id = chat_controller.create_new_chat(user_id)
        chat_controller.choose_chat(chat_id)