import streamlit as st

from Controllers import AuthController, ChatController
from .Sidebar import Sidebar


def ChatPage(auth_controller: AuthController, chat_controller: ChatController) -> None:
    user_id = st.session_state["user_id"]
    Sidebar(user_id, auth_controller, chat_controller)

    st.title("Чат")