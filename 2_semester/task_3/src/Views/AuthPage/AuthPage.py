import streamlit as st

from Presenter import AuthPresenter, ChatPresenter
from .LoginButton import LoginButton
from .RegisterButton import RegisterButton


def AuthPage(auth_presenter: AuthPresenter, chat_presenter: ChatPresenter) -> None:
    _, main_column, _  = st.columns([1, 3, 1])
    with main_column:
        st.title("Авторизация")
        email = st.text_input("Электронная почта")
        password = st.text_input("Пароль", type="password")

        left_column, right_column = st.columns(2)
        with left_column:
            LoginButton(email, password, auth_presenter)
        with right_column:
            RegisterButton(email, password, auth_presenter)