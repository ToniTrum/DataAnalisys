import streamlit as st

from Controllers import AuthController, ChatController
from .LoginButton import LoginButton
from .RegisterButton import RegisterButton


def AuthPage(auth_controller: AuthController, chat_controller: ChatController) -> None:
    _, main_column, _  = st.columns([1, 3, 1])
    with main_column:
        st.title("Авторизация")
        email = st.text_input("Электронная почта")
        password = st.text_input("Пароль", type="password")

        left_column, right_column = st.columns(2)
        with left_column:
            LoginButton(email, password, auth_controller)
        with right_column:
            RegisterButton(email, password, auth_controller, chat_controller)