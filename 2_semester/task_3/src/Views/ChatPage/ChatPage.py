import streamlit as st

from Controllers import AuthController, ChatController, LlmController
from .Sidebar import Sidebar
from .ChatList import ChatList


def ChatPage(auth_controller: AuthController, chat_controller: ChatController, llm_controller: LlmController) -> None:
    user_id = st.session_state["user_id"]

    Sidebar(user_id, auth_controller, chat_controller)
    ChatList(user_id, chat_controller, llm_controller)
