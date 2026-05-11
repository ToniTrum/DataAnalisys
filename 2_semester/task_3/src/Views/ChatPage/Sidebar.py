import streamlit as st

from Presenter import AuthPresenter, ChatPresenter
from .NewChatButton import NewChatButton


def Sidebar(user_id: int, auth_presenter: AuthPresenter, chat_presenter: ChatPresenter) -> None:
    with st.sidebar:
        if st.button("Выход"):
            auth_presenter.logout()
            st.rerun()

        NewChatButton(user_id, chat_presenter)
