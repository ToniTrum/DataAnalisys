import streamlit as st

from Presenter import AuthPresenter, ChatPresenter, LlmPresenter
from .Sidebar import Sidebar
from .ChatList import ChatList


def ChatPage(auth_presenter: AuthPresenter, chat_presenter: ChatPresenter, llm_presenter: LlmPresenter) -> None:
    user_id = st.session_state["user_id"]

    Sidebar(user_id, auth_presenter, chat_presenter)
    ChatList(user_id, chat_presenter, llm_presenter)
