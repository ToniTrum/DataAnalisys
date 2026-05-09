import streamlit as st

from Models import UserModel, ChatModel, UserChatModel
from Controllers import AuthController, ChatController, LlmController
from Views import AuthPage, ChatPage


class PageManager:
    def __init__(self) -> None:
        if "user_model" not in st.session_state:
            st.session_state.user_model = UserModel()
        if "chat_model" not in st.session_state:
            st.session_state.chat_model = ChatModel(
                st.session_state.user_model.client
            )
        if "user_chat_model" not in st.session_state:
            st.session_state.user_chat_model = UserChatModel(
                st.session_state.user_model.client
            )
        
        if "auth_controller" not in st.session_state:
            st.session_state.auth_controller = AuthController(
                st.session_state.user_model,
            )
        if "chat_controller" not in st.session_state:
            st.session_state.chat_controller = ChatController(
                st.session_state.chat_model, 
                st.session_state.user_chat_model
            )
        if "llm_controller" not in st.session_state:
            st.session_state.llm_controller = LlmController()
            
        self.auth_controller = st.session_state.auth_controller
        self.chat_controller = st.session_state.chat_controller
        self.llm_controller = st.session_state.llm_controller

    def render(self) -> None:
        if not st.session_state.get("is_logged_in"):
            if self.auth_controller.check_auto_login():
                st.rerun()

        if st.session_state.get("is_logged_in"):
            ChatPage(self.auth_controller, self.chat_controller, self.llm_controller)
        else:
            AuthPage(self.auth_controller, self.chat_controller)