import streamlit as st

from Controllers import AuthController, ChatController
from .NewChatButton import NewChatButton


def Sidebar(user_id: int, auth_controller: AuthController, chat_controller: ChatController) -> None:
    with st.sidebar:
        if st.button("Выход"):
            auth_controller.logout()

        NewChatButton(user_id, chat_controller)
