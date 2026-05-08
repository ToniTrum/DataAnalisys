import streamlit as st

from Controllers import ChatController


def ChatList(user_id: str, chat_controller: ChatController) -> None:
    chats = chat_controller.get_user_chat_list(user_id)
    for chat in chats:
        chat_button = st.button(chat["title"])

        if chat_button:
            chat_controller.choose_chat(chat["chat_id"])