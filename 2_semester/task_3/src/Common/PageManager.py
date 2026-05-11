import streamlit as st

from Models import UserModel, ChatModel, UserChatModel
from Presenter import AuthPresenter, ChatPresenter, LlmPresenter
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
        
        if "auth_presenter" not in st.session_state:
            st.session_state.auth_presenter = AuthPresenter(
                st.session_state.user_model,
            )
        if "chat_presenter" not in st.session_state:
            st.session_state.chat_presenter = ChatPresenter(
                st.session_state.chat_model, 
                st.session_state.user_chat_model
            )
        if "llm_presenter" not in st.session_state:
            st.session_state.llm_presenter = LlmPresenter()
            
        self.auth_presenter = st.session_state.auth_presenter
        self.chat_presenter = st.session_state.chat_presenter
        self.llm_presenter = st.session_state.llm_presenter

    def render(self) -> None:
        if not st.session_state.get("is_logged_in"):
            if self.auth_presenter.check_auto_login():
                st.rerun()

        if st.session_state.get("is_logged_in"):
            ChatPage(self.auth_presenter, self.chat_presenter, self.llm_presenter)
        else:
            AuthPage(self.auth_presenter, self.chat_presenter)