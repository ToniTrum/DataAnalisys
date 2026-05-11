import streamlit as st

from Presenter import ChatPresenter

def NewChatButton(user_id: int, chat_presenter: ChatPresenter) -> None:
    new_chat_button = st.button("Новый чат")

    if new_chat_button:
        chat_id = chat_presenter.create_new_chat(user_id)
        chat_presenter.choose_chat(chat_id)